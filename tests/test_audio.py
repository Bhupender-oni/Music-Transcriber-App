import unittest
import numpy as np
from src.audio import load_audio, detect_tonic, extract_pitch_contour

class TestAudio(unittest.TestCase):
    def test_load_audio(self):
        # Create dummy audio
        dummy = np.zeros(22050)
        # Would need a real file; skipping
        pass