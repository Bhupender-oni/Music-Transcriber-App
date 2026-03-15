import json
import numpy as np
import librosa
from pathlib import Path
from typing import Dict, Optional
from src.config import settings
from src.audio.tonic_detector import detect_tonic

try:
    from bhargava_swara import raga as bhargava_raga
    BHARGAVA_AVAILABLE = True
except ImportError:
    BHARGAVA_AVAILABLE = False
    print("bhargava-swara not installed; using built-in raga database.")

class RagaIdentifier:
    def __init__(self):
        self.raga_db = self._load_raga_db()
        if BHARGAVA_AVAILABLE:
            self.bhargava = bhargava_raga.RagaDetector()
        else:
            self.bhargava = None

    def _load_raga_db(self):
        db_path = Path(settings.raga_db_path)
        if db_path.exists():
            with open(db_path, 'r') as f:
                return json.load(f)
        default = {
            "Yaman": {"thaat": "Kalyan", "aaroh": ["N","R","G","M#","P","D","N","S"], "avaroh": ["S","N","D","P","M#","G","R","S"], "vadi": "G", "samvadi": "N", "time": "Evening"},
            "Bhairav": {"thaat": "Bhairav", "aaroh": ["S","r","G","M","P","d","N","S"], "avaroh": ["S","N","d","P","M","G","r","S"], "vadi": "d", "samvadi": "r", "time": "Morning"}
        }
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(db_path, 'w') as f:
            json.dump(default, f, indent=2)
        return default

    # ================= Main Public Method =================
    def identify(self, audio_path: str, tonic: Optional[float] = None) -> Dict:
        audio, sr = librosa.load(audio_path, sr=22050, mono=True)
        if tonic is None:
            tonic = detect_tonic(audio, sr)

        f0 = self._extract_pitch(audio, sr)
        if len(f0) == 0:
            return self._unknown_result()

        cents = self._freq_to_cents(f0, tonic)
        if len(cents) == 0:
            return self._unknown_result()

        hist = self._compute_pitch_histogram(cents)

        if BHARGAVA_AVAILABLE and self.bhargava:
            try:
                return self._predict_with_bhargava(hist)
            except Exception:
                # Fall through to fallback method
                pass

        return self._fallback_raga_match(hist)

    # ================= Helper Methods =================
    def _extract_pitch(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Extract fundamental frequency contour and remove NaN values."""
        f0, _, _ = librosa.pyin(audio, fmin=50, fmax=2000, sr=sr)
        return f0[~np.isnan(f0)]

    def _freq_to_cents(self, f0: np.ndarray, tonic: float) -> np.ndarray:
        """Convert frequencies to cents relative to tonic and clip to valid range."""
        cents = 1200 * np.log2(f0 / tonic)
        return cents[(cents > 0) & (cents < 1200)]

    def _compute_pitch_histogram(self, cents: np.ndarray) -> np.ndarray:
        """Create normalized 12‑bin histogram of pitch cents."""
        hist, _ = np.histogram(cents, bins=12, range=(0, 1200))
        return hist / (len(cents) + 1e-10)

    def _unknown_result(self) -> Dict:
        """Return a safe 'unknown' result when no data is available."""
        return {'primary_raga': 'Unknown', 'confidence': 0, 'alternatives': []}

    def _predict_with_bhargava(self, hist: np.ndarray) -> Dict:
        """Use bhargava‑swara library to predict raga."""
        res = self.bhargava.predict_from_histogram(hist, top_k=3)
        return {
            'primary_raga': res[0]['raga'],
            'confidence': res[0]['confidence'],
            'alternatives': res[1:],
            'raga_details': self.raga_db.get(res[0]['raga'], {})
        }

    def _fallback_raga_match(self, hist: np.ndarray) -> Dict:
        """Fallback rule‑based raga identification when bhargava is unavailable."""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(hist, height=0.05)
        peak_notes = [int(p) for p in peaks]

        best_raga = 'Yaman'
        best_score = 0
        swara_to_idx = {'S':0, 'r':1, 'R':2, 'g':3, 'G':4, 'M':5, 'M#':6, 'P':7, 'd':8, 'D':9, 'n':10, 'N':11}

        for raga_name, info in self.raga_db.items():
            expected = self._get_expected_swaras(info, swara_to_idx)
            if not expected:
                continue
            score = len(set(peak_notes) & set(expected)) / len(expected)
            if score > best_score:
                best_score = score
                best_raga = raga_name

        return {
            'primary_raga': best_raga,
            'confidence': best_score,
            'alternatives': [],
            'raga_details': self.raga_db.get(best_raga, {})
        }

    def _get_expected_swaras(self, raga_info: Dict, swara_to_idx: Dict) -> list:
        """Extract unique swara indices from a raga's aaroh and avaroh."""
        expected = []
        for note in raga_info.get('aaroh', []) + raga_info.get('avaroh', []):
            if note in swara_to_idx:
                expected.append(swara_to_idx[note])
        return list(set(expected))