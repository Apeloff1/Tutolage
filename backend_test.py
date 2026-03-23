#!/usr/bin/env python3
"""
CodeDock v11.3 SOTA Backend API Testing
Testing Multi-Agent System, SOTA 2026, Code Intelligence, and Collaboration APIs
"""

import requests
import json
import sys
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = "https://ai-tutor-stage.preview.emergentagent.com/api"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        result = {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "success": response.status_code == expected_status,
            "response_size": len(response.text),
            "timestamp": datetime.now().isoformat()
        }
        
        if response.status_code == expected_status:
            try:
                json_data = response.json()
                result["response_data"] = json_data
            except:
                result["response_text"] = response.text[:500]
        else:
            result["error"] = response.text[:500]
            
        return result
        
    except Exception as e:
        return {
            "endpoint": endpoint,
            "method": method,
            "error": str(e),
            "success": False,
            "timestamp": datetime.now().isoformat()
        }

def main():
    print("🚀 CodeDock v11.3 SOTA Backend API Testing")
    print("=" * 60)
    
    test_results = []
    
    # ============================================================================
    # 1. MULTI-AGENT SYSTEM TESTS (prefix: /api/agents)
    # ============================================================================
    
    print("\n🤖 MULTI-AGENT SYSTEM TESTS")
    print("-" * 40)
    
    # Test 1: GET /api/agents/info
    print("Testing GET /api/agents/info...")
    result = test_endpoint("GET", "/agents/info")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        print(f"✅ Multi-Agent info: {data.get('name', 'N/A')} v{data.get('version', 'N/A')}")
        print(f"   Total agents: {data.get('total_agents', 0)}")
        print(f"   Agent systems: {len(data.get('systems', {}))}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 2: GET /api/agents/roles
    print("\nTesting GET /api/agents/roles...")
    result = test_endpoint("GET", "/agents/roles")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        roles_count = len(data.get("roles", {}))
        print(f"✅ Agent roles: {roles_count} roles available")
        if roles_count > 0:
            sample_roles = list(data["roles"].keys())[:3]
            print(f"   Sample roles: {', '.join(sample_roles)}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 3: GET /api/agents/systems
    print("\nTesting GET /api/agents/systems...")
    result = test_endpoint("GET", "/agents/systems")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        systems_count = len(data.get("systems", {}))
        print(f"✅ Agent systems: {systems_count} systems available")
        if systems_count > 0:
            sample_systems = list(data["systems"].keys())[:3]
            print(f"   Sample systems: {', '.join(sample_systems)}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # ============================================================================
    # 2. SOTA 2026 TESTS (prefix: /api/sota)
    # ============================================================================
    
    print("\n🔬 SOTA 2026 TESTS")
    print("-" * 40)
    
    # Test 4: GET /api/sota/info
    print("Testing GET /api/sota/info...")
    result = test_endpoint("GET", "/sota/info")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        print(f"✅ SOTA info: {data.get('name', 'N/A')} v{data.get('version', 'N/A')}")
        features = data.get("features", {})
        print(f"   Features available: {len(features)}")
        if features:
            feature_names = list(features.keys())[:3]
            print(f"   Sample features: {', '.join(feature_names)}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # ============================================================================
    # 3. CODE INTELLIGENCE TESTS (prefix: /api/intelligence)
    # ============================================================================
    
    print("\n🧠 CODE INTELLIGENCE TESTS")
    print("-" * 40)
    
    # Test 5: GET /api/intelligence/info
    print("Testing GET /api/intelligence/info...")
    result = test_endpoint("GET", "/intelligence/info")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        print(f"✅ Intelligence info: {data.get('name', 'N/A')} v{data.get('version', 'N/A')}")
        features = data.get("features", [])
        print(f"   Intelligence features: {len(features)}")
        if features:
            feature_names = [f["name"] for f in features[:3]]
            print(f"   Sample features: {', '.join(feature_names)}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # ============================================================================
    # 4. COLLABORATION TESTS (prefix: /api/collab)
    # ============================================================================
    
    print("\n👥 COLLABORATION TESTS")
    print("-" * 40)
    
    # Test 6: GET /api/collab/info
    print("Testing GET /api/collab/info...")
    result = test_endpoint("GET", "/collab/info")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        print(f"✅ Collaboration info: {data.get('name', 'N/A')} v{data.get('version', 'N/A')}")
        features = data.get("features", [])
        print(f"   Collaboration features: {len(features)}")
        active_sessions = data.get("active_sessions", 0)
        print(f"   Active sessions: {active_sessions}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 7: GET /api/collab/sessions
    print("\nTesting GET /api/collab/sessions...")
    result = test_endpoint("GET", "/collab/sessions")
    test_results.append(result)
    if result["success"]:
        data = result["response_data"]
        sessions_count = data.get("count", 0)
        print(f"✅ Active sessions: {sessions_count} sessions")
        if sessions_count > 0:
            sessions = data.get("sessions", {})
            print(f"   Session IDs: {list(sessions.keys())[:3]}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r["success"])
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\n📋 DETAILED RESULTS:")
    for i, result in enumerate(test_results, 1):
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        endpoint = result["endpoint"]
        method = result["method"]
        print(f"{i:2d}. {method} {endpoint} - {status}")
        if not result["success"]:
            error = result.get("error", "Unknown error")[:100]
            print(f"     Error: {error}")
    
    # ============================================================================
    # FEATURE VERIFICATION
    # ============================================================================
    
    print("\n🔍 FEATURE VERIFICATION:")
    
    # Check Multi-Agent System
    multi_agent_working = any(r["success"] and "/agents/" in r["endpoint"] for r in test_results)
    print(f"Multi-Agent System: {'✅ Working' if multi_agent_working else '❌ Issues'}")
    
    # Check SOTA 2026
    sota_working = any(r["success"] and "/sota/" in r["endpoint"] for r in test_results)
    print(f"SOTA 2026 Features: {'✅ Working' if sota_working else '❌ Issues'}")
    
    # Check Code Intelligence
    intel_working = any(r["success"] and "/intelligence/" in r["endpoint"] for r in test_results)
    print(f"Code Intelligence: {'✅ Working' if intel_working else '❌ Issues'}")
    
    # Check Collaboration
    collab_working = any(r["success"] and "/collab/" in r["endpoint"] for r in test_results)
    print(f"Collaboration: {'✅ Working' if collab_working else '❌ Issues'}")
    
    print("\n🎯 CODEDOCK v11.3 SOTA BACKEND API TESTING COMPLETE!")
    
    # Return appropriate exit code
    return 0 if success_rate == 100 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)