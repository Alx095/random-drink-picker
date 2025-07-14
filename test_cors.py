#!/usr/bin/env python3
"""
Test CORS functionality more thoroughly
"""

import requests

def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

def test_cors_comprehensive():
    """Test CORS headers more comprehensively"""
    print("🌐 Testing CORS Configuration")
    print("=" * 30)
    
    BASE_URL = get_backend_url()
    
    try:
        # Test actual GET request CORS headers
        print("Testing GET request CORS headers...")
        response = requests.get(f"{BASE_URL}/api")
        
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-credentials': response.headers.get('access-control-allow-credentials'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers'),
        }
        
        print("CORS Headers on GET request:")
        for header, value in cors_headers.items():
            print(f"  {header}: {value}")
        
        # Test POST request CORS headers
        print("\nTesting POST request CORS headers...")
        data = {'test': 'data'}
        post_response = requests.post(f"{BASE_URL}/api/analyze-menu", data=data)
        
        post_cors_headers = {
            'access-control-allow-origin': post_response.headers.get('access-control-allow-origin'),
            'access-control-allow-credentials': post_response.headers.get('access-control-allow-credentials'),
        }
        
        print("CORS Headers on POST request:")
        for header, value in post_cors_headers.items():
            print(f"  {header}: {value}")
        
        # Check if CORS is working for actual requests
        if cors_headers['access-control-allow-origin'] == '*':
            print("✅ CORS is properly configured for actual requests")
            print("✅ Frontend should be able to make requests without CORS issues")
            return True
        else:
            print("❌ CORS may not be properly configured")
            return False
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

if __name__ == "__main__":
    test_cors_comprehensive()