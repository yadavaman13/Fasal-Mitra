@echo off
color 0A
echo.
echo ================================================================
echo          DISEASE DETECTION - QUICK START GUIDE
echo ================================================================
echo.
echo [Step 1] Testing System...
echo.
cd /d C:\Users\Aman\Desktop\ibm\fasal-mitra\server
echo Running verification tests...
C:\Users\Aman\Desktop\ibm\.venv\Scripts\python.exe quick_test.py
if %ERRORLEVEL% == 0 (
    echo.
    echo ================================================================
    echo                  ALL TESTS PASSED!
    echo ================================================================
    echo.
    echo [Step 2] Ready to start server!
    echo.
    echo To start the backend server, run:
    echo.
    echo   cd fasal-mitra\server
    echo   python run.py
    echo.
    echo Then open: http://localhost:8000/docs
    echo.
    echo For full system:
    echo   Terminal 1: python run.py (backend)
    echo   Terminal 2: npm run dev (frontend - in client folder)
    echo.
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo                  TESTS FAILED
    echo ================================================================
    echo.
    echo Please check the error messages above.
    echo.
)
echo.
pause
