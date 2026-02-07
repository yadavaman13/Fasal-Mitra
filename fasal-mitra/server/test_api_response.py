"""
Quick test to verify the disease detection API is responding correctly
"""

import requests
import json

# Test the detect endpoint with a simple request
API_URL = "http://localhost:8000/api/v1/disease/detect"

# Create a minimal test (you'll need a real image for full test)
print("Testing Disease Detection API...")
print(f"Endpoint: {API_URL}")
print("-" * 50)

try:
    # Test if server is running by hitting a simpler endpoint first
    health_check = requests.get("http://localhost:8000/api/v1/disease/supported-crops", timeout=5)
    print(f"Server Status: {health_check.status_code}")
    
    if health_check.status_code == 200:
        data = health_check.json()
        print(f"✅ Server is running!")
        print(f"Response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Server returned error: {health_check.status_code}")
        print(f"Response: {health_check.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Make sure uvicorn is running on port 8000")
except Exception as e:
    print(f"❌ Error: {e}")

print("\nTo fully test disease detection:")
print("1. Make sure the backend server is running")
print("2. Upload an image through the web interface")
print("3. Check browser console for any errors")
