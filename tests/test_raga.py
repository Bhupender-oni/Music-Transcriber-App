import unittest
from src.models import RagaIdentifier

class TestRaga(unittest.TestCase):
    def test_raga_identifier(self):
        ident = RagaIdentifier()
        self.assertIsNotNone(ident)