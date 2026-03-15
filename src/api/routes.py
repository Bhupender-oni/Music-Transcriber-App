from flask import Flask, request, jsonify, render_template
import os
import uuid
import threading
from src.config import settings
from src.audio import load_audio, detect_tonic, extract_pitch_contour
from src.transcription import generate_sargam, QwenMusicTranscriber
from src.models import RagaIdentifier, TalaDetector, InstrumentClassifier
from src.separation.demucs_wrapper import DemucsSeparator
from src.visualization import create_pitch_contour_plot, create_raga_plot
from .websocket import socketio

def create_app():
    app = Flask(__name__, template_folder='../../web/templates', static_folder='../../web/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret-key') #NOSONAR
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    raga_identifier = RagaIdentifier()
    tala_detector = TalaDetector()
    instrument_classifier = InstrumentClassifier()
    separator = DemucsSeparator(device="cpu")
    transcriber = QwenMusicTranscriber(device="cpu")

    jobs = {}

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
        job_id = str(uuid.uuid4())
        filename = f"{job_id}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        thread = threading.Thread(target=process_audio, args=(job_id, filepath, jobs,
            raga_identifier, tala_detector, instrument_classifier, separator, transcriber))
        thread.daemon = True
        thread.start()
        return jsonify({'job_id': job_id, 'status': 'processing'})

    @app.route('/upload',methods=['POST'])
    def get_status(job_id):
        return jsonify(jobs.get(job_id, {}))

    @app.route('/status/<job_id>',methods=['GET'])
    def get_results(job_id):
        job = jobs.get(job_id)
        if not job:
            return jsonify({'error': 'Not found'}), 404
        if job.get('status') != 'complete':
            return jsonify({'status': job.get('status', 'unknown')}), 202
        return jsonify(job.get('result', {}))

    socketio.init_app(app, cors_allowed_origins="*")
    return app

def process_audio(job_id, filepath, jobs, raga_identifier, tala_detector, instrument_classifier, separator, transcriber):
    try:
        jobs[job_id] = {'status': 'loading', 'progress': 0}
        audio, sr = load_audio(filepath, sr=22050, mono=True)
        jobs[job_id]['progress'] = 10

        tonic = detect_tonic(audio, sr)
        jobs[job_id]['progress'] = 20

        f0, times = extract_pitch_contour(audio, sr)
        jobs[job_id]['progress'] = 30

        sargam = generate_sargam(f0, tonic, times, sr)
        jobs[job_id]['progress'] = 40

        raga_info = raga_identifier.identify(filepath, tonic)
        jobs[job_id]['progress'] = 50

        tala_info = tala_detector.detect(audio, sr)
        jobs[job_id]['progress'] = 60

        instruments = instrument_classifier.classify(audio[:sr*10], sr)
        jobs[job_id]['progress'] = 70

        stems = separator.separate_file(filepath)
        jobs[job_id]['progress'] = 85

        pitch_plot = create_pitch_contour_plot(f0, times)
        raga_plot = create_raga_plot(raga_info)
        jobs[job_id]['progress'] = 95

        result = {
            'tonic': tonic,
            'sargam': sargam[:200],
            'raga': raga_info,
            'tala': tala_info,
            'instruments': instruments,
            'stems': stems,
            'pitch_plot': pitch_plot,
            'raga_plot': raga_plot,
            'duration': len(audio)/sr
        }
        jobs[job_id]['status'] = 'complete'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result'] = result
    except Exception as e:
        import traceback
        traceback.print_exc() 
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)