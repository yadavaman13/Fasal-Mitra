"""
Test ML Disease Service Initialization
"""
import sys
import traceback
from pathlib import Path

print("=" * 60)
print("ML Disease Service Diagnostic Test")
print("=" * 60)
print()

# Test 1: Check if TensorFlow is installed
print("Test 1: TensorFlow Installation")
print("-" * 60)
try:
    import tensorflow as tf
    print(f"✅ TensorFlow version: {tf.__version__}")
except ImportError as e:
    print(f"❌ TensorFlow not installed: {e}")
    print("   Run: pip install tensorflow>=2.15.0")
    sys.exit(1)
print()

# Test 2: Check model file existence
print("Test 2: Model File Location")
print("-" * 60)
model_path = Path(__file__).parent / "app" / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
print(f"Looking for model at: {model_path}")
if model_path.exists():
    file_size = model_path.stat().st_size / (1024 * 1024)  # Convert to MB
    print(f"✅ Model file found ({file_size:.2f} MB)")
else:
    print(f"❌ Model file NOT found!")
    print(f"   Download from: https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view")
    print(f"   Place at: {model_path}")
print()

# Test 3: Try to load the model
print("Test 3: Model Loading")
print("-" * 60)
if model_path.exists():
    try:
        print("Loading model... (this may take 10-30 seconds)")
        model = tf.keras.models.load_model(str(model_path))
        print(f"✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        traceback.print_exc()
else:
    print("⚠️  Skipping model load test (file not found)")
print()

# Test 4: Check disease database
print("Test 4: Disease Database")
print("-" * 60)
db_path = Path(__file__).parent / "app" / "data" / "plant_diseases.json"
print(f"Looking for database at: {db_path}")
if db_path.exists():
    import json
    with open(db_path, 'r') as f:
        diseases = json.load(f)
    print(f"✅ Disease database found ({len(diseases)} entries)")
else:
    print(f"❌ Disease database NOT found!")
print()

# Test 5: Try to initialize ML service
print("Test 5: ML Service Initialization")
print("-" * 60)
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    print("Initializing ML service...")
    service = MLDiseaseDetectionService()
    print(f"✅ Service initialized successfully!")
    print(f"   Model loaded: {service.model_loaded}")
    print(f"   Number of diseases: {len(service.disease_database)}")
    print(f"   Number of classes: {len(service.class_labels)}")
except Exception as e:
    print(f"❌ Service initialization failed: {e}")
    traceback.print_exc()
print()

# Test 6: Check supported crops
print("Test 6: Supported Crops")
print("-" * 60)
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    service = MLDiseaseDetectionService()
    crops = service.get_supported_crops()
    print(f"✅ Supported crops ({len(crops)}):")
    for crop in sorted(crops):
        print(f"   - {crop}")
except Exception as e:
    print(f"❌ Error getting supported crops: {e}")
print()

print("=" * 60)
print("Diagnostic Test Complete")
print("=" * 60)
