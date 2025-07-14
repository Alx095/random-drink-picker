#!/usr/bin/env python3
"""
Test MongoDB integration and data persistence
"""

import requests
import json

def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

def test_mongodb_persistence():
    """Test that data is properly stored and retrieved from MongoDB"""
    print("🗄️ Testing MongoDB Integration and Data Persistence")
    print("=" * 55)
    
    BASE_URL = get_backend_url()
    
    try:
        # Get the analysis we just created
        analysis_id = "5c5a62bd-9b49-47f8-9265-6543b06efa57"  # From previous test
        
        print(f"Testing retrieval of analysis: {analysis_id}")
        
        response = requests.get(f"{BASE_URL}/api/analysis/{analysis_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully retrieved analysis from MongoDB")
            print(f"Analysis ID: {result['analysis_id']}")
            print(f"Total drinks: {result['total_drinks']}")
            print(f"Timestamp: {result['timestamp']}")
            print(f"First few drinks: {[d['name'] for d in result['drinks'][:3]]}")
            
            # Verify data integrity
            if (result['analysis_id'] == analysis_id and 
                result['total_drinks'] == 10 and
                len(result['drinks']) == 10):
                print("✅ Data integrity verified - all fields match expected values")
                return True
            else:
                print("❌ Data integrity issue - values don't match expected")
                return False
        else:
            print(f"❌ Failed to retrieve analysis: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_persistence()