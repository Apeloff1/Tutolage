#!/usr/bin/env python3
"""
CodeDock v11.9 Enhanced AI Toolkit Backend API Testing Suite
Testing AI Toolkit endpoints as requested in review
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from pathlib import Path

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://codedock-learn.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class CodeDockTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []
        
    async def test_endpoint(self, method: str, endpoint: str, data=None, params=None, description=""):
        """Test a single endpoint and record results"""
        url = f"{API_BASE}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = await self.client.get(url, params=params)
            elif method.upper() == "POST":
                response = await self.client.post(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == 200
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "success": success,
                "description": description,
                "response_size": len(response.text) if response.text else 0,
                "error": None if success else response.text[:500]
            }
            
            if success:
                try:
                    json_data = response.json()
                    result["response_data"] = json_data
                except:
                    result["response_data"] = response.text[:200]
            
            self.results.append(result)
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {method} {endpoint} - {description}")
            if not success:
                print(f"   Error: {response.status_code} - {response.text[:200]}")
            
            return result
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "success": False,
                "description": description,
                "error": str(e)
            }
            self.results.append(result)
            print(f"❌ FAIL {method} {endpoint} - {description}")
            print(f"   Exception: {str(e)}")
            return result

    async def test_ai_toolkit_info(self):
        """Test AI Toolkit info endpoint"""
        print("\n🤖 TESTING AI TOOLKIT INFO ENDPOINT")
        print("=" * 60)
        
        # GET /api/ai-toolkit/info - Should return AI toolkit capabilities (10 tools)
        result = await self.test_endpoint(
            "GET", "/ai-toolkit/info",
            description="AI toolkit capabilities (should have 10 tools)"
        )
        
        # Validate response structure
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            capabilities = data.get("capabilities", [])
            print(f"   Found {len(capabilities)} capabilities")
            if len(capabilities) == 10:
                print("   ✅ Correct number of capabilities (10)")
            else:
                print(f"   ⚠️  Expected 10 capabilities, found {len(capabilities)}")
        
        return result

    async def test_ai_toolkit_code_review(self):
        """Test AI Toolkit code review endpoint"""
        print("\n🔍 TESTING AI TOOLKIT CODE REVIEW ENDPOINT")
        print("=" * 60)
        
        # POST /api/ai-toolkit/code-review with specific body as requested
        code_review_data = {
            "code": "def hello():\n    print('Hello World')\n    x = 1\n    y = 2\n    return x + y",
            "language": "python",
            "review_depth": "standard"
        }
        
        result = await self.test_endpoint(
            "POST", "/ai-toolkit/code-review",
            data=code_review_data,
            description="Code review with structure analysis, security analysis, quality score, and AI review"
        )
        
        # Validate response structure
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            required_fields = ["structure_analysis", "security_analysis", "quality_score", "ai_review"]
            
            for field in required_fields:
                if field in data:
                    print(f"   ✅ Found {field}")
                else:
                    print(f"   ❌ Missing {field}")
            
            # Check structure analysis details
            if "structure_analysis" in data:
                structure = data["structure_analysis"]
                print(f"   Structure: {structure.get('total_lines', 0)} lines, complexity {structure.get('cyclomatic_complexity', 0)}")
            
            # Check quality score
            if "quality_score" in data:
                quality = data["quality_score"]
                print(f"   Quality Score: {quality.get('overall', 0)}/100 (Grade: {quality.get('grade', 'N/A')})")
        
        return result

    async def test_ai_toolkit_quality_score(self):
        """Test AI Toolkit quality score endpoint"""
        print("\n📊 TESTING AI TOOLKIT QUALITY SCORE ENDPOINT")
        print("=" * 60)
        
        # GET /api/ai-toolkit/quality-score with query params as requested
        params = {
            "code": "def test(): pass",
            "language": "python"
        }
        
        result = await self.test_endpoint(
            "GET", "/ai-toolkit/quality-score",
            params=params,
            description="Quality score with metrics"
        )
        
        # Validate response structure
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            required_fields = ["code_metrics", "quality_score"]
            
            for field in required_fields:
                if field in data:
                    print(f"   ✅ Found {field}")
                else:
                    print(f"   ❌ Missing {field}")
            
            # Check quality score details
            if "quality_score" in data:
                quality = data["quality_score"]
                print(f"   Overall Score: {quality.get('overall', 0)}/100")
                print(f"   Grade: {quality.get('grade', 'N/A')}")
                if "breakdown" in quality:
                    breakdown = quality["breakdown"]
                    print(f"   Breakdown: Maintainability={breakdown.get('maintainability', 0)}, Security={breakdown.get('security', 0)}")
        
        return result

    async def test_ai_toolkit_generate_tests(self):
        """Test AI Toolkit generate tests endpoint"""
        print("\n🧪 TESTING AI TOOLKIT GENERATE TESTS ENDPOINT")
        print("=" * 60)
        
        # POST /api/ai-toolkit/generate-tests with specific body as requested
        test_generation_data = {
            "code": "def add(a, b):\n    return a + b",
            "language": "python",
            "test_framework": "pytest",
            "test_types": ["unit", "edge_cases"]
        }
        
        result = await self.test_endpoint(
            "POST", "/ai-toolkit/generate-tests",
            data=test_generation_data,
            description="Generate automated tests for code"
        )
        
        # Validate response structure
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            required_fields = ["test_code", "framework", "test_types"]
            
            for field in required_fields:
                if field in data:
                    print(f"   ✅ Found {field}")
                else:
                    print(f"   ❌ Missing {field}")
            
            # Check test generation details
            if "test_code" in data:
                test_code = data["test_code"]
                print(f"   Generated test code length: {len(test_code)} characters")
            
            if "estimated_test_count" in data:
                print(f"   Estimated test count: {data['estimated_test_count']}")
            
            if "framework" in data:
                print(f"   Framework: {data['framework']}")
        
        return result

    async def run_all_tests(self):
        """Run all test suites"""
        print(f"🚀 STARTING CODEDOCK v11.9 ENHANCED AI TOOLKIT TESTING")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print(f"Test started at: {datetime.now().isoformat()}")
        
        # Run AI Toolkit test suites as requested
        await self.test_ai_toolkit_info()
        await self.test_ai_toolkit_code_review()
        await self.test_ai_toolkit_quality_score()
        await self.test_ai_toolkit_generate_tests()
        
        # Generate summary
        await self.generate_summary()
        
    async def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Group by endpoint category
        ai_toolkit_tests = [r for r in self.results if r["endpoint"].startswith("/ai-toolkit")]
        
        print(f"\n📊 RESULTS BY CATEGORY:")
        print(f"AI Toolkit Enhanced: {sum(1 for r in ai_toolkit_tests if r['success'])}/{len(ai_toolkit_tests)} passed")
        
        # Show failed tests
        failed_results = [r for r in self.results if not r["success"]]
        if failed_results:
            print(f"\n❌ FAILED TESTS:")
            for result in failed_results:
                print(f"  • {result['method']} {result['endpoint']} - {result['description']}")
                print(f"    Status: {result['status_code']}, Error: {result.get('error', 'Unknown')[:100]}")
        
        # Show successful tests with key data
        successful_results = [r for r in self.results if r["success"]]
        if successful_results:
            print(f"\n✅ SUCCESSFUL TESTS:")
            for result in successful_results:
                print(f"  • {result['method']} {result['endpoint']} - {result['description']}")
                if "response_data" in result and isinstance(result["response_data"], dict):
                    # Show key response data
                    data = result["response_data"]
                    if "name" in data:
                        print(f"    Name: {data['name']}")
                    if "capabilities" in data and isinstance(data["capabilities"], list):
                        print(f"    Capabilities: {len(data['capabilities'])}")
                    if "quality_score" in data and isinstance(data["quality_score"], dict):
                        quality = data["quality_score"]
                        print(f"    Quality Score: {quality.get('overall', 0)}/100 (Grade: {quality.get('grade', 'N/A')})")
                    if "test_code" in data:
                        print(f"    Generated test code: {len(data['test_code'])} characters")
                    if "framework" in data:
                        print(f"    Test framework: {data['framework']}")
        
        print(f"\n🎯 CONCLUSION:")
        if success_rate >= 90:
            print("🏆 EXCELLENT! All AI Toolkit endpoints are working correctly.")
        elif success_rate >= 75:
            print("✅ GOOD! Most AI Toolkit endpoints are working with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE! Some AI Toolkit endpoints need attention.")
        else:
            print("🚨 CRITICAL! Multiple AI Toolkit endpoints are failing.")
        
        await self.client.aclose()

async def main():
    """Main test runner"""
    tester = CodeDockTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())