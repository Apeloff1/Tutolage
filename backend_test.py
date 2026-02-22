#!/usr/bin/env python3
"""
CodeDock v10.0.0 (CS Bible Edition) - Comprehensive Backend API Testing
Testing all modular routes and endpoints as specified in the review request.
"""

import requests
import json
import time
from typing import Dict, Any, List
import sys

# Backend URL from frontend .env
BACKEND_URL = "https://codedock-ultimate.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def success(self, test_name: str, details: str = ""):
        self.passed += 1
        print(f"{Colors.GREEN}✅ {test_name}{Colors.END}")
        if details:
            print(f"   {Colors.CYAN}{details}{Colors.END}")
            
    def failure(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"{Colors.RED}❌ {test_name}{Colors.END}")
        print(f"   {Colors.RED}Error: {error}{Colors.END}")
        
    def summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")
        print(f"Success Rate: {Colors.GREEN if success_rate >= 80 else Colors.YELLOW}{success_rate:.1f}%{Colors.END}")
        
        if self.errors:
            print(f"\n{Colors.RED}FAILED TESTS:{Colors.END}")
            for error in self.errors:
                print(f"  • {error}")

def make_request(method: str, endpoint: str, data: Dict = None, timeout: int = 10) -> Dict[str, Any]:
    """Make HTTP request with error handling"""
    try:
        url = f"{API_BASE}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=timeout)
        elif method.upper() == "DELETE":
            response = requests.delete(url, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error"}
    except Exception as e:
        return {"error": str(e)}

def test_health_and_system_routes(result: TestResult):
    """Test Health & System Routes"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🏥 TESTING HEALTH & SYSTEM ROUTES{Colors.END}")
    
    # Test root info endpoint
    response = make_request("GET", "/")
    if "error" in response:
        result.failure("GET /api/ - Root info", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and data.get("version") == "10.0.0":
            result.success("GET /api/ - Root info", f"Version: {data.get('version')}, Codename: {data.get('codename', 'N/A')}")
        else:
            result.failure("GET /api/ - Root info", f"Expected version 10.0.0, got: {data.get('version') if isinstance(data, dict) else 'Invalid response'}")
    else:
        result.failure("GET /api/ - Root info", f"HTTP {response['status_code']}")
    
    # Test health check
    response = make_request("GET", "/health")
    if "error" in response:
        result.failure("GET /api/health - Health check", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and data.get("status") == "healthy":
            result.success("GET /api/health - Health check", f"Status: {data.get('status')}")
        else:
            result.failure("GET /api/health - Health check", f"Expected healthy status, got: {data}")
    else:
        result.failure("GET /api/health - Health check", f"HTTP {response['status_code']}")
    
    # Test readiness probe
    response = make_request("GET", "/readiness")
    if "error" in response:
        result.failure("GET /api/readiness - Readiness probe", response["error"])
    elif response["status_code"] == 200:
        result.success("GET /api/readiness - Readiness probe", "Kubernetes readiness OK")
    else:
        result.failure("GET /api/readiness - Readiness probe", f"HTTP {response['status_code']}")
    
    # Test liveness probe
    response = make_request("GET", "/liveness")
    if "error" in response:
        result.failure("GET /api/liveness - Liveness probe", response["error"])
    elif response["status_code"] == 200:
        result.success("GET /api/liveness - Liveness probe", "Kubernetes liveness OK")
    else:
        result.failure("GET /api/liveness - Liveness probe", f"HTTP {response['status_code']}")
    
    # Test system info
    response = make_request("GET", "/system/info")
    if "error" in response:
        result.failure("GET /api/system/info - System info", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict):
            result.success("GET /api/system/info - System info", f"System info retrieved")
        else:
            result.failure("GET /api/system/info - System info", "Invalid response format")
    else:
        result.failure("GET /api/system/info - System info", f"HTTP {response['status_code']}")

def test_cs_bible_routes(result: TestResult):
    """Test CS Bible Routes (Modular)"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}📚 TESTING CS BIBLE ROUTES{Colors.END}")
    
    # Test full curriculum overview
    response = make_request("GET", "/bible")
    if "error" in response:
        result.failure("GET /api/bible - Full curriculum overview", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "total_years" in data and "total_courses" in data:
            result.success("GET /api/bible - Full curriculum overview", 
                         f"Years: {data.get('total_years')}, Courses: {data.get('total_courses')}, Hours: {data.get('total_hours')}")
        else:
            result.failure("GET /api/bible - Full curriculum overview", "Missing expected fields")
    else:
        result.failure("GET /api/bible - Full curriculum overview", f"HTTP {response['status_code']}")
    
    # Test Year 1 details
    response = make_request("GET", "/bible/year/1")
    if "error" in response:
        result.failure("GET /api/bible/year/1 - Year 1 details", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "year" in data:
            result.success("GET /api/bible/year/1 - Year 1 details", 
                         f"Year {data.get('year')}: {data.get('name', 'N/A')}")
        else:
            result.failure("GET /api/bible/year/1 - Year 1 details", "Missing expected fields")
    else:
        result.failure("GET /api/bible/year/1 - Year 1 details", f"HTTP {response['status_code']}")
    
    # Test CS 101 course
    response = make_request("GET", "/bible/course/y1_cs101")
    if "error" in response:
        result.failure("GET /api/bible/course/y1_cs101 - CS 101 course", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "id" in data and "title" in data:
            result.success("GET /api/bible/course/y1_cs101 - CS 101 course", 
                         f"Course: {data.get('title')}")
        else:
            result.failure("GET /api/bible/course/y1_cs101 - CS 101 course", "Missing expected fields")
    else:
        result.failure("GET /api/bible/course/y1_cs101 - CS 101 course", f"HTTP {response['status_code']}")
    
    # Test all tracks
    response = make_request("GET", "/bible/tracks")
    if "error" in response:
        result.failure("GET /api/bible/tracks - All 8 tracks", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, list) and len(data) == 8:
            track_names = [track.get('name', 'Unknown') for track in data if isinstance(track, dict)]
            result.success("GET /api/bible/tracks - All 8 tracks", f"Found {len(data)} tracks")
        else:
            result.failure("GET /api/bible/tracks - All 8 tracks", f"Expected 8 tracks, got: {len(data) if isinstance(data, list) else 'Invalid format'}")
    else:
        result.failure("GET /api/bible/tracks - All 8 tracks", f"HTTP {response['status_code']}")
    
    # Test certification path
    response = make_request("GET", "/bible/certifications")
    if "error" in response:
        result.failure("GET /api/bible/certifications - Certification path", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "levels" in data and len(data["levels"]) >= 5:
            result.success("GET /api/bible/certifications - Certification path", 
                         f"Found {len(data['levels'])} certifications")
        else:
            result.failure("GET /api/bible/certifications - Certification path", f"Expected certification levels, got: {data}")
    else:
        result.failure("GET /api/bible/certifications - Certification path", f"HTTP {response['status_code']}")

def test_compiler_routes(result: TestResult):
    """Test Compiler Routes (Modular)"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}⚙️ TESTING COMPILER ROUTES{Colors.END}")
    
    # Test available sanitizers
    response = make_request("GET", "/compiler/sanitizers")
    if "error" in response:
        result.failure("GET /api/compiler/sanitizers - Available sanitizers", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "sanitizers" in data and len(data["sanitizers"]) > 0:
            sanitizers = data["sanitizers"]
            result.success("GET /api/compiler/sanitizers - Available sanitizers", 
                         f"Found {len(sanitizers)} sanitizers")
        else:
            result.failure("GET /api/compiler/sanitizers - Available sanitizers", "No sanitizers found")
    else:
        result.failure("GET /api/compiler/sanitizers - Available sanitizers", f"HTTP {response['status_code']}")
    
    # Test available optimizers
    response = make_request("GET", "/compiler/optimizers")
    if "error" in response:
        result.failure("GET /api/compiler/optimizers - Available optimizers", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "optimizers" in data and len(data["optimizers"]) > 0:
            optimizers = data["optimizers"]
            result.success("GET /api/compiler/optimizers - Available optimizers", 
                         f"Found {len(optimizers)} optimizers")
        else:
            result.failure("GET /api/compiler/optimizers - Available optimizers", "No optimizers found")
    else:
        result.failure("GET /api/compiler/optimizers - Available optimizers", f"HTTP {response['status_code']}")
    
    # Test compile code
    compile_request = {
        "code": 'print("Hello from compiler test!")',
        "language": "python",
        "sanitizers": ["memory"],
        "optimizers": ["basic"]
    }
    response = make_request("POST", "/compiler/compile", compile_request)
    if "error" in response:
        result.failure("POST /api/compiler/compile - Compile code", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "success" in data and data.get("success"):
            result.success("POST /api/compiler/compile - Compile code", 
                         f"Compilation successful, {len(data.get('stages', []))} stages completed")
        else:
            result.failure("POST /api/compiler/compile - Compile code", "Compilation failed or invalid response")
    else:
        result.failure("POST /api/compiler/compile - Compile code", f"HTTP {response['status_code']}")

def test_hub_routes(result: TestResult):
    """Test Hub Routes (Modular)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 TESTING HUB ROUTES{Colors.END}")
    
    # Test hub info
    response = make_request("GET", "/v9/info")
    if "error" in response:
        result.failure("GET /api/v9/info - Hub info", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict):
            result.success("GET /api/v9/info - Hub info", f"Hub version: {data.get('version', 'N/A')}")
        else:
            result.failure("GET /api/v9/info - Hub info", "Invalid response format")
    else:
        result.failure("GET /api/v9/info - Hub info", f"HTTP {response['status_code']}")
    
    # Test language packs (should be 64)
    response = make_request("GET", "/language-packs")
    if "error" in response:
        result.failure("GET /api/language-packs - All language packs", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "packs" in data:
            packs = data["packs"]
            result.success("GET /api/language-packs - All language packs", 
                         f"Found {len(packs)} language packs (expected 64)")
        else:
            result.failure("GET /api/language-packs - All language packs", "Invalid response format")
    else:
        result.failure("GET /api/language-packs - All language packs", f"HTTP {response['status_code']}")
    
    # Test expansion packs (should be 10)
    response = make_request("GET", "/expansions")
    if "error" in response:
        result.failure("GET /api/expansions - All expansion packs", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "expansions" in data:
            expansions = data["expansions"]
            result.success("GET /api/expansions - All expansion packs", 
                         f"Found {len(expansions)} expansion packs (expected 10)")
        else:
            result.failure("GET /api/expansions - All expansion packs", "Invalid response format")
    else:
        result.failure("GET /api/expansions - All expansion packs", f"HTTP {response['status_code']}")
    
    # Test algorithms
    response = make_request("GET", "/algorithms")
    if "error" in response:
        result.failure("GET /api/algorithms - All algorithms", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "algorithms" in data:
            algorithms = data["algorithms"]
            total_algorithms = sum(len(category) for category in algorithms.values())
            result.success("GET /api/algorithms - All algorithms", f"Found {total_algorithms} algorithms in {len(algorithms)} categories")
        else:
            result.failure("GET /api/algorithms - All algorithms", "Invalid response format")
    else:
        result.failure("GET /api/algorithms - All algorithms", f"HTTP {response['status_code']}")

def test_ai_routes(result: TestResult):
    """Test AI Routes (Modular)"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}🤖 TESTING AI ROUTES{Colors.END}")
    
    # Test AI modes
    response = make_request("GET", "/ai/modes")
    if "error" in response:
        result.failure("GET /api/ai/modes - AI assistance modes", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "modes" in data and len(data["modes"]) > 0:
            modes = data["modes"]
            result.success("GET /api/ai/modes - AI assistance modes", 
                         f"Found {len(modes)} AI modes")
        else:
            result.failure("GET /api/ai/modes - AI assistance modes", "No AI modes found")
    else:
        result.failure("GET /api/ai/modes - AI assistance modes", f"HTTP {response['status_code']}")
    
    # Test AI providers
    response = make_request("GET", "/ai/hub/providers")
    if "error" in response:
        result.failure("GET /api/ai/hub/providers - AI providers", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "providers" in data and len(data["providers"]) > 0:
            providers = data["providers"]
            result.success("GET /api/ai/hub/providers - AI providers", 
                         f"Found {len(providers)} providers")
        else:
            result.failure("GET /api/ai/hub/providers - AI providers", "No AI providers found")
    else:
        result.failure("GET /api/ai/hub/providers - AI providers", f"HTTP {response['status_code']}")
    
    # Test AI assistance
    ai_request = {
        "code": 'def hello():\n    print("Hello World")',
        "language": "python",
        "mode": "explain"
    }
    response = make_request("POST", "/ai/assist", ai_request)
    if "error" in response:
        result.failure("POST /api/ai/assist - Get AI assistance", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "suggestion" in data:
            result.success("POST /api/ai/assist - Get AI assistance", 
                         f"AI mode: {data.get('mode')}, Response received")
        else:
            result.failure("POST /api/ai/assist - Get AI assistance", "Invalid response format")
    else:
        result.failure("POST /api/ai/assist - Get AI assistance", f"HTTP {response['status_code']}")

def test_core_routes(result: TestResult):
    """Test Core Routes"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}🔧 TESTING CORE ROUTES{Colors.END}")
    
    # Test available languages
    response = make_request("GET", "/languages")
    if "error" in response:
        result.failure("GET /api/languages - Available languages", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "languages" in data and len(data["languages"]) > 0:
            languages = data["languages"]
            executable_count = sum(1 for lang in languages if isinstance(lang, dict) and lang.get('executable', False))
            result.success("GET /api/languages - Available languages", 
                         f"Found {len(languages)} languages, {executable_count} executable")
        else:
            result.failure("GET /api/languages - Available languages", "No languages found or invalid format")
    else:
        result.failure("GET /api/languages - Available languages", f"HTTP {response['status_code']}")
    
    # Test code execution
    execute_request = {
        "code": 'print("test")',
        "language": "python"
    }
    response = make_request("POST", "/execute", execute_request)
    if "error" in response:
        result.failure("POST /api/execute - Execute code", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "result" in data:
            result.success("POST /api/execute - Execute code", 
                         f"Execution status: {data.get('result', {}).get('status', 'Unknown')}")
        else:
            result.failure("POST /api/execute - Execute code", "Invalid response format")
    else:
        result.failure("POST /api/execute - Execute code", f"HTTP {response['status_code']}")
    
    # Test tutorial steps
    response = make_request("GET", "/tutorial/steps")
    if "error" in response:
        result.failure("GET /api/tutorial/steps - Tutorial steps", response["error"])
    elif response["status_code"] == 200:
        data = response["data"]
        if isinstance(data, dict) and "steps" in data and len(data["steps"]) > 0:
            steps = data["steps"]
            result.success("GET /api/tutorial/steps - Tutorial steps", f"Found {len(steps)} tutorial steps")
        else:
            result.failure("GET /api/tutorial/steps - Tutorial steps", "No tutorial steps found")
    else:
        result.failure("GET /api/tutorial/steps - Tutorial steps", f"HTTP {response['status_code']}")

def main():
    """Run comprehensive backend API tests"""
    print(f"{Colors.BOLD}{Colors.WHITE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}CodeDock v10.0.0 (CS Bible Edition) - Backend API Testing{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}Testing Backend: {BACKEND_URL}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}{'='*80}{Colors.END}")
    
    result = TestResult()
    
    # Run all test suites
    test_health_and_system_routes(result)
    test_cs_bible_routes(result)
    test_compiler_routes(result)
    test_hub_routes(result)
    test_ai_routes(result)
    test_core_routes(result)
    
    # Print summary
    result.summary()
    
    # Return exit code based on results
    return 0 if result.failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)