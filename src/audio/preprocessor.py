import numpy as np
import librosa

def resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)

def normalize(audio: np.ndarray) -> np.ndarray:
    return audio / (np.max(np.abs(audio)) + 1e-10)