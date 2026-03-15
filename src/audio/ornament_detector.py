import numpy as np
from typing import Dict, List

def detect_ornaments(pitch_contour: np.ndarray, sr: int, hop_length: int = 512) -> Dict[str, List[Dict]]:
    if len(pitch_contour) < 10:
        return {}
    derivative = np.diff(pitch_contour)
    threshold = np.std(derivative) * 2.5
    ornament_indices = np.where(np.abs(derivative) > threshold)[0]
    regions = []
    if len(ornament_indices) > 0:
        current = [ornament_indices[0]]
        for i in range(1, len(ornament_indices)):
            if ornament_indices[i] - ornament_indices[i-1] == 1:
                current.append(ornament_indices[i])
            else:
                regions.append(current)
                current = [ornament_indices[i]]
        regions.append(current)
    frame_time = hop_length / sr
    ornaments = {'meend': [], 'gamak': [], 'kan': [], 'andolan': []}
    for reg in regions:
        if len(reg) < 2:
            continue
        start, end = reg[0], reg[-1]
        duration = (end - start + 1) * frame_time
        pitch_range = np.max(pitch_contour[start:end+1]) - np.min(pitch_contour[start:end+1])
        if duration < 0.05:
            ornaments['kan'].append({'time': start * frame_time, 'duration': duration, 'pitch_range': float(pitch_range)})
        elif duration < 0.2:
            if pitch_range > 100:
                ornaments['gamak'].append({'time': start * frame_time, 'duration': duration, 'pitch_range': float(pitch_range)})
            else:
                ornaments['andolan'].append({'time': start * frame_time, 'duration': duration, 'pitch_range': float(pitch_range)})
        else:
            ornaments['meend'].append({
                'time': start * frame_time,
                'duration': duration,
                'pitch_range': float(pitch_range),
                'direction': 'up' if pitch_contour[end] > pitch_contour[start] else 'down'
            })
    return ornaments