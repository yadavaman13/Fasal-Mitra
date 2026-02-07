"""
Comprehensive ML Disease Detection Test
Tests the complete disease detection pipeline
"""
import sys
import requests
from pathlib import Path
import json

print("="*70)
print("COMPREHENSIVE DISEASE DETECTION TEST")
print("="*70)
print()

# Test 1: ML Service Direct Test
print("[TEST 1] ML Service Initialization")
print("-"*70)
try:
    from app.services.ml_disease_service import MLDiseaseDetectionService
    service = MLDiseaseDetectionService()
    print(f"✅ Service initialized successfully")
    print(f"   Model loaded: {service.model_loaded}")
    print(f"   Classes: {len(service.class_labels)}")
    print(f"   Diseases in DB: {len(service.disease_database)}")
except Exception as e:
    print(f"❌ Service initialization failed: {e}")
    sys.exit(1)
print()

# Test 2: Check model can predict
print("[TEST 2] Model Prediction Test")
print("-"*70)
try:
    import numpy as np
    from PIL import Image
    import io
    
    # Create a test image (random 160x160 RGB)
    test_image = np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
    pil_image = Image.fromarray(test_image)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    print("Testing with random image...")
    result = service.detect_disease(
        image_data=img_bytes,
        crop_type="Corn",
        location="Test Location"
    )
    
    # This is async, so we need to handle it
    import asyncio
    result = asyncio.run(result)
    
    print(f"✅ Detection completed")
    print(f"   Disease: {result.get('disease_name', 'N/A')}")
    print(f"   Confidence: {result.get('confidence', 0)}%")
    print(f"   Severity: {result.get('severity', 'N/A')}")
    print(f"   Model used: {result.get('model_used', 'N/A')}")
except Exception as e:
    print(f"❌ Detection failed: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 3: Check API Server
print("[TEST 3] API Server Health Check")
print("-"*70)
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print(f"✅ Server is responding")
        print(f"   Status: {response.json()}")
    else:
        print(f"⚠️  Server responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Cannot connect to server on port 8000")
    print(f"   Start server with: python run.py")
except Exception as e:
    print(f"❌ Error: {e}")
print()

# Test 4: Check Disease Detection Endpoint
print("[TEST 4] Disease Detection API Endpoint")
print("-"*70)
try:
    # Check if we have a test image
    test_image_path = Path("../Plant-Disease-Recognition-System-main/Plant-Disease-Recognition-System-main/static/images/Apple_tree_leaf.jpg")
    
    if test_image_path.exists():
        print(f"Using test image: {test_image_path.name}")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': (test_image_path.name, f, 'image/jpeg')}
            data = {'crop_type': 'Apple', 'location': 'Test'}
            
            response = requests.post(
                "http://localhost:8000/api/v1/disease/detect",
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Detection API working")
                print(f"   Success: {result.get('success')}")
                if result.get('success'):
                    data = result.get('data', {})
                    print(f"   Disease: {data.get('disease_name', 'N/A')}")
                    print(f"   Confidence: {data.get('confidence', 0)}%")
                    print(f"   Severity: {data.get('severity', 'N/A')}")
                    print(f"   Is Healthy: {data.get('is_healthy', False)}")
                else:
                    print(f"   Message: {result.get('message')}")
            else:
                print(f"❌ API returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
    else:
        print(f"ℹ️  No test image found at {test_image_path}")
        print(f"   Upload an image through the web interface to test")
        
except requests.exceptions.ConnectionError:
    print(f"❌ Cannot connect to server")
    print(f"   Make sure server is running: python run.py")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 5: Supported Crops
print("[TEST 5] Supported Crops Endpoint")
print("-"*70)
try:
    response = requests.get("http://localhost:8000/api/v1/disease/supported-crops", timeout=5)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            crops = result.get('data', {}).get('crops', [])
            print(f"✅ Supported crops endpoint working")
            print(f"   Total crops: {len(crops)}")
            print(f"   Crops: {', '.join(crops)}")
        else:
            print(f"⚠️  API returned success=False")
    else:
        print(f"❌ API returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Server not running")
except Exception as e:
    print(f"❌ Error: {e}")
print()

print("="*70)
print("TEST SUMMARY")
print("="*70)
print()
print("If all tests passed:")
print("1. ✅ ML Service is working")
print("2. ✅ Model loads and can predict")
print("3. ✅ API server is running")
print("4. ✅ Disease detection endpoint works")
print("5. ✅ Frontend should work correctly")
print()
print("Next steps:")
print("- Open http://localhost:5173/disease-detection")
print("- Upload a plant image")
print("- Click 'Analyze Disease'")
print("- Results should appear within 2-5 seconds")
print()
