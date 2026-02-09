#!/usr/bin/env python
"""
Run script for Fasal Mitra server with Python 3.12 and TensorFlow support
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the server using Python 3.12 for TensorFlow compatibility"""
    server_dir = Path(__file__).parent
    os.chdir(server_dir)
    
    # Use Python 3.12 specifically for TensorFlow compatibility
    try:
        # Try py -3.12 first (Windows Python Launcher)
        result = subprocess.run([
            "py", "-3.12", "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to python3.12 command
            result = subprocess.run([
                "python3.12", "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000", 
                "--reload"
            ], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Error: Python 3.12 not found!")
            print("Please install Python 3.12 for TensorFlow compatibility.")
            print("Current Python versions available:")
            try:
                subprocess.run(["py", "-0"], check=False)
            except FileNotFoundError:
                pass
            sys.exit(1)

if __name__ == "__main__":
    main()