import os
import numpy as np
import librosa
from typing import Dict, List

try:
    from easytranscriber.pipelines import pipeline as transcriber_pipeline
    EASY_AVAILABLE = True
except ImportError:
    EASY_AVAILABLE = False
    print("easytranscriber not installed; forced alignment disabled.")

class EasyTranscriberWrapper:
    def __init__(self, device: str = "cpu"):
        self.model = None
        if EASY_AVAILABLE:
            # Transcriber class was removed in v0.2.0; we indicate availability here.
            self.model = True
            print("easytranscriber pipeline is available.")

    def align(self, audio_path: str, text: str) -> List[Dict]:
        if not self.model:
            return []
        try:
            # Using the new pipeline API for forced alignment.
            result = transcriber_pipeline(
                audio_paths=[os.path.basename(audio_path)],
                audio_dir=os.path.dirname(audio_path),
                return_alignments=True
            )
            if result and len(result) > 0:
                # result is list[list[SpeechSegment]]; mapping segments to dicts.
                return [segment.__dict__ for segment in result[0]]
            return []
        except Exception as e:
            print(f"EasyTranscriber error: {e}")
            return []