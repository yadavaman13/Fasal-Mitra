"""
Test script for Disease Detection ML Integration

Verifies that all components are properly integrated without requiring TensorFlow
to be installed (useful for CI/CD).
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all necessary modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.services.ml_disease_service import MLDiseaseDetectionService
        print("  ✅ MLDiseaseDetectionService imported")
    except ImportError as e:
        print(f"  ❌ Failed to import MLDiseaseDetectionService: {e}")
        return False
    
    try:
        from app.api.v1.endpoints.disease_detection import router
        print("  ✅ Disease detection API router imported")
    except ImportError as e:
        print(f"  ❌ Failed to import disease detection router: {e}")
        return False
    
    return True


def test_disease_database():
    """Test that disease database can be loaded"""
    print("\nTesting disease database...")
    
    try:
        import json
        from pathlib import Path
        
        db_path = Path(__file__).parent / "app" / "data" / "plant_diseases.json"
        
        if not db_path.exists():
            print(f"  ❌ Disease database not found at {db_path}")
            return False
        
        with open(db_path, 'r', encoding='utf-8') as f:
            diseases = json.load(f)
        
        if not isinstance(diseases, list):
            print("  ❌ Disease database is not a list")
            return False
        
        if len(diseases) != 39:
            print(f"  ⚠️  Expected 39 diseases, found {len(diseases)}")
        
        print(f"  ✅ Disease database loaded: {len(diseases)} diseases")
        
        # Verify structure
        sample = diseases[0]
        required_keys = ['name', 'cause', 'cure']
        for key in required_keys:
            if key not in sample:
                print(f"  ❌ Disease entry missing key: {key}")
                return False
        
        print("  ✅ Disease database structure valid")
        return True
    
    except Exception as e:
        print(f"  ❌ Error loading disease database: {e}")
        return False


def test_model_path():
    """Test that model directory exists"""
    print("\nTesting model path...")
    
    model_dir = Path(__file__).parent / "app" / "models" / "ml"
    
    if not model_dir.exists():
        print(f"  ❌ Model directory does not exist: {model_dir}")
        return False
    
    print(f"  ✅ Model directory exists: {model_dir}")
    
    model_file = model_dir / "plant_disease_recog_model_pwp.keras"
    
    if model_file.exists():
        size_mb = model_file.stat().st_size / (1024 * 1024)
        print(f"  ✅ Model file found ({size_mb:.1f}MB)")
    else:
        print(f"  ⚠️  Model file not found (expected for initial setup)")
        print(f"     Download from Google Drive and place in: {model_dir}")
    
    readme = model_dir / "README.md"
    if readme.exists():
        print(f"  ✅ Model README exists")
    else:
        print(f"  ❌ Model README missing")
        return False
    
    return True


def test_api_endpoints():
    """Test that API endpoints are properly configured"""
    print("\nTesting API endpoints...")
    
    try:
        from app.api.v1.endpoints import disease_detection
        
        # Check that router has the expected endpoints
        routes = [route.path for route in disease_detection.router.routes]
        
        expected_routes = ['/detect', '/diseases', '/supported-crops', '/history']
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ Endpoint {route} registered")
            else:
                print(f"  ❌ Endpoint {route} not found")
                return False
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error testing endpoints: {e}")
        return False


def test_service_initialization():
    """Test that service can be initialized without TensorFlow"""
    print("\nTesting service initialization...")
    
    try:
        from app.services.ml_disease_service import MLDiseaseDetectionService
        
        # This should work even without TensorFlow
        service = MLDiseaseDetectionService()
        
        print("  ✅ Service initialized")
        
        # Test methods that don't require model
        crops = service.get_supported_crops()
        print(f"  ✅ Supported crops: {len(crops)} crops")
        
        diseases = service.get_all_diseases()
        print(f"  ✅ Disease database: {len(diseases)} diseases")
        
        # Test class labels
        if len(service.class_labels) == 39:
            print(f"  ✅ Class labels: {len(service.class_labels)} classes")
        else:
            print(f"  ❌ Expected 39 class labels, got {len(service.class_labels)}")
            return False
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error initializing service: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Disease Detection ML Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Disease Database", test_disease_database),
        ("Model Path", test_model_path),
        ("API Endpoints", test_api_endpoints),
        ("Service Initialization", test_service_initialization),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Integration is ready.")
        print("\n📝 Next steps:")
        print("   1. Install TensorFlow: pip install tensorflow>=2.15.0")
        print("   2. Download model file and place in app/models/ml/")
        print("   3. Start server: uvicorn app.main:app --reload")
        return True
    else:
        print("\n❌ Some tests failed. Please review errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
