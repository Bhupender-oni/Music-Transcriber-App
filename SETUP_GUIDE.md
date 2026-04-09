# Music Transcriber 2026 - Complete Setup & Usage Guide

## ✅ Project Structure Verified

All files are properly connected. No structural errors found.

### Module Hierarchy
```
src/
├── audio/           → load_audio, detect_tonic, extract_pitch_contour
├── models/          → RagaIdentifier, TalaDetector, InstrumentClassifier  
├── transcription/   → generate_sargam
├── separation/      → DemucsSeparator
├── visualization/   → create_pitch_contour_plot, create_raga_plot
├── api/             → Flask app with routes
└── config.py        → Settings & configuration
```

---

## 🚀 Getting Started

### 1. Activate Virtual Environment
```bash
cd C:\Users\Bhupender\Documents\Music\Music-Transcriber-App

# Activate venv
venv\Scripts\activate

# Verify: you should see (venv) prefix in terminal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### Option A: Development Mode (with debug)
```bash
python run.py --debug
```
- Auto-reloads on code changes
- Full error tracebacks
- Runs on http://127.0.0.1:5000

#### Option B: Production Mode
```bash
python run.py --port 8000
```
- Runs on http://127.0.0.1:8000
- No auto-reload

#### Option C: Docker (if configured)
```bash
docker-compose up
```

---

## 🧪 Running Tests

### From Project Root (CORRECT WAY)
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_audio.py -v

# Using test runner script
python tests/run_tests.py
```

### ❌ DON'T Run Tests from tests/ Directory
This will cause `ModuleNotFoundError` because `src` won't be in Python path.

---

## 📁 File Connection Summary

| Component | File | Imports From | Status |
|-----------|------|--------------|--------|
| Entry Point | `run.py` | `src.api.routes`, `src.config` | ✅ |
| Flask App | `src/api/routes.py` | All submodules | ✅ |
| Audio Module | `src/audio/__init__.py` | `.loader`, `.tonic_detector`, `.pitch_extractor` | ✅ |
| Models Module | `src/models/__init__.py` | `.raga_identifier`, `.tala_detector` | ✅ |
| Transcription | `src/transcription/__init__.py` | `.sargam_generator` | ✅ |
| Separation | `src/separation/__init__.py` | `.demucs_wrapper` | ✅ |
| Visualization | `src/visualization/__init__.py` | `.interactive_plots` | ✅ |

---

## 🔧 Fixes Applied

### 1. Removed Unused Import
- ❌ `import sys` from routes.py (was unused)

### 2. Organized Imports
- Moved `import numpy as np` to top of routes.py
- Ensures proper import order

### 3. Improved Error Handling
- Added `OSError` exception for file operations
- Better error messages in processing steps

### 4. Enhanced Routes Structure
- `_create_model_getters()` - lazy loads models
- `_register_routes()` - registers endpoints
- `create_app()` - initializes Flask
- Helper functions extracted for clarity

### 5. Added Test Runner
- Created `tests/run_tests.py` for easy test execution
- Automatically discovers all test files

### 6. Updated run.py
- Better logging and startup messages
- Configuration display on startup
- Cleaner help text

---

## 🎯 Typical Workflow

### Development
```bash
# 1. Activate venv
venv\Scripts\activate

# 2. Start server in debug mode
python run.py --debug

# 3. In another terminal, run tests
python -m pytest tests/ -v

# 4. Make changes, server auto-reloads
# (browser will show new changes)
```

### Before Commit
```bash
# Run full test suite
python -m pytest tests/ -v

# Check code style
python -m flake8 src/ tests/
```

---

## ⚠️ Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'src'`
**Solution:** Always run from project root
```bash
cd C:\Users\Bhupender\Documents\Music\Music-Transcriber-App
python tests/test_audio.py  # ✅ Works
```

### Issue: `No venv found`
**Solution:** Recreate it
```bash
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution:** Use different port
```bash
python run.py --port 8000
```

### Issue: Templates not found
**Solution:** Ensure web/ directory exists with templates/ subdirectory
```bash
C:\Users\Bhupender\Documents\Music\Music-Transcriber-App\
└── web/
    ├── templates/
    │   └── index.html
    └── static/
```

---

## 📊 Configuration

Edit `src/config.py` to customize:
- `target_sample_rate` - Audio processing sample rate (default: 22050)
- `max_audio_length` - Max audio length in seconds (default: 300s / 5min)
- `demucs_enabled` - Enable source separation (default: True)
- `raga_detection_enabled` - Enable raga detection (default: True)
- `tala_detection_enabled` - Enable tala detection (default: True)

---

## ✨ API Endpoints

- `GET /` - Web UI
- `POST /upload` - Upload audio file → returns `job_id`
- `GET /status/<job_id>` - Check processing status

---

## 📝 Next Steps

1. ✅ Verify venv is activated
2. ✅ Run `python run.py --debug`
3. ✅ Open http://127.0.0.1:5000 in browser
4. ✅ Upload a music file to test
5. ✅ Run tests with `python -m pytest tests/ -v`

All systems are **GO**! 🚀
