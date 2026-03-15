import librosa
import soundfile as sf
import numpy as np
from typing import Optional, Tuple
from src.config import settings

def load_audio(file_path: str, sr: Optional[int] = None, mono: bool = True) -> Tuple[np.ndarray, int]:
    if sr is None:
        sr = settings.target_sample_rate
    audio, sr = librosa.load(file_path, sr=sr, mono=mono)
    return audio, sr

def save_audio(file_path: str, audio: np.ndarray, sr: int):
    sf.write(file_path, audio, sr)