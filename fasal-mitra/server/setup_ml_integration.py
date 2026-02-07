"""
Quick Setup Script for Disease Detection ML Integration

Run this after downloading the model file.
"""

import subprocess
import sys
from pathlib import Path


def main():
    print("🌾 FasalMitra - Disease Detection ML Integration Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    server_dir = Path(__file__).parent
    required_files = [
        server_dir / "requirements.txt",
        server_dir / "app" / "services" / "ml_disease_service.py",
        server_dir / "app" / "data" / "plant_diseases.json"
    ]
    
    print("\n1️⃣  Checking directory structure...")
    all_exist = True
    for file in required_files:
        if file.exists():
            print(f"   ✅ {file.name}")
        else:
            print(f"   ❌ {file.name} - NOT FOUND!")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing. Please check setup.")
        return False
    
    # Check if model file exists
    model_path = server_dir / "app" / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
    print("\n2️⃣  Checking ML model...")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ Model file found ({size_mb:.1f}MB)")
    else:
        print(f"   ⚠️  Model file NOT found at:")
        print(f"      {model_path}")
        print(f"\n   📥 Download from: https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view?usp=sharing")
        print(f"   📁 Place in: app/models/ml/")
        print(f"\n   Note: Server will still work with fallback mode")
    
    # Check if TensorFlow is installed
    print("\n3️⃣  Checking TensorFlow installation...")
    try:
        import tensorflow as tf
        print(f"   ✅ TensorFlow {tf.__version__} installed")
    except ImportError:
        print("   ❌ TensorFlow not installed")
        print("\n   Installing TensorFlow...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "tensorflow>=2.15.0"
            ])
            print("   ✅ TensorFlow installed successfully!")
        except subprocess.CalledProcessError:
            print("   ❌ Failed to install TensorFlow")
            print("   🔧 Try manually: pip install tensorflow>=2.15.0")
            return False
    
    # Check other dependencies
    print("\n4️⃣  Checking other dependencies...")
    missing = []
    required_packages = [
        ("PIL", "Pillow"),
        ("numpy", "numpy"),
        ("fastapi", "fastapi"),
    ]
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - NOT INSTALLED")
            missing.append(package_name)
    
    if missing:
        print(f"\n   Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", *missing
            ])
            print("   ✅ Missing packages installed!")
        except subprocess.CalledProcessError:
            print("   ❌ Failed to install packages")
            print("   🔧 Try manually: pip install -r requirements.txt")
            return False
    
    # Final checks
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("\n📝 Next Steps:")
    
    if not model_path.exists():
        print("   1. Download the ML model from Google Drive")
        print("   2. Place it in: app/models/ml/")
        print("   3. Restart the server")
    else:
        print("   1. Start the server: uvicorn app.main:app --reload")
        print("   2. Test at: http://localhost:8000/docs")
        print("   3. Try disease detection endpoint!")
    
    print("\n🌾 Happy Farming!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
