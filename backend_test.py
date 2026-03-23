#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CODEDOCK v11.3 COMPREHENSIVE BACKEND API TESTING SUITE                      ║
║  Testing Multi-Agent, SOTA 2026, Code Intelligence, Collaboration,           ║
║  AI Log Vault, and Jeeves Tutor APIs                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://ai-tutor-stage.preview.emergentagent.com/api"

class CodeDockTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, response_data: Any = None, error: str = None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "response_data": response_data,
            "error": error
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if error:
            print(f"      Error: {error}")
        if response_data and isinstance(response_data, dict):
            if 'name' in response_data:
                print(f"      Response: {response_data.get('name', 'N/A')}")
            elif 'status' in response_data:
                print(f"      Status: {response_data.get('status', 'N/A')}")
    
    async def test_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict:
        """Test a single endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
                    return {"success": success, "data": response_data, "status": response.status}
            
            elif method.upper() == "POST":
                headers = {"Content-Type": "application/json"}
                async with self.session.post(url, json=data, headers=headers) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
                    return {"success": success, "data": response_data, "status": response.status}
                    
        except Exception as e:
            return {"success": False, "data": None, "error": str(e), "status": 0}
    
    # ============================================================================
    # 1. MULTI-AGENT SYSTEM TESTS
    # ============================================================================
    
    async def test_multi_agent_system(self):
        """Test Multi-Agent System endpoints"""
        print("\n🤖 TESTING MULTI-AGENT SYSTEM")
        print("=" * 50)
        
        # Test 1: GET /api/agents/info
        result = await self.test_endpoint("GET", "/agents/info")
        self.log_result(
            "Multi-Agent System Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/agents/run/code_architect
        test_data = {
            "system": "code_architect",
            "task": "Create a hello world function",
            "code": "",
            "language": "python",
            "max_iterations": 1
        }
        
        result = await self.test_endpoint("POST", "/agents/run/code_architect", test_data)
        self.log_result(
            "Code Architect Multi-Agent Run",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # 2. SOTA 2026 TESTS
    # ============================================================================
    
    async def test_sota_2026(self):
        """Test SOTA 2026 endpoints"""
        print("\n🚀 TESTING SOTA 2026 FEATURES")
        print("=" * 50)
        
        # Test 1: GET /api/sota/info
        result = await self.test_endpoint("GET", "/sota/info")
        self.log_result(
            "SOTA 2026 Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/sota/predict
        predict_data = {
            "code": "def hello():\n    print('hello')",
            "language": "python",
            "recent_actions": []
        }
        
        result = await self.test_endpoint("POST", "/sota/predict", predict_data)
        self.log_result(
            "SOTA Predictive Assistance",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 3: POST /api/sota/code-intel
        intel_data = {
            "code": "def test(): pass",
            "language": "python",
            "analysis_types": ["complexity"]
        }
        
        result = await self.test_endpoint("POST", "/sota/code-intel", intel_data)
        self.log_result(
            "SOTA Code Intelligence",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # 3. CODE INTELLIGENCE TESTS
    # ============================================================================
    
    async def test_code_intelligence(self):
        """Test Code Intelligence endpoints"""
        print("\n🧠 TESTING CODE INTELLIGENCE")
        print("=" * 50)
        
        # Test 1: GET /api/intelligence/info
        result = await self.test_endpoint("GET", "/intelligence/info")
        self.log_result(
            "Code Intelligence Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/intelligence/auto-document
        doc_data = {
            "code": "def add(a, b):\n    return a + b",
            "language": "python",
            "doc_style": "google"
        }
        
        result = await self.test_endpoint("POST", "/intelligence/auto-document", doc_data)
        self.log_result(
            "Auto Documentation Generation",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 3: POST /api/intelligence/predict-bugs
        bug_data = {
            "code": "x = None\nprint(x.upper())",
            "language": "python"
        }
        
        result = await self.test_endpoint("POST", "/intelligence/predict-bugs", bug_data)
        self.log_result(
            "Bug Prediction",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # 4. COLLABORATION TESTS
    # ============================================================================
    
    async def test_collaboration(self):
        """Test Collaboration endpoints"""
        print("\n👥 TESTING COLLABORATION FEATURES")
        print("=" * 50)
        
        # Test 1: GET /api/collab/info
        result = await self.test_endpoint("GET", "/collab/info")
        self.log_result(
            "Collaboration Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/collab/pair-program
        pair_data = {
            "code": "print('hi')",
            "language": "python",
            "task": "Add error handling",
            "ai_role": "copilot"
        }
        
        result = await self.test_endpoint("POST", "/collab/pair-program", pair_data)
        self.log_result(
            "AI Pair Programming",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # 5. AI LOG VAULT TESTS
    # ============================================================================
    
    async def test_ai_log_vault(self):
        """Test AI Log Vault endpoints"""
        print("\n📊 TESTING AI LOG VAULT")
        print("=" * 50)
        
        # Test 1: GET /api/ai-logs/info
        result = await self.test_endpoint("GET", "/ai-logs/info")
        self.log_result(
            "AI Log Vault Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/ai-logs/startup-train
        result = await self.test_endpoint("POST", "/ai-logs/startup-train")
        self.log_result(
            "AI Log Vault Startup Training",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # 6. JEEVES TUTOR TESTS
    # ============================================================================
    
    async def test_jeeves_tutor(self):
        """Test Jeeves Tutor endpoints"""
        print("\n🎩 TESTING JEEVES AI TUTOR")
        print("=" * 50)
        
        # Test 1: GET /api/jeeves/info
        result = await self.test_endpoint("GET", "/jeeves/info")
        self.log_result(
            "Jeeves Tutor Info",
            result["success"],
            result.get("data"),
            result.get("error")
        )
        
        # Test 2: POST /api/jeeves/ask-with-context
        ask_data = {
            "message": "What is a loop?",
            "skill_level": "beginner"
        }
        
        result = await self.test_endpoint("POST", "/jeeves/ask-with-context", ask_data)
        self.log_result(
            "Jeeves Ask with Context",
            result["success"],
            result.get("data"),
            result.get("error")
        )
    
    # ============================================================================
    # MAIN TEST RUNNER
    # ============================================================================
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    CODEDOCK v11.3 BACKEND API TESTING                         ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Started at: {datetime.utcnow().isoformat()}")
        
        # Run all test suites
        await self.test_multi_agent_system()
        await self.test_sota_2026()
        await self.test_code_intelligence()
        await self.test_collaboration()
        await self.test_ai_log_vault()
        await self.test_jeeves_tutor()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🎯 TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test']}")
                if test.get('error'):
                    print(f"     Error: {test['error']}")
        
        # Show successful tests
        passed_tests = [r for r in self.results if r["success"]]
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"   • {test['test']}")
        
        print("\n" + "=" * 80)
        
        # Overall status
        if success_rate >= 90:
            print("🎉 EXCELLENT: All systems operational!")
        elif success_rate >= 75:
            print("✅ GOOD: Most systems working, minor issues detected")
        elif success_rate >= 50:
            print("⚠️  WARNING: Several systems have issues")
        else:
            print("🚨 CRITICAL: Major system failures detected")

async def main():
    """Main test runner"""
    async with CodeDockTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())