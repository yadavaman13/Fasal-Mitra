#!/usr/bin/env python
"""Quick launcher for Gujarat analysis"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Run Gujarat analysis
import subprocess
subprocess.run([sys.executable, str(Path(__file__).parent / "tests" / "test_gujarat_data.py")])
