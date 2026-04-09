from flask import Flask, request, jsonify, render_template
import os
import uuid
import threading
import time
import numpy as np
from pathlib import Path
from src.config import settings
from src.audio import load_audio, detect_tonic, extract_pitch_contour
from src.transcription import generate_sargam
from src.models import RagaIdentifier, TalaDetector, InstrumentClassifier
from src.separation.demucs_wrapper import DemucsSeparator
from src.visualization import create_pitch_contour_plot, create_raga_plot
from .websocket import socketio

# Ensure bundled ffmpeg/ffprobe is on PATH (fixes broken Chocolatey shim)
_HERE = Path(__file__).resolve().parent.parent.parent  # project root
_FFMPEG_BIN = _HERE / "ffmpeg" / "ffmpeg-master-latest-win64-gpl" / "bin"
if _FFMPEG_BIN.is_dir() and str(_FFMPEG_BIN) not in os.environ.get("PATH", ""):
    os.environ["PATH"] = str(_FFMPEG_BIN) + os.pathsep + os.environ.get("PATH", "")

def _create_model_getters(models_cache):
    """Create lazy-loading getter functions for models"""
    def get_raga_identifier():
        if 'raga' not in models_cache:
            models_cache['raga'] = RagaIdentifier()
        return models_cache['raga']

    def get_tala_detector():
        if 'tala' not in models_cache:
            models_cache['tala'] = TalaDetector()
        return models_cache['tala']

    def get_instrument_classifier():
        if 'instrument' not in models_cache:
            models_cache['instrument'] = InstrumentClassifier()
        return models_cache['instrument']

    def get_separator():
        if 'separator' not in models_cache and settings.demucs_enabled:
            models_cache['separator'] = DemucsSeparator()
        return models_cache.get('separator')

    return get_raga_identifier, get_tala_detector, get_instrument_classifier, get_separator

def _register_routes(app, jobs, get_raga_identifier, get_tala_detector, get_instrument_classifier, get_separator):
    """Register all Flask routes"""
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'No file'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > settings.max_audio_length * 1024 * 1024:
            return jsonify({'error': f'File too large (max {settings.max_audio_length}MB)'}), 413
        
        job_id = str(uuid.uuid4())
        filename = f"{job_id}_{file.filename}"
        filepath = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(filepath)
        
        thread = threading.Thread(
            target=process_audio, 
            args=(job_id, filepath, jobs, get_raga_identifier, get_tala_detector, 
                  get_instrument_classifier, get_separator)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id, 'status': 'processing'})

    @app.route('/status/<job_id>', methods=['GET'])
    def get_status(job_id):
        job = jobs.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        if job.get('status') != 'complete':
            return jsonify({
                'status': job.get('status', 'unknown'),
                'progress': job.get('progress', 0)
            }), 202
        return jsonify(job.get('result', {}))

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder='../../web/templates', static_folder='../../web/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    models_cache = {}
    jobs = {}
    
    model_getters = _create_model_getters(models_cache)
    _register_routes(app, jobs, *model_getters)
    
    socketio.init_app(app, cors_allowed_origins="*")
    return app

def _convert_to_serializable(obj):
    """Recursively convert numpy arrays and types to native Python types"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_convert_to_serializable(item) for item in obj]
    return obj

def _load_and_prepare_audio(job_id, filepath, jobs):
    """Load audio and prepare it for processing"""
    print(f"[{job_id}] Loading audio...")
    audio, sr = load_audio(filepath, sr=22050, mono=True)
    jobs[job_id]['progress'] = 10
    
    duration = len(audio) / sr
    if duration > 300:  # 5 minutes
        audio = audio[:sr * 300]
    return audio, sr, duration

def _detect_raga_and_tala(job_id, filepath, audio, sr, tonic, jobs, get_raga_identifier, get_tala_detector):
    """Detect raga and tala"""
    print(f"[{job_id}] Identifying raga...")
    raga_identifier = get_raga_identifier()
    raga_info = raga_identifier.identify(filepath, tonic)
    jobs[job_id]['progress'] = 50
    
    print(f"[{job_id}] Detecting tala...")
    tala_detector = get_tala_detector()
    tala_info = tala_detector.detect(audio, sr)
    jobs[job_id]['progress'] = 60
    
    return raga_info, tala_info

def _classify_instruments(job_id, audio, sr, jobs, get_instrument_classifier):
    """Classify instruments with error handling"""
    try:
        print(f"[{job_id}] Classifying instruments...")
        instrument_classifier = get_instrument_classifier()
        instruments = instrument_classifier.classify(audio[:sr*10], sr)
    except Exception as e:
        print(f"[{job_id}] Instrument classification failed: {e}")
        instruments = []
    jobs[job_id]['progress'] = 70
    return instruments

def _separate_sources(job_id, filepath, jobs, get_separator):
    """Separate audio sources with error handling"""
    stems = {}
    if settings.demucs_enabled:
        try:
            print(f"[{job_id}] Separating sources...")
            separator = get_separator()
            if separator:
                stems = separator.separate_file(filepath)
        except Exception as e:
            print(f"[{job_id}] Separation failed: {e}")
    jobs[job_id]['progress'] = 85
    return stems

def _create_visualizations(job_id, f0, times, raga_info, jobs):
    """Create visualizations with error handling"""
    try:
        print(f"[{job_id}] Creating visualizations...")
        pitch_plot = create_pitch_contour_plot(f0, times)
        raga_plot = create_raga_plot(raga_info)
    except Exception as e:
        print(f"[{job_id}] Visualization failed: {e}")
        pitch_plot = None
        raga_plot = None
    jobs[job_id]['progress'] = 95
    return pitch_plot, raga_plot

def process_audio(job_id, filepath, jobs, get_raga_identifier, get_tala_detector, 
                  get_instrument_classifier, get_separator):
    """Process audio file with optimization for speed"""
    start_time = time.time()
    
    try:
        jobs[job_id] = {'status': 'loading', 'progress': 0}
        
        # Step 1: Load and prepare audio
        audio, sr, duration = _load_and_prepare_audio(job_id, filepath, jobs)
        
        # Step 2: Detect tonic
        print(f"[{job_id}] Detecting tonic...")
        tonic = detect_tonic(audio, sr)
        jobs[job_id]['progress'] = 20
        
        # Step 3: Extract pitch contour
        print(f"[{job_id}] Extracting pitch contour...")
        f0, times = extract_pitch_contour(audio, sr)
        jobs[job_id]['progress'] = 30
        
        # Step 4: Generate sargam
        print(f"[{job_id}] Generating sargam...")
        sargam = generate_sargam(f0, tonic, times, sr)
        jobs[job_id]['progress'] = 40
        
        # Step 5 & 6: Identify raga and detect tala
        raga_info, tala_info = _detect_raga_and_tala(
            job_id, filepath, audio, sr, tonic, jobs, get_raga_identifier, get_tala_detector
        )
        
        # Step 7: Classify instruments
        instruments = _classify_instruments(job_id, audio, sr, jobs, get_instrument_classifier)
        
        # Step 8: Separate sources
        stems = _separate_sources(job_id, filepath, jobs, get_separator)
        
        # Step 9: Create visualizations
        pitch_plot, raga_plot = _create_visualizations(job_id, f0, times, raga_info, jobs)
        
        # Compile results
        result = {
            'tonic': float(tonic),
            'sargam': [{'note': str(n), 'time': float(t)} for n, t in zip(sargam[:200], times[:200])],
            'raga': _convert_to_serializable(raga_info),
            'tala': _convert_to_serializable(tala_info),
            'instruments': _convert_to_serializable(instruments),
            'stems': _convert_to_serializable(stems),
            'pitch_plot': pitch_plot,
            'raga_plot': raga_plot,
            'duration': float(duration)
        }
        
        jobs[job_id]['status'] = 'complete'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result'] = result
        
        elapsed = time.time() - start_time
        print(f"[{job_id}] Processing complete in {elapsed:.1f}s")
        
        # Cleanup
        try:
            os.remove(filepath)
        except OSError:
            pass
            
    except Exception as e:
        import traceback
        print(f"[{job_id}] Error: {e}")
        traceback.print_exc()
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)
