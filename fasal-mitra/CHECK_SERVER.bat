@echo off
color 0E
echo.
echo ================================================================
echo          DISEASE DETECTION - SERVER CHECK
echo ================================================================
echo.

echo [Checking if backend server is running...]
echo.

REM Check if port 8000 is in use
netstat -ano | findstr ":8000" >nul 2>&1

if %ERRORLEVEL% == 0 (
    echo ================================================================
    echo                  SERVER IS RUNNING!
    echo ================================================================
    echo.
    echo Backend server is active on port 8000
    echo.
    echo API Documentation: http://localhost:8000/docs
    echo.
    echo If Disease Detection is still stuck:
    echo   1. Check browser console for errors (F12)
    echo   2. Refresh the page (Ctrl+R)
    echo   3. Try uploading the image again
    echo.
) else (
    echo ================================================================
    echo                  SERVER IS NOT RUNNING!
    echo ================================================================
    echo.
    echo This is why Disease Detection is stuck on "Analyzing..."
    echo.
    echo TO FIX: Start the backend server now!
    echo.
    echo Press any key to start the server...
    pause >nul
    echo.
    echo Starting FasalMitra Backend Server...
    echo.
    cd /d C:\Users\Aman\Desktop\ibm\fasal-mitra\server
    C:\Users\Aman\Desktop\ibm\.venv\Scripts\python.exe run.py
)

pause
