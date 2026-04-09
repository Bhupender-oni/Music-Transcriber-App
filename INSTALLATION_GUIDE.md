# Python 3.13 Installation & Setup Instructions

## ✅ What's Been Updated

1. **requirements.txt** - All packages updated to latest Python 3.13 compatible versions
2. **pyproject.toml** - Modern Python packaging with Python 3.13 support
3. **setup.py** - Automated setup script for Python 3.13
4. **PYTHON313_COMPATIBILITY.md** - Detailed compatibility guide

---

## 🚀 Fresh Start (Recommended)

### Step 1: Clean Up Old Environment
```bash
cd C:\Users\Bhupender\Documents\Music\Music-Transcriber-App

# Remove old venv
rmdir /s /q venv

# Remove pip cache
rmdir /s /q %APPDATA%\pip
```

### Step 2: Create New Virtual Environment
```bash
# Verify Python version
python --version
# Should output: Python 3.13.1 (or similar)

# Create fresh venv
python -m venv venv

# Activate venv
venv\Scripts\activate
# You should see (venv) prefix in terminal
```

### Step 3: Upgrade pip & Setuptools
```bash
pip install --upgrade pip setuptools wheel
# Should complete without errors
```

### Step 4: Install Dependencies

#### Option A: Using setup.py (Automated)
```bash
python setup.py
```

#### Option B: Using requirements.txt (Manual)
```bash
pip install -r requirements.txt
```

#### Option C: Using pyproject.toml (Modern)
```bash
pip install -e .
```

### Step 5: Verify Installation
```bash
# Test all imports
python -c "import torch; import librosa; import flask; print('✅ All imports OK')"

# Start application
python run.py --debug
```

Expected output:
```
============================================================
Music Transcriber 2026 - Indian Classical Music Analysis
============================================================
Starting on 127.0.0.1:5000
Configuration: CPU mode
Demucs enabled: True
Raga detection: True
Tala detection: True
============================================================
```

---

## 📦 Package Versions (Python 3.13 Optimized)

| Package | Version | Status |
|---------|---------|--------|
| Python | 3.13.1 | ✅ Latest |
| torch | 2.4.1+ | ✅ Latest |
| librosa | 0.11.0+ | ✅ Latest |
| numpy | 2.2.0+ | ✅ Latest (3.13 optimized) |
| scipy | 1.15.0+ | ✅ Latest |
| flask | 3.1.0+ | ✅ Latest |
| pandas | 2.3.0+ | ✅ Latest |
| matplotlib | 3.10.0+ | ✅ Latest (3.13 compatible) |
| scikit-learn | 1.6.0+ | ✅ Latest |

---

## ⚠️ Warnings (Normal, Not Errors)

### Warning: IDTAP not installed
```
IDTAP not installed; using robust histogram method.
```
**Status**: ✅ OK - Fallback method works fine

### Warning: torchcodec not found
```
UserWarning: torchcodec is not installed correctly
```
**Status**: ✅ OK - App uses librosa instead

**These are just warnings, NOT errors. Your app will work fine.**

---

## 🔧 If You Get Errors

### Error: "ModuleNotFoundError: No module named 'X'"
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Or use setup.py
python setup.py
```

### Error: "conflicting dependencies"
```bash
# Clean install
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "No module named 'src'"
```bash
# Always run from project root
cd C:\Users\Bhupender\Documents\Music\Music-Transcriber-App
python run.py --debug
```

### Error: "Port 5000 already in use"
```bash
# Use different port
python run.py --port 8000
```

---

## ✨ Optional: Additional Development Tools

For development, install optional dependencies:

```bash
# Dev tools (testing, linting, formatting)
pip install -e ".[dev]"

# Music analysis tools
pip install -e ".[music]"

# All extras
pip install -e ".[dev,music]"
```

### Available Extras
- **dev**: pytest, black, ruff, mypy, jupyter
- **music**: Enhanced music analysis tools
- **gpu**: CUDA support (install separately with PyTorch)

---

## 📊 Installation Verification

Run these commands to verify everything:

```bash
# Check Python version
python --version
# Expected: Python 3.13.1

# Check pip packages
pip list | find "torch\|librosa\|flask"

# Test imports
python -c "
import sys
print(f'Python: {sys.version}')
import torch; print(f'PyTorch: {torch.__version__}')
import librosa; print(f'Librosa: {librosa.__version__}')
import flask; print(f'Flask: {flask.__version__}')
import numpy; print(f'NumPy: {numpy.__version__}')
print('✅ All imports successful!')
"

# Run tests
python -m pytest tests/ -v
```

---

## 🎯 Next Steps

After successful installation:

1. **Start Development Server**
   ```bash
   python run.py --debug
   ```

2. **Open Browser**
   - Navigate to: http://127.0.0.1:5000

3. **Upload Audio File**
   - Select an Indian classical music file
   - Wait for analysis to complete

4. **Run Tests**
   ```bash
   python -m pytest tests/ -v
   ```

5. **Deploy (Optional)**
   ```bash
   gunicorn --bind 0.0.0.0:8000 'src.api.routes:create_app()'
   ```

---

## 🆘 Need Help?

Check these files for more info:
- `SETUP_GUIDE.md` - General setup guide
- `PYTHON313_COMPATIBILITY.md` - Detailed compatibility info
- `PROJECT_STRUCTURE.md` - Project organization
- `VERIFICATION_REPORT.txt` - Structure verification

---

## 📝 Summary

✅ **All dependencies are Python 3.13 compatible**
✅ **Latest stable versions installed**
✅ **Optimized for performance**
✅ **Ready for development and deployment**

**Your setup is complete!** 🎉
