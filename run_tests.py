#!/usr/bin/env python
"""Quick launcher for running tests"""
import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    test_file = Path(__file__).parent / "tests" / "test_system.py"
    subprocess.run([sys.executable, str(test_file)])
