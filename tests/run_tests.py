#!/usr/bin/env python
"""
Test runner for Music Transcriber project
Run from project root: python tests/run_tests.py
"""
import unittest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def discover_and_run_tests():
    """Discover and run all tests in tests directory"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(discover_and_run_tests())
