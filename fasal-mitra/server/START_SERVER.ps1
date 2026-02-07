# FasalMitra Backend Server Startup Script
Write-Host "========================================" -ForegroundColor Green
Write-Host "   FasalMitra Backend Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server with fixed datetime serialization..." -ForegroundColor Yellow
Write-Host ""

# Navigate to server directory
Set-Location -Path $PSScriptRoot

# Activate virtual environment
& "C:\Users\Aman\Desktop\ibm\.venv\Scripts\Activate.ps1"

# Start the server
python run.py
