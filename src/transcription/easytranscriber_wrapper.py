# Wrapper for easytranscriber (forced alignment)
import numpy as np
import librosa
from typing import Dict, List

try:
    from easytranscriber import Transcriber
    EASY_AVAILABLE = True
except ImportError:
    EASY_AVAILABLE = False
    print("easytranscriber not installed; forced alignment disabled.")

class EasyTranscriberWrapper:
    def __init__(self, device: str = "cpu"):
        self.device = device
        if EASY_AVAILABLE:
            try:
                self.model = Transcriber(device=device)
            except Exception as e:
                print(f"Failed to load easytranscriber: {e}")
                self.model = None
        else:
            self.model = None

    def align(self, audio_path: str, text: str) -> List[Dict]:
        if not self.model:
            return []
        try:
            wav, sr = librosa.load(audio_path, sr=16000, mono=True)
            result = self.model.align(wav, sr, text)
            return result.get('words', [])
        except Exception as e:
            print(f"EasyTranscriber error: {e}")
            return []