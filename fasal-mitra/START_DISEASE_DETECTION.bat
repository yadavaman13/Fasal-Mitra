@echo off
echo ===============================================
echo    Disease Detection System - Quick Start
echo ===============================================
echo.

echo [1/4] Checking Python environment...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo [2/4] Testing backend server...
cd fasal-mitra\server
python -c "from app.services.ml_disease_service import MLDiseaseDetectionService; print('✅ ML Service OK')"
if errorlevel 1 (
    echo ERROR: Backend dependencies not installed!
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [3/4] Starting backend server...
echo Backend will run at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
start "FasalMitra Backend" cmd /k "cd fasal-mitra\server && python run.py"

timeout /t 5 /nobreak

echo.
echo [4/4] Starting frontend...
echo Frontend will run at: http://localhost:5173
echo.
cd ..\client
start "FasalMitra Frontend" cmd /k "npm run dev"

timeout /t 3 /nobreak

echo.
echo ===============================================
echo    System Started Successfully!
echo ===============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open frontend in browser...
pause > nul

start http://localhost:5173

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
