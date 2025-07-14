#!/usr/bin/env python3
"""
Backend API Testing for Menu Drink Selector
Tests all backend endpoints with comprehensive scenarios
"""

import requests
import json
import base64
import time
import os
from io import BytesIO
from PIL import Image

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

def create_test_image_base64():
    """Create a simple test image and convert to base64"""
    # Create a simple test image with text
    img = Image.new('RGB', (400, 300), color='white')
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    
    # Convert to base64 string with data URL prefix
    base64_string = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{base64_string}"

def test_root_endpoint():
    """Test GET /api endpoint"""
    print("\n=== Testing API Root Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/api")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check CORS headers
        print(f"CORS Headers: {response.headers.get('access-control-allow-origin', 'Not found')}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('message') == 'Menu Drink Selector API':
                print("✅ API root endpoint working")
                return True
            else:
                print("❌ Unexpected response message")
                return False
        else:
            print("❌ API root endpoint failed")
            return False
    except Exception as e:
        print(f"❌ API root endpoint error: {e}")
        return False

def test_analyze_menu_endpoint():
    """Test POST /api/analyze-menu endpoint"""
    print("\n=== Testing Analyze Menu Endpoint ===")
    try:
        # Create test image
        test_image = create_test_image_base64()
        
        # Test with form data
        data = {'image_data': test_image}
        response = requests.post(f"{BASE_URL}/api/analyze-menu", data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            required_fields = ['analysis_id', 'drinks', 'total_drinks']
            
            if all(field in result for field in required_fields):
                print("✅ Analyze menu endpoint working")
                print(f"Analysis ID: {result['analysis_id']}")
                print(f"Total drinks found: {result['total_drinks']}")
                return True, result['analysis_id']
            else:
                print(f"❌ Missing required fields in response: {required_fields}")
                return False, None
        else:
            print("❌ Analyze menu endpoint failed")
            return False, None
            
    except Exception as e:
        print(f"❌ Analyze menu endpoint error: {e}")
        return False, None

def test_analyze_menu_invalid_data():
    """Test analyze menu with invalid data"""
    print("\n=== Testing Analyze Menu with Invalid Data ===")
    try:
        # Test with invalid base64
        data = {'image_data': 'invalid_base64_data'}
        response = requests.post(f"{BASE_URL}/api/analyze-menu", data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code >= 400:
            print("✅ Error handling working for invalid data")
            return True
        else:
            print("❌ Should have returned error for invalid data")
            return False
            
    except Exception as e:
        print(f"❌ Invalid data test error: {e}")
        return False

def test_random_drink_endpoint(analysis_id):
    """Test POST /api/random-drink endpoint"""
    print("\n=== Testing Random Drink Endpoint ===")
    try:
        data = {'analysis_id': analysis_id}
        response = requests.post(f"{BASE_URL}/api/random-drink", data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            required_fields = ['selected_drink', 'message']
            
            if all(field in result for field in required_fields):
                print("✅ Random drink endpoint working")
                return True
            else:
                print(f"❌ Missing required fields in response: {required_fields}")
                return False
        elif response.status_code == 404:
            print("✅ Random drink endpoint working (no drinks found - expected for test image)")
            return True
        else:
            print("❌ Random drink endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Random drink endpoint error: {e}")
        return False

def test_random_drink_invalid_id():
    """Test random drink with invalid analysis ID"""
    print("\n=== Testing Random Drink with Invalid ID ===")
    try:
        data = {'analysis_id': 'invalid-analysis-id'}
        response = requests.post(f"{BASE_URL}/api/random-drink", data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 404:
            print("✅ Error handling working for invalid analysis ID")
            return True
        else:
            print("❌ Should have returned 404 for invalid analysis ID")
            return False
            
    except Exception as e:
        print(f"❌ Invalid ID test error: {e}")
        return False

def test_get_analysis_endpoint(analysis_id):
    """Test GET /api/analysis/{analysis_id} endpoint"""
    print("\n=== Testing Get Analysis Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/api/analysis/{analysis_id}")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            required_fields = ['analysis_id', 'drinks', 'total_drinks', 'timestamp']
            
            if all(field in result for field in required_fields):
                print("✅ Get analysis endpoint working")
                return True
            else:
                print(f"❌ Missing required fields in response: {required_fields}")
                return False
        else:
            print("❌ Get analysis endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Get analysis endpoint error: {e}")
        return False

def test_get_analysis_invalid_id():
    """Test get analysis with invalid ID"""
    print("\n=== Testing Get Analysis with Invalid ID ===")
    try:
        response = requests.get(f"{BASE_URL}/api/analysis/invalid-analysis-id")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 404:
            print("✅ Error handling working for invalid analysis ID")
            return True
        else:
            print("❌ Should have returned 404 for invalid analysis ID")
            return False
            
    except Exception as e:
        print(f"❌ Invalid ID test error: {e}")
        return False

def test_cors_headers():
    """Test CORS headers on all endpoints"""
    print("\n=== Testing CORS Headers ===")
    try:
        # Test OPTIONS request
        response = requests.options(f"{BASE_URL}/api/analyze-menu")
        print(f"OPTIONS Status Code: {response.status_code}")
        
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers'),
        }
        
        print(f"CORS Headers: {cors_headers}")
        
        if cors_headers['access-control-allow-origin']:
            print("✅ CORS headers present")
            return True
        else:
            print("❌ CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def main():
    """Run all backend tests"""
    print("🚀 Starting Backend API Tests for Menu Drink Selector")
    print("=" * 60)
    
    results = []
    analysis_id = None
    
    # Test 1: API root endpoint
    results.append(("API Root Endpoint", test_root_endpoint()))
    
    # Test 2: Analyze menu endpoint
    success, analysis_id = test_analyze_menu_endpoint()
    results.append(("Analyze Menu", success))
    
    # Test 3: Analyze menu with invalid data
    results.append(("Analyze Menu (Invalid Data)", test_analyze_menu_invalid_data()))
    
    # Test 4: Random drink endpoint (only if we have analysis_id)
    if analysis_id:
        results.append(("Random Drink", test_random_drink_endpoint(analysis_id)))
        results.append(("Get Analysis", test_get_analysis_endpoint(analysis_id)))
    else:
        print("⚠️ Skipping random drink and get analysis tests - no analysis_id available")
        results.append(("Random Drink", False))
        results.append(("Get Analysis", False))
    
    # Test 5: Error handling tests
    results.append(("Random Drink (Invalid ID)", test_random_drink_invalid_id()))
    results.append(("Get Analysis (Invalid ID)", test_get_analysis_invalid_id()))
    
    # Test 6: CORS headers
    results.append(("CORS Headers", test_cors_headers()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend tests passed!")
        return True
    else:
        print("⚠️ Some backend tests failed!")
        return False

if __name__ == "__main__":
    main()