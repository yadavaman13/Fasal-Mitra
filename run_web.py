#!/usr/bin/env python
"""Quick launcher for web application"""
import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    streamlit_path = Path(sys.executable).parent / "streamlit.exe"
    app_path = Path(__file__).parent / "src" / "ui" / "streamlit_app.py"
    subprocess.run([str(streamlit_path), "run", str(app_path)])
