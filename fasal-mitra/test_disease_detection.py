"""
Complete Disease Detection System Test Script
Tests backend API, ML model, and disease database
"""

import requests
import json
from pathlib import Path
import sys

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_server_health():
    """Test if server is running"""
    print_section("🏥 Testing Server Health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        data = response.json()
        print(f"✅ Server is healthy!")
        print(f"   Status: {data['status']}")
        print(f"   Environment: {data['environment']}")
        print(f"   Version: {data['version']}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Please start the backend server:")
        print("   cd fasal-mitra/server && python run.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_docs():
    """Test API documentation availability"""
    print_section("📚 Testing API Documentation")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✅ API docs available at: {BASE_URL}/docs")
            return True
        else:
            print(f"⚠️ Docs returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing docs: {e}")
        return False

def test_supported_crops():
    """Test getting supported crops"""
    print_section("🌾 Testing Supported Crops")
    try:
        response = requests.get(f"{API_URL}/disease/supported-crops", timeout=5)
        data = response.json()
        
        if data['success']:
            crops = data['data']['crops']
            total = data['data']['total']
            print(f"✅ Model supports {total} crop types:")
            print(f"   {', '.join(crops[:10])}")
            if total > 10:
                print(f"   ... and {total - 10} more")
            return True
        else:
            print(f"❌ Failed: {data.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_disease_database():
    """Test disease database"""
    print_section("🦠 Testing Disease Database")
    try:
        response = requests.get(f"{API_URL}/disease/diseases", timeout=5)
        data = response.json()
        
        if data['success']:
            diseases = data['data']
            print(f"✅ Database contains {len(diseases)} diseases")
            
            # Show a sample disease
            if diseases:
                sample = diseases[0]
                print(f"\n   Sample Disease:")
                print(f"   Name: {sample['name']}")
                print(f"   Cause: {sample['cause'][:80]}...")
                print(f"   Cure: {sample['cure'][:80]}...")
            return True
        else:
            print(f"❌ Failed: {data.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_disease_detection_with_sample():
    """Test disease detection with a sample image"""
    print_section("🔬 Testing Disease Detection (Sample Image)")
    
    # Look for any sample images
    sample_dirs = [
        Path("data/uploaded_images"),
        Path("fasal-mitra/server/uploads"),
        Path("uploads"),
    ]
    
    test_image = None
    for sample_dir in sample_dirs:
        if sample_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                images = list(sample_dir.glob(ext))
                if images:
                    test_image = images[0]
                    break
        if test_image:
            break
    
    if not test_image or not test_image.exists():
        print("⚠️ No test image found.")
        print("   To test disease detection:")
        print("   1. Download a sample plant disease image")
        print("   2. Or use the web UI at http://localhost:5173")
        return None
    
    print(f"📷 Using test image: {test_image.name}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': f}
            data = {
                'crop_type': 'Tomato',
                'location': 'Test Location'
            }
            response = requests.post(
                f"{API_URL}/disease/detect", 
                files=files, 
                data=data,
                timeout=30
            )
        
        result = response.json()
        
        if result['success']:
            detection = result['data']
            print(f"✅ Detection successful!")
            print(f"\n   🔍 Results:")
            print(f"   Disease: {detection['disease_name']}")
            print(f"   Confidence: {detection['confidence']}%")
            print(f"   Severity: {detection['severity']}")
            print(f"   Is Healthy: {detection['is_healthy']}")
            print(f"\n   💊 Treatment:")
            print(f"   {detection['treatment'][:100]}...")
            return True
        else:
            print(f"❌ Detection failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_model_loading():
    """Test if ML model can be loaded"""
    print_section("🤖 Testing ML Model")
    
    try:
        # Try to import and check model
        sys.path.insert(0, str(Path(__file__).parent / 'fasal-mitra' / 'server'))
        from app.services.ml_disease_service import MLDiseaseDetectionService
        
        print("⏳ Loading ML service (this may take 30-60 seconds on first load)...")
        service = MLDiseaseDetectionService()
        
        if service.model_loaded:
            print("✅ ML Model loaded successfully!")
            print(f"   Model type: TensorFlow/Keras")
            print(f"   Classes: {len(service.class_labels)}")
            return True
        else:
            print("⚠️ ML Model not loaded (using fallback)")
            return False
            
    except ImportError as e:
        print(f"⚠️ Cannot import ML service: {e}")
        print("   This is okay if testing via API only")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    print_section("⚛️ Checking React Frontend")
    
    frontend_urls = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
    ]
    
    for url in frontend_urls:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ Frontend is running at: {url}")
                print(f"   Open in browser to test UI")
                return True
        except:
            pass
    
    print("⚠️ Frontend not detected")
    print("   Start it with: cd fasal-mitra/client && npm run dev")
    return False

def run_all_tests():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║      🌿 Disease Detection System - Complete Test Suite       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Test server
    results['server'] = test_server_health()
    
    if not results['server']:
        print("\n❌ Cannot proceed without server running!")
        return
    
    # Test other components
    results['docs'] = test_api_docs()
    results['crops'] = test_supported_crops()
    results['database'] = test_disease_database()
    results['ml_model'] = test_ml_model_loading()
    results['detection'] = test_disease_detection_with_sample()
    results['frontend'] = check_frontend()
    
    # Summary
    print_section("📊 Test Summary")
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    print(f"\n   Total Tests: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⚠️ Skipped: {skipped}")
    
    if failed == 0:
        print("\n   🎉 All critical tests passed!")
        print("   System is ready for use!")
    elif passed >= 4:
        print("\n   ✅ System is mostly functional")
        print("   Some optional features may not be available")
    else:
        print("\n   ⚠️ System may have issues")
        print("   Check failed tests above")
    
    print("\n" + "="*60)
    print("  Next Steps:")
    print("="*60)
    print("  1. Backend:  cd fasal-mitra/server && python run.py")
    print("  2. Frontend: cd fasal-mitra/client && npm run dev")
    print("  3. Open:     http://localhost:5173")
    print("  4. API Docs: http://localhost:8000/docs")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
