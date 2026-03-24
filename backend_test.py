#!/usr/bin/env python3
"""
CodeDock v11.5 AI-to-Game Pipeline Backend API Testing
Testing World Engine, Narrative Engine, and Logic Engine APIs
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://ai-tutor-stage.preview.emergentagent.com"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single API endpoint"""
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            print_error(f"Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print_success(f"{method} {endpoint} - Status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                json_response = response.json()
                if isinstance(json_response, dict):
                    # Print key information from response
                    if 'name' in json_response:
                        print_info(f"  Name: {json_response['name']}")
                    if 'version' in json_response:
                        print_info(f"  Version: {json_response['version']}")
                    if 'capabilities' in json_response:
                        print_info(f"  Capabilities: {len(json_response['capabilities'])} features")
                    if 'id' in json_response:
                        print_info(f"  Generated ID: {json_response['id']}")
                    if 'title' in json_response:
                        print_info(f"  Title: {json_response['title']}")
                    
                    # Print response size
                    response_text = json.dumps(json_response)
                    print_info(f"  Response size: {len(response_text)} characters")
                    
                return True
            except json.JSONDecodeError:
                print_warning(f"  Response is not valid JSON")
                return True
                
        else:
            print_error(f"{method} {endpoint} - Status: {response.status_code}")
            try:
                error_detail = response.json()
                print_error(f"  Error: {error_detail}")
            except:
                print_error(f"  Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"{method} {endpoint} - Request failed: {str(e)}")
        return False

def test_world_engine():
    """Test World Engine APIs"""
    print_test_header("WORLD ENGINE API TESTING")
    
    tests = []
    
    # Test GET endpoints
    tests.append(test_endpoint("GET", "/api/world-engine/info"))
    tests.append(test_endpoint("GET", "/api/world-engine/styles"))
    tests.append(test_endpoint("GET", "/api/world-engine/biomes"))
    
    # Test POST generate endpoint
    world_request = {
        "prompt": "A mystical forest with ancient ruins",
        "style": "fantasy",
        "scale": "medium",
        "include_terrain": True,
        "include_structures": True
    }
    tests.append(test_endpoint("POST", "/api/world-engine/generate", world_request))
    
    passed = sum(tests)
    total = len(tests)
    print_info(f"World Engine Tests: {passed}/{total} passed")
    return passed, total

def test_narrative_engine():
    """Test Narrative Engine APIs"""
    print_test_header("NARRATIVE ENGINE API TESTING")
    
    tests = []
    
    # Test GET endpoints
    tests.append(test_endpoint("GET", "/api/narrative/info"))
    tests.append(test_endpoint("GET", "/api/narrative/structures"))
    tests.append(test_endpoint("GET", "/api/narrative/archetypes"))
    
    # Test POST generate-story endpoint
    story_request = {
        "premise": "A hero discovers an ancient artifact",
        "genre": "fantasy",
        "tone": "epic",
        "structure": "hero_journey"
    }
    tests.append(test_endpoint("POST", "/api/narrative/generate-story", story_request))
    
    # Test POST generate-quest endpoint
    quest_request = {
        "description": "Retrieve the stolen crown",
        "quest_type": "main",
        "difficulty": "medium"
    }
    tests.append(test_endpoint("POST", "/api/narrative/generate-quest", quest_request))
    
    passed = sum(tests)
    total = len(tests)
    print_info(f"Narrative Engine Tests: {passed}/{total} passed")
    return passed, total

def test_logic_engine():
    """Test Logic Engine APIs"""
    print_test_header("LOGIC ENGINE API TESTING")
    
    tests = []
    
    # Test GET endpoints
    tests.append(test_endpoint("GET", "/api/game-logic/info"))
    tests.append(test_endpoint("GET", "/api/game-logic/templates"))
    tests.append(test_endpoint("GET", "/api/game-logic/ai-templates"))
    
    # Test POST generate-mechanic endpoint
    mechanic_request = {
        "description": "Turn-based combat with elemental weaknesses",
        "mechanic_type": "combat",
        "complexity": "medium"
    }
    tests.append(test_endpoint("POST", "/api/game-logic/generate-mechanic", mechanic_request))
    
    # Test POST generate-ai endpoint
    ai_request = {
        "entity_type": "boss",
        "description": "A dragon that adapts to player tactics",
        "behavior_style": "tactical",
        "intelligence_level": "boss"
    }
    tests.append(test_endpoint("POST", "/api/game-logic/generate-ai", ai_request))
    
    passed = sum(tests)
    total = len(tests)
    print_info(f"Logic Engine Tests: {passed}/{total} passed")
    return passed, total

def main():
    """Run all tests"""
    print_test_header("CODEDOCK v11.5 AI-TO-GAME PIPELINE API TESTING")
    print_info(f"Backend URL: {BACKEND_URL}")
    print_info(f"Test started at: {datetime.now().isoformat()}")
    
    total_passed = 0
    total_tests = 0
    
    # Test World Engine
    passed, tests = test_world_engine()
    total_passed += passed
    total_tests += tests
    
    # Test Narrative Engine
    passed, tests = test_narrative_engine()
    total_passed += passed
    total_tests += tests
    
    # Test Logic Engine
    passed, tests = test_logic_engine()
    total_passed += passed
    total_tests += tests
    
    # Final Results
    print_test_header("FINAL RESULTS")
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    if success_rate == 100:
        print_success(f"ALL TESTS PASSED: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    elif success_rate >= 80:
        print_warning(f"MOSTLY SUCCESSFUL: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    else:
        print_error(f"MULTIPLE FAILURES: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    
    print_info(f"Test completed at: {datetime.now().isoformat()}")
    
    # Return appropriate exit code
    return 0 if success_rate == 100 else 1

if __name__ == "__main__":
    sys.exit(main())