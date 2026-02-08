@echo off
echo ============================================================
echo Testing TensorFlow Installation and ML Service
echo ============================================================
echo.

cd /d C:\Users\Aman\Desktop\ibm\fasal-mitra\server

echo [1/3] Testing TensorFlow...
C:\Users\Aman\Desktop\ibm\.venv\Scripts\python.exe -c "import tensorflow as tf; print('SUCCESS: TensorFlow', tf.__version__, 'is installed')"

echo.
echo [2/3] Running comprehensive ML service tests...
C:\Users\Aman\Desktop\ibm\.venv\Scripts\python.exe test_ml_service.py

echo.
echo [3/3] Done!
pause
