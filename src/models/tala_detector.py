import numpy as np
import librosa
from typing import Dict

class TalaDetector:
    def __init__(self):
        self.talas = {
            'Teental': 16, 'Jhaptaal': 10, 'Rupak': 7, 'Ektaal': 12,
            'Dadra': 6, 'Keherwa': 8, 'Chautaal': 12, 'Dhamar': 14,
            'Sooltaal': 10, 'Teevra': 7
        }

    def detect(self, audio: np.ndarray, sr: int) -> Dict:
        onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        if len(beats) < 4:
            return {'primary_tala': 'Unknown', 'tempo': tempo, 'beats_per_cycle': 0, 'confidence': 0}
        beat_times = librosa.frames_to_time(beats, sr=sr)
        beat_intervals = np.diff(beat_times)
        from scipy.signal import correlate
        correlation = correlate(beat_intervals, beat_intervals)
        peaks = np.where(correlation > np.percentile(correlation, 95))[0]
        if len(peaks) > 1:
            cycle_length = np.median(np.diff(peaks))
        else:
            cycle_length = 16
        closest = min(self.talas.items(), key=lambda x: abs(x[1] - cycle_length))
        confidence = 1 - (abs(closest[1] - cycle_length) / closest[1])
        return {
            'primary_tala': closest[0],
            'beats_per_cycle': closest[1],
            'detected_cycle_length': cycle_length,
            'tempo': tempo,
            'confidence': confidence
        }