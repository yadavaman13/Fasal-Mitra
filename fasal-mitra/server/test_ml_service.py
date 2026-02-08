"""
Test script to verify ML Disease Detection Service is working
"""
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_tensorflow():
    """Test TensorFlow installation"""
    print("=" * 60)
    print("TEST 1: TensorFlow Installation")
    print("=" * 60)
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} is installed")
        
        # Check if GPU is available
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU detected: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"   - {gpu}")
        else:
            print("ℹ️  No GPU detected, using CPU")
        
        return True
    except Exception as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False

def test_service_initialization():
    """Test ML service initialization"""
    print("\n" + "=" * 60)
    print("TEST 2: ML Service Initialization")
    print("=" * 60)
    try:
        from app.services.ml_disease_service import MLDiseaseDetectionService
        
        print("Initializing ML Disease Detection Service...")
        service = MLDiseaseDetectionService()
        
        if service.model_loaded:
            print("✅ ML Model loaded successfully")
            print(f"✅ Number of disease classes: {len(service.class_labels)}")
            print(f"✅ Disease database entries: {len(service.disease_database)}")
            return True
        else:
            print("❌ Model failed to load")
            return False
            
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_path():
    """Test if model file exists"""
    print("\n" + "=" * 60)
    print("TEST 3: Model File Check")
    print("=" * 60)
    
    model_path = Path(__file__).parent / "app" / "models" / "ml" / "plant_disease_recog_model_pwp.keras"
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model file exists: {model_path}")
        print(f"✅ Model size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Model file not found: {model_path}")
        return False

def test_disease_database():
    """Test disease database"""
    print("\n" + "=" * 60)
    print("TEST 4: Disease Database Check")
    print("=" * 60)
    
    db_path = Path(__file__).parent / "app" / "data" / "plant_diseases.json"
    
    if db_path.exists():
        print(f"✅ Database file exists: {db_path}")
        
        import json
        with open(db_path, 'r', encoding='utf-8') as f:
            diseases = json.load(f)
        
        print(f"✅ Total diseases in database: {len(diseases)}")
        
        # Show first few diseases
        print("\nSample diseases:")
        for i, (key, value) in enumerate(list(diseases.items())[:3]):
            print(f"  {i+1}. {key}: {value.get('name', 'N/A')}")
        
        return True
    else:
        print(f"❌ Database file not found: {db_path}")
        return False

def test_class_labels():
    """Test class labels"""
    print("\n" + "=" * 60)
    print("TEST 5: Class Labels Check")
    print("=" * 60)
    
    try:
        from app.services.ml_disease_service import MLDiseaseDetectionService
        service = MLDiseaseDetectionService()
        
        print(f"✅ Total class labels: {len(service.class_labels)}")
        print("\nFirst 5 classes:")
        for i, label in enumerate(service.class_labels[:5]):
            print(f"  {i}. {label}")
        
        print("\nLast 5 classes:")
        for i, label in enumerate(service.class_labels[-5:], start=len(service.class_labels)-5):
            print(f"  {i}. {label}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to get class labels: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🚀 ML DISEASE DETECTION SERVICE - COMPREHENSIVE TEST")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run all tests
    results.append(("TensorFlow Installation", test_tensorflow()))
    results.append(("Model File Check", test_model_path()))
    results.append(("Disease Database Check", test_disease_database()))
    results.append(("ML Service Initialization", test_service_initialization()))
    results.append(("Class Labels Check", test_class_labels()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 SUCCESS! All systems are operational!")
        print("✅ ML Disease Detection is ready to use")
        return 0
    else:
        print(f"\n⚠️  WARNING: {total - passed} test(s) failed")
        print("Please review the errors above")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
