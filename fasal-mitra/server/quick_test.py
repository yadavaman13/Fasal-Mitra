"""Quick Test: Verify TensorFlow and ML Service"""
import sys
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("QUICK TEST - TensorFlow & ML Disease Detection Service")
print("=" * 70)

# Test 1: TensorFlow
print("\n[1/5] Testing TensorFlow installation...")
try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} installed successfully!")
    
    # Check GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPU available: {len(gpus)} device(s)")
    else:
        print("ℹ️  Using CPU (no GPU detected)")
except Exception as e:
    print(f"❌ TensorFlow error: {e}")
    sys.exit(1)

# Test 2: Model file exists
print("\n[2/5] Checking model file...")
model_path = Path(__file__).parent / "app" / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
if model_path.exists():
    size_mb = model_path.stat().st_size / (1024 * 1024)
    print(f"✅ Model file found: {size_mb:.2f} MB")
else:
    print(f"❌ Model file missing: {model_path}")
    sys.exit(1)

# Test 3: Disease database exists
print("\n[3/5] Checking disease database...")
db_path = Path(__file__).parent / "app" / "data" / "plant_diseases.json"
if db_path.exists():
    import json
    with open(db_path, 'r', encoding='utf-8') as f:
        diseases = json.load(f)
    print(f"✅ Database loaded: {len(diseases)} diseases")
else:
    print(f"❌ Database missing: {db_path}")
    sys.exit(1)

# Test 4: Initialize service
print("\n[4/5] Initializing ML service...")
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    service = MLDiseaseDetectionService()
    
    if service.model_loaded:
        print(f"✅ Service initialized successfully!")
        print(f"   - Classes: {len(service.class_labels)}")
        print(f"   - Diseases: {len(service.disease_database)}")
        print(f"   - Supported crops: {len(service.get_supported_crops())}")
    else:
        print("❌ Model failed to load")
        sys.exit(1)
except Exception as e:
    print(f"❌ Service initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Sample crops
print("\n[5/5] Supported crops:")
crops = service.get_supported_crops()
for i, crop in enumerate(crops[:10], 1):
    print(f"   {i}. {crop}")
if len(crops) > 10:
    print(f"   ... and {len(crops) - 10} more")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - System is ready!")
print("=" * 70)
print("\n💡 Next steps:")
print("   1. Start server: python run.py")
print("   2. Navigate to Disease Detection page")
print("   3. Upload plant image")
print("   4. View ML-powered results")
print("\n" + "=" * 70)
