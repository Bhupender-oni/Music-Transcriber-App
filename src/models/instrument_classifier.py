import json
import numpy as np
import librosa
from pathlib import Path
from typing import List, Dict
from src.config import settings

class InstrumentClassifier:
    def __init__(self):
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        db_path = Path(settings.instrument_db_path)
        if db_path.exists():
            with open(db_path, 'r') as f:
                return json.load(f)
        default = {
            'tabla': {'freq_range': [100,400], 'zcr_range': [0.05,0.15]},
            'sitar': {'freq_range': [150,1500], 'zcr_range': [0.02,0.08]},
            'bansuri': {'freq_range': [500,2000], 'zcr_range': [0.01,0.05]},
            'harmonium': {'freq_range': [200,2000], 'zcr_range': [0.03,0.07]},
            'violin': {'freq_range': [200,3000], 'zcr_range': [0.02,0.06]},
            'flute': {'freq_range': [500,2500], 'zcr_range': [0.01,0.04]},
            'vocals': {'freq_range': [80,1000], 'zcr_range': [0.02,0.1]},
            'piano': {'freq_range': [27,4000], 'zcr_range': [0.01,0.05]}
        }
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(db_path, 'w') as f:
            json.dump(default, f, indent=2)
        return default

    def classify(self, audio: np.ndarray, sr: int) -> List[Dict]:
        centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio))
        results = []
        for name, prof in self.profiles.items():
            if prof['freq_range'][0] <= centroid <= prof['freq_range'][1] and \
               prof['zcr_range'][0] <= zcr <= prof['zcr_range'][1]:
                results.append({'name': name, 'confidence': 0.7})
        return results[:5]