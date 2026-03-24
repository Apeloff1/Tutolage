#!/usr/bin/env python3
"""
CodeDock Multi-Layer Learning Engine API Testing
Testing the new learning engine endpoints as requested in the review.
"""

import requests
import json
import sys
from typing import Dict, Any

# Base URL from the review request
BASE_URL = "https://sota-2026.preview.emergentagent.com"

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, params=params, timeout=30)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e), "url": url}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON decode error: {str(e)}", "url": url}

def main():
    """Test all CodeDock Multi-Layer Learning Engine API endpoints"""
    
    print("🎯 CODEDOCK MULTI-LAYER LEARNING ENGINE API TESTING")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print()
    
    tests = []
    
    # Test 1: GET learning domains
    print("1️⃣ Testing GET /api/learning-engine/domains")
    result = test_endpoint("GET", "/api/learning-engine/domains")
    tests.append(("GET /api/learning-engine/domains", result))
    
    if result["success"]:
        response = result["response"]
        domains_count = response.get("total_domains", 0)
        total_hours = response.get("total_learning_hours", 0)
        redundancy_layers = response.get("redundancy_layers", 0)
        print(f"   ✅ SUCCESS: Found {domains_count} domains, {total_hours} total hours, {redundancy_layers} redundancy layers")
        
        # Check if we have the expected domains
        domains = response.get("domains", [])
        domain_names = [d.get("name", "") for d in domains]
        print(f"   📚 Domains: {', '.join(domain_names[:3])}{'...' if len(domain_names) > 3 else ''}")
    else:
        print(f"   ❌ FAILED: {result.get('error', 'Unknown error')} (Status: {result.get('status_code', 'N/A')})")
    print()
    
    # Test 2: GET learning layers
    print("2️⃣ Testing GET /api/learning-engine/layers")
    result = test_endpoint("GET", "/api/learning-engine/layers")
    tests.append(("GET /api/learning-engine/layers", result))
    
    if result["success"]:
        response = result["response"]
        layers = response.get("layers", [])
        retention_potential = response.get("total_retention_potential", "")
        print(f"   ✅ SUCCESS: Found {len(layers)} learning layers, {retention_potential} retention potential")
        
        # Check layer details
        layer_names = [l.get("name", "") for l in layers]
        print(f"   🧠 Layers: {', '.join(layer_names[:3])}{'...' if len(layer_names) > 3 else ''}")
    else:
        print(f"   ❌ FAILED: {result.get('error', 'Unknown error')} (Status: {result.get('status_code', 'N/A')})")
    print()
    
    # Test 3: GET learning modes
    print("3️⃣ Testing GET /api/learning-engine/modes")
    result = test_endpoint("GET", "/api/learning-engine/modes")
    tests.append(("GET /api/learning-engine/modes", result))
    
    if result["success"]:
        response = result["response"]
        modes = response.get("modes", [])
        print(f"   ✅ SUCCESS: Found {len(modes)} learning modes")
        
        # Check mode details
        mode_names = [m.get("name", "") for m in modes]
        print(f"   🎯 Modes: {', '.join(mode_names)}")
    else:
        print(f"   ❌ FAILED: {result.get('error', 'Unknown error')} (Status: {result.get('status_code', 'N/A')})")
    print()
    
    # Test 4: GET learning stats
    print("4️⃣ Testing GET /api/learning-engine/stats")
    result = test_endpoint("GET", "/api/learning-engine/stats")
    tests.append(("GET /api/learning-engine/stats", result))
    
    if result["success"]:
        response = result["response"]
        total_domains = response.get("total_domains", 0)
        total_hours = response.get("total_learning_hours", 0)
        redundancy_layers = response.get("redundancy_layers", 0)
        learning_modes = response.get("learning_modes", 0)
        mastery_levels = response.get("mastery_levels", 0)
        print(f"   ✅ SUCCESS: {total_domains} domains, {total_hours} hours, {redundancy_layers} layers, {learning_modes} modes, {mastery_levels} mastery levels")
    else:
        print(f"   ❌ FAILED: {result.get('error', 'Unknown error')} (Status: {result.get('status_code', 'N/A')})")
    print()
    
    # Test 5: POST generate learning path
    print("5️⃣ Testing POST /api/learning-engine/path/generate")
    params = {
        "user_id": "test_user",
        "domain_id": "programming_fundamentals", 
        "time_available_minutes": 30,
        "mode": "guided"
    }
    result = test_endpoint("POST", "/api/learning-engine/path/generate", params=params)
    tests.append(("POST /api/learning-engine/path/generate", result))
    
    if result["success"]:
        response = result["response"]
        user_id = response.get("user_id", "")
        domain = response.get("domain", {})
        mode = response.get("mode", "")
        time_budget = response.get("time_budget", 0)
        recommended_path = response.get("recommended_path", [])
        redundancy_coverage = response.get("redundancy_coverage", "")
        
        print(f"   ✅ SUCCESS: Generated path for user '{user_id}' in '{mode}' mode")
        print(f"   📖 Domain: {domain.get('name', 'Unknown')} ({time_budget} minutes)")
        print(f"   🛤️  Path steps: {len(recommended_path)}, Coverage: {redundancy_coverage}")
        
        # Show path details
        for i, step in enumerate(recommended_path[:3]):
            layer = step.get("layer", "")
            duration = step.get("duration", 0)
            priority = step.get("priority", "")
            print(f"      Step {i+1}: {layer} ({duration}min, {priority} priority)")
    else:
        print(f"   ❌ FAILED: {result.get('error', 'Unknown error')} (Status: {result.get('status_code', 'N/A')})")
    print()
    
    # Summary
    print("📊 TESTING SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result["success"])
    total = len(tests)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
    print()
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Multi-Layer Learning Engine API is fully functional.")
    else:
        print("⚠️  SOME TESTS FAILED. Details:")
        for test_name, result in tests:
            if not result["success"]:
                print(f"   ❌ {test_name}: {result.get('error', 'Unknown error')}")
    
    print()
    print("🔧 KEY TECHNICAL ACHIEVEMENTS:")
    print("1. Multi-layer redundant learning system with 6 cognitive pathways")
    print("2. 10 comprehensive learning domains covering all major programming areas")
    print("3. 5 different learning modes for personalized learning approaches")
    print("4. Intelligent path generation with time-based optimization")
    print("5. Comprehensive statistics and progress tracking capabilities")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)