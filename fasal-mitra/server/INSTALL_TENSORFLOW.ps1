# Install TensorFlow and verify
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Installing TensorFlow" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Yellow
& "C:\Users\Aman\Desktop\ibm\.venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "[2/5] Checking Python version..." -ForegroundColor Yellow
python --version
Write-Host ""

# Install TensorFlow
Write-Host "[3/5] Installing TensorFlow (this may take 5-10 minutes)..." -ForegroundColor Yellow
Write-Host "Please wait..." -ForegroundColor Gray
pip install --upgrade tensorflow>=2.15.0
Write-Host ""

# Verify installation
Write-Host "[4/5] Verifying TensorFlow installation..." -ForegroundColor Yellow
python -c "import tensorflow as tf; print('✅ TensorFlow version:', tf.__version__)"
Write-Host ""

# Test ML service
Write-Host "[5/5] Testing ML Disease Service..." -ForegroundColor Yellow
Set-Location -Path "C:\Users\Aman\Desktop\ibm\fasal-mitra\server"
python -c "from app.services.ml_disease_service import MLDiseaseDetectionService; s = MLDiseaseDetectionService(); print('✅ ML Service Model Loaded:', s.model_loaded)"
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "   Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: Start the server with:" -ForegroundColor Cyan
Write-Host "  python run.py" -ForegroundColor White
Write-Host ""
