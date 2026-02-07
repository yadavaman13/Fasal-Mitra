@echo off
echo ========================================
echo   ML Disease Detection Fix Script
echo ========================================
echo.

cd /d "%~dp0"
call C:\Users\Aman\Desktop\ibm\.venv\Scripts\activate.bat

echo [Step 1] Checking Python environment...
python --version
echo.

echo [Step 2] Checking installed packages...
pip list | findstr /I "tensorflow numpy pillow"
echo.

echo [Step 3] Installing TensorFlow (this may take 5-10 minutes)...
pip install --upgrade tensorflow>=2.15.0
echo.

echo [Step 4] Verifying installation...
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
python -c "import numpy as np; print('NumPy version:', np.__version__)"
python -c "from PIL import Image; print('Pillow installed successfully')"
echo.

echo [Step 5] Testing ML service initialization...
python -c "from app.services.ml_disease_service import MLDiseaseDetectionService; s = MLDiseaseDetectionService(); print('ML Service initialized:', s.model_loaded)"
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Press any key to start the server...
pause > nul

python run.py
