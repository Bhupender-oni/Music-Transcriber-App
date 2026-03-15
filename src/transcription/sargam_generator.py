import numpy as np
from typing import List, Dict
from src.audio.ornament_detector import detect_ornaments

SWARA_MAP = {
    0: 'S', 100: 'r', 200: 'R', 300: 'g', 400: 'G',
    500: 'M', 600: 'M#', 700: 'P', 800: 'd', 900: 'D',
    1000: 'n', 1100: 'N'
}

def generate_sargam(pitch_contour: np.ndarray, tonic: float, times: np.ndarray, sr: int) -> List[Dict]:
    if tonic <= 0:
        return []
    ornaments = detect_ornaments(pitch_contour, sr)
    ornament_at_time = {}
    for o_type, occ_list in ornaments.items():
        for occ in occ_list:
            idx = int(occ['time'] * sr / 512)
            if 0 <= idx < len(pitch_contour):
                ornament_at_time[idx] = o_type
    sargam = []
    for i, freq in enumerate(pitch_contour):
        if freq > 0:
            cents = 1200 * np.log2(freq / tonic)
            cents = max(0, min(1199, cents))
            swara_cents = min(SWARA_MAP.keys(), key=lambda x: abs(x - cents))
            note = SWARA_MAP[swara_cents]
            ornament = ornament_at_time.get(i, 'none')
            sargam.append({
                'time': float(times[i]),
                'note': note,
                'frequency': float(freq),
                'cents': float(cents),
                'ornament': ornament
            })
    return sargam