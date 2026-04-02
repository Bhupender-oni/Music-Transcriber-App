import os
import sys
import subprocess
import shutil

def check_system():
    print("--- Music Transcriber System Check ---")
    
    # 1. Check Python Version
    print(f"Python Version: {sys.version}")
    
    # 2. Check FFmpeg
    # Add local ffmpeg to path for this check
    ffmpeg_bin = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg-master-latest-win64-gpl", "bin")
    if os.path.exists(ffmpeg_bin):
        os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ.get("PATH", "")
    
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"FFmpeg Status: FOUND ({ffmpeg_path})")
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            print(result.stdout.split('\n')[0])
        except Exception as e:
            print(f"Error checking FFmpeg version: {e}")
    else:
        print("FFmpeg Status: NOT FOUND")

    # 3. Check PyTorch
    torch_ok = False
    try:
        import torch
        torch_ok = True
    except ImportError:
        pass

    if torch_ok:
        print(f"PyTorch Version: {torch.__version__}")
        cuda_avail = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_avail}")
        if cuda_avail:
            print(f"Device Name: {torch.cuda.get_device_name(0)}")
        
        # Check for DirectML (Intel GPU support)
        try:
            import torch_directml
            dml_avail = torch_directml.is_available()
            print(f"DirectML Available: {dml_avail}")
            if dml_avail:
                print(f"DirectML Device: {torch_directml.device().type}")
                print("Intel GPU detected via DirectML.")
        except ImportError:
            print("DirectML Status: NOT INSTALLED")
    else:
        print("PyTorch Status: NOT FOUND")

    print("---------------------------------------")

if __name__ == "__main__":
    check_system()
