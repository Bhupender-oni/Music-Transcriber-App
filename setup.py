#!/usr/bin/env python
"""
Setup script for Music Transcriber with Python 3.13
Handles dependency installation and compatibility
"""
import sys
import subprocess
import platform

def check_python_version():
    """Verify Python 3.13 compatibility"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        sys.exit(1)
    
    if version.major == 3 and version.minor >= 13:
        print("✅ Python 3.13+ detected - Using optimized dependencies")
        return "3.13+"
    else:
        print(f"✅ Python {version.major}.{version.minor} - Compatible")
        return f"{version.major}.{version.minor}"

def install_dependencies():
    """Install all dependencies"""
    print("\n📦 Installing dependencies for Python 3.13+...")
    
    # Core dependencies
    core_packages = [
        "librosa>=0.11.0",
        "soundfile>=0.13.0",
        "audioread>=3.1.0",
        "scipy>=1.15.0",
        "numpy>=2.2.0",
        "pandas>=2.3.0",
    ]
    
    # PyTorch (CPU version for Windows)
    pytorch_packages = [
        "torch>=2.4.1",
        "torchaudio>=2.4.1",
        "torchvision>=0.19.1",
    ]
    
    # Music analysis
    music_packages = [
        "demucs>=4.0.0",
        "scikit-learn>=1.6.0",
        "mir_eval>=0.8.0",
        "python-speech-features>=0.6",
    ]
    
    # Web framework
    web_packages = [
        "flask>=3.1.0",
        "flask-cors>=5.0.0",
        "flask-socketio>=5.4.0",
        "gunicorn>=23.0.0",
        "python-socketio>=5.11.0",
        "python-engineio>=4.11.0",
    ]
    
    # Utilities
    util_packages = [
        "python-dotenv>=1.0.1",
        "pydantic>=2.6.0",
        "pydantic-settings>=2.0.0",
        "matplotlib>=3.10.0",
        "seaborn>=0.13.2",
        "plotly>=5.25.0",
    ]
    
    all_packages = core_packages + pytorch_packages + music_packages + web_packages + util_packages
    
    print(f"Installing {len(all_packages)} packages...\n")
    
    try:
        # Upgrade pip first
        print("🔄 Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        
        # Install in groups
        groups = [
            ("Core audio libraries", core_packages),
            ("PyTorch", pytorch_packages),
            ("Music analysis", music_packages),
            ("Web framework", web_packages),
            ("Utilities", util_packages),
        ]
        
        for group_name, packages in groups:
            print(f"\n📥 Installing {group_name}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + packages + ["-q"],
                stdout=subprocess.DEVNULL
            )
            print(f"✅ {group_name} installed")
        
        print("\n✅ All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    print("=" * 70)
    print("Music Transcriber Setup for Python 3.13+")
    print("=" * 70)
    
    # Check Python version
    py_version = check_python_version()
    
    # Check platform
    system = platform.system()
    print(f"🖥️  Platform: {system}")
    
    if system == "Windows":
        print("✅ Windows detected - Using compatible packages")
    
    # Install dependencies
    if install_dependencies():
        print("\n" + "=" * 70)
        print("🎉 Setup complete! You can now run:")
        print("   python run.py --debug")
        print("=" * 70)
    else:
        print("\n❌ Setup failed. Please check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
