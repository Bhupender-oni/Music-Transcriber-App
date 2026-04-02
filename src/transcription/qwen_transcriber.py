import numpy as np
import librosa
from typing import Dict, List, Optional
from src.config import settings

try:
    from qwen_asr.inference.qwen3_asr import Qwen3ASRModel as QwenASR, Qwen3ForcedAligner as QwenForcedAligner
    import torch
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False
    print("qwen-asr not installed; lyrics transcription disabled.")

class QwenMusicTranscriber:
    def __init__(self, model_size: str = "0.6B", device: str = None):
        self.device = device if device else settings.device
        if QWEN_AVAILABLE:
            try:
                self.asr = QwenASR.from_pretrained(f"Qwen/Qwen3-ASR-{model_size}",
                                                    device=self.device, torch_dtype=torch.float32)
                self.aligner = QwenForcedAligner.from_pretrained("Qwen/Qwen3-ForcedAligner-0.6B", device=self.device)
            except Exception as e:
                print(f"Failed to load Qwen models: {e}")
                self.asr = None
                self.aligner = None
        else:
            self.asr = None
            self.aligner = None

    def transcribe(self, audio_path: str, word_timestamps: bool = True) -> Dict:
        if not self.asr:
            return {'text': '', 'words': []}
        try:
            wav, sr = librosa.load(audio_path, sr=16000, mono=True)
            result = self.asr.transcribe(wav, sample_rate=sr, return_timestamps=True)
            if word_timestamps and self.aligner:
                alignment = self.aligner.align(wav, sr, result['text'])
                result['words'] = alignment['words']
            return result
        except Exception as e:
            print(f"Qwen error: {e}")
            return {'text': '', 'words': []}