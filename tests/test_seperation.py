import unittest
from src.separation import DemucsSeparator

class TestSeparation(unittest.TestCase):
    def test_separator_init(self):
        sep = DemucsSeparator(device="cpu")
        self.assertIsNotNone(sep)