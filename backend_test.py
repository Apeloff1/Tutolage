#!/usr/bin/env python3
"""
CodeDock v11.6 MASSIVE EXPANSION Backend API Testing
Testing all new Educational Academy and SOTA Extended Features

New Features to Test:
1. Physics Engine - GET /api/physics/info
2. Math Engine - GET /api/math/info  
3. CS Engine - GET /api/cs/info
4. Hybrid Pipeline - GET /api/hybrid/info
5. SOTA Extended - GET /api/sota-extended/info
6. Jeeves Knowledge Base - GET /api/jeeves/knowledge-base

Plus additional endpoints for comprehensive testing.
"""

import requests
import json
import sys
from datetime import datetime

# Base URL from frontend environment
BASE_URL = "https://codedock-sota-v116.preview.emergentagent.com/api"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        print(f"🔍 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            try:
                json_data = response.json()
                print(f"   ✅ SUCCESS - Response length: {len(str(json_data))} chars")
                
                # Print key information for verification
                if "name" in json_data:
                    print(f"   📋 Name: {json_data['name']}")
                if "version" in json_data:
                    print(f"   📋 Version: {json_data['version']}")
                if "total_hours" in json_data:
                    print(f"   📋 Total Hours: {json_data['total_hours']}")
                if "categories" in json_data:
                    print(f"   📋 Categories: {len(json_data['categories'])} found")
                if "features" in json_data:
                    print(f"   📋 Features: {len(json_data['features'])} found")
                if "capabilities" in json_data:
                    print(f"   📋 Capabilities: {len(json_data['capabilities'])} found")
                if "genres_supported" in json_data:
                    print(f"   📋 Genres: {len(json_data['genres_supported'])} supported")
                if "total_upgrades" in json_data:
                    print(f"   📋 Total Upgrades: {json_data['total_upgrades']}")
                if "subjects" in json_data:
                    print(f"   📋 Subjects: {list(json_data['subjects'].keys())}")
                    
                return True
            except json.JSONDecodeError:
                print(f"   ❌ FAILED - Invalid JSON response")
                return False
        else:
            print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
            try:
                error_data = response.json()
                print(f"   📋 Error: {error_data}")
            except:
                print(f"   📋 Raw response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED - Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ FAILED - Unexpected error: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("🚀 CODEDOCK v11.6 MASSIVE EXPANSION - BACKEND API TESTING")
    print("=" * 80)
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test results tracking
    tests_passed = 0
    tests_total = 0
    failed_tests = []
    
    # ========================================================================
    # CORE v11.6 FEATURES TESTING
    # ========================================================================
    
    print("📚 TESTING NEW EDUCATIONAL ENGINES")
    print("-" * 50)
    
    # 1. Physics Engine
    tests_total += 1
    if test_endpoint("GET", "/physics/info"):
        tests_passed += 1
    else:
        failed_tests.append("Physics Engine - GET /api/physics/info")
    
    tests_total += 1
    if test_endpoint("GET", "/physics/curriculum"):
        tests_passed += 1
    else:
        failed_tests.append("Physics Engine - GET /api/physics/curriculum")
        
    tests_total += 1
    if test_endpoint("GET", "/physics/simulations"):
        tests_passed += 1
    else:
        failed_tests.append("Physics Engine - GET /api/physics/simulations")
    
    print()
    
    # 2. Math Engine
    tests_total += 1
    if test_endpoint("GET", "/math/info"):
        tests_passed += 1
    else:
        failed_tests.append("Math Engine - GET /api/math/info")
        
    tests_total += 1
    if test_endpoint("GET", "/math/curriculum"):
        tests_passed += 1
    else:
        failed_tests.append("Math Engine - GET /api/math/curriculum")
        
    # Test math visualizations (if endpoint exists)
    tests_total += 1
    if test_endpoint("GET", "/math/formulas/vectors"):
        tests_passed += 1
    else:
        failed_tests.append("Math Engine - GET /api/math/formulas/vectors")
    
    print()
    
    # 3. CS Engine
    tests_total += 1
    if test_endpoint("GET", "/cs/info"):
        tests_passed += 1
    else:
        failed_tests.append("CS Engine - GET /api/cs/info")
        
    tests_total += 1
    if test_endpoint("GET", "/cs/curriculum"):
        tests_passed += 1
    else:
        failed_tests.append("CS Engine - GET /api/cs/curriculum")
        
    tests_total += 1
    if test_endpoint("GET", "/cs/implementations/algorithms"):
        tests_passed += 1
    else:
        failed_tests.append("CS Engine - GET /api/cs/implementations/algorithms")
    
    print()
    
    # 4. Hybrid Pipeline
    print("🔄 TESTING HYBRID PIPELINE")
    print("-" * 50)
    
    tests_total += 1
    if test_endpoint("GET", "/hybrid/info"):
        tests_passed += 1
    else:
        failed_tests.append("Hybrid Pipeline - GET /api/hybrid/info")
        
    # Test game generation
    game_concept = {
        "concept": "A magical forest adventure where players collect mystical crystals",
        "genre": "action_rpg",
        "style": "fantasy",
        "scope": "demo"
    }
    tests_total += 1
    if test_endpoint("POST", "/hybrid/generate", game_concept):
        tests_passed += 1
    else:
        failed_tests.append("Hybrid Pipeline - POST /api/hybrid/generate")
    
    print()
    
    # 5. SOTA Extended
    print("🔬 TESTING SOTA EXTENDED FEATURES")
    print("-" * 50)
    
    tests_total += 1
    if test_endpoint("GET", "/sota-extended/info"):
        tests_passed += 1
    else:
        failed_tests.append("SOTA Extended - GET /api/sota-extended/info")
        
    tests_total += 1
    if test_endpoint("GET", "/sota-extended/upgrades"):
        tests_passed += 1
    else:
        failed_tests.append("SOTA Extended - GET /api/sota-extended/upgrades")
        
    # Test applying an upgrade
    tests_total += 1
    if test_endpoint("POST", "/sota-extended/apply/predictive_v2", {"config": {"enabled": True}}):
        tests_passed += 1
    else:
        failed_tests.append("SOTA Extended - POST /api/sota-extended/apply/predictive_v2")
    
    print()
    
    # 6. Jeeves Enhanced
    print("🎩 TESTING JEEVES AI TUTOR ENHANCED")
    print("-" * 50)
    
    tests_total += 1
    if test_endpoint("GET", "/jeeves/knowledge-base"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Knowledge Base - GET /api/jeeves/knowledge-base")
        
    # Test physics teaching (using query parameters)
    tests_total += 1
    if test_endpoint("POST", "/jeeves/teach-physics?topic=collision%20detection&skill_level=intermediate&include_simulation=true&game_context=2D%20platformer%20game"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Tutor - POST /api/jeeves/teach-physics")
        
    # Test math teaching (using query parameters)
    tests_total += 1
    if test_endpoint("POST", "/jeeves/teach-math?topic=vectors&skill_level=beginner&include_visualization=true&game_context=3D%20game%20development"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Tutor - POST /api/jeeves/teach-math")
        
    # Test CS teaching (using query parameters)
    tests_total += 1
    if test_endpoint("POST", "/jeeves/teach-cs?topic=pathfinding&skill_level=intermediate&include_complexity=true&language=python"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Tutor - POST /api/jeeves/teach-cs")
        
    # Test general game dev Q&A (using query parameters)
    tests_total += 1
    if test_endpoint("POST", "/jeeves/game-dev-qa?question=How%20do%20I%20implement%20A*%20pathfinding%20in%20Unity?&category=cs&skill_level=intermediate&include_code=true"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Tutor - POST /api/jeeves/game-dev-qa")
        
    # Test personalized study path
    tests_total += 1
    if test_endpoint("GET", "/jeeves/study-path/build-a-3d-game-engine"):
        tests_passed += 1
    else:
        failed_tests.append("Jeeves Tutor - GET /api/jeeves/study-path/build-a-3d-game-engine")
    
    print()
    
    # ========================================================================
    # VERIFICATION TESTS - Existing APIs
    # ========================================================================
    
    print("✅ VERIFICATION - EXISTING APIs")
    print("-" * 50)
    
    # Health check
    tests_total += 1
    if test_endpoint("GET", "/health"):
        tests_passed += 1
    else:
        failed_tests.append("Health Check - GET /api/health")
    
    # Languages
    tests_total += 1
    if test_endpoint("GET", "/languages"):
        tests_passed += 1
    else:
        failed_tests.append("Languages - GET /api/languages")
    
    # Code execution
    code_test = {
        "language": "python",
        "code": "print('CodeDock v11.6 Testing!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')"
    }
    tests_total += 1
    if test_endpoint("POST", "/execute", code_test):
        tests_passed += 1
    else:
        failed_tests.append("Code Execution - POST /api/execute")
    
    print()
    
    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    
    print("=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    
    success_rate = (tests_passed / tests_total) * 100 if tests_total > 0 else 0
    
    print(f"✅ Tests Passed: {tests_passed}/{tests_total}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
        for i, test in enumerate(failed_tests, 1):
            print(f"   {i}. {test}")
    else:
        print(f"\n🎉 ALL TESTS PASSED! CodeDock v11.6 is fully operational!")
    
    print("\n" + "=" * 80)
    
    # Return success status
    return len(failed_tests) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)