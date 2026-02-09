@echo off
echo ========================================
echo   FasalMitra Backend Server
echo ========================================
echo.
echo Starting server with fixed datetime serialization...
echo.

cd /d "%~dp0"
call C:\Users\Aman\Desktop\ibm\.venv\Scripts\activate.bat
python run.py

pause
