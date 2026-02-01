#!/usr/bin/env python
"""Quick launcher for console application"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.console_app import main

if __name__ == "__main__":
    main()
