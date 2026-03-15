import numpy as np
import librosa

def detect_tonic_robust(audio: np.ndarray, sr: int) -> float:
    f0, _, _ = librosa.pyin(audio, fmin=65, fmax=2093, sr=sr)
    f0 = f0[~np.isnan(f0)]
    if len(f0) > 0:
        hist, bins = np.histogram(f0, bins=50)
        tonic_hist = bins[np.argmax(hist)]
    else:
        tonic_hist = 220.0
    spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)
    tonic_spec = np.median(spectral_centroids)
    return float(0.7 * tonic_hist + 0.3 * tonic_spec)

try:
    from idtap import HindustaniAnalyzer
    _idtap = HindustaniAnalyzer()
    def detect_tonic(audio: np.ndarray, sr: int) -> float:
        return _idtap.detect_tonic(audio, sr)
except ImportError:
    detect_tonic = detect_tonic_robust
    print("IDTAP not installed; using robust histogram method.")