import librosa
import numpy as np
from typing import Tuple

def extract_pitch_contour(audio: np.ndarray, sr: int) -> Tuple[np.ndarray, np.ndarray]:
    f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'),
                             fmax=librosa.note_to_hz('C7'), sr=sr, hop_length=512)
    f0 = np.nan_to_num(f0)
    times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=512)
    return f0, times