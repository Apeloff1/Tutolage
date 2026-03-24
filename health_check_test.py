#!/usr/bin/env python3
"""
CodeDock v11.8 Backend Health Check
Quick verification of 6 key endpoints as requested in review
"""

import asyncio
import httpx
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://codedock-learn.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class HealthChecker:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []
        
    async def test_endpoint(self, endpoint: str, description="", expected_data=None):
        """Test a single endpoint and record results"""
        url = f"{API_BASE}{endpoint}"
        
        try:
            response = await self.client.get(url)
            success = response.status_code == 200
            
            result = {
                "endpoint": endpoint,
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
                    
                    # Check expected data if provided
                    if expected_data:
                        for key, expected_value in expected_data.items():
                            if key in json_data:
                                actual_value = json_data[key]
                                if isinstance(expected_value, str) and expected_value.endswith('+'):
                                    # Handle "1600+" type expectations
                                    min_value = int(expected_value[:-1])
                                    if isinstance(actual_value, (int, float)) and actual_value >= min_value:
                                        result[f"validation_{key}"] = f"✅ {actual_value} >= {min_value}"
                                    else:
                                        result[f"validation_{key}"] = f"❌ {actual_value} < {min_value}"
                                elif isinstance(expected_value, int):
                                    if actual_value == expected_value:
                                        result[f"validation_{key}"] = f"✅ {actual_value} == {expected_value}"
                                    else:
                                        result[f"validation_{key}"] = f"❌ {actual_value} != {expected_value}"
                                else:
                                    result[f"validation_{key}"] = f"Found: {actual_value}"
                            else:
                                result[f"validation_{key}"] = f"❌ Key '{key}' not found"
                                
                except Exception as e:
                    result["response_data"] = response.text[:200]
                    result["parse_error"] = str(e)
            
            self.results.append(result)
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} GET {endpoint} - {description}")
            if not success:
                print(f"   Error: {response.status_code} - {response.text[:200]}")
            else:
                # Show key validation results
                for key, value in result.items():
                    if key.startswith("validation_"):
                        print(f"   {key.replace('validation_', '').title()}: {value}")
            
            return result
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "status_code": 0,
                "success": False,
                "description": description,
                "error": str(e)
            }
            self.results.append(result)
            print(f"❌ FAIL GET {endpoint} - {description}")
            print(f"   Exception: {str(e)}")
            return result

    async def run_health_check(self):
        """Run the 6 endpoint health check as requested"""
        print(f"🏥 CODEDOCK v11.8 BACKEND HEALTH CHECK")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print(f"Health check started at: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # 1. GET /api/health - Basic health check
        await self.test_endpoint(
            "/health",
            "Basic health check",
            {"status": "healthy"}
        )
        
        # 2. GET /api/reading/info - Reading curriculum info (should return 1600+ hours)
        await self.test_endpoint(
            "/reading/info",
            "Reading curriculum info (should return 1600+ hours)",
            {"total_curriculum_hours": "1600+"}
        )
        
        # 3. GET /api/jeeves-eq/info - Jeeves EQ info
        await self.test_endpoint(
            "/jeeves-eq/info",
            "Jeeves EQ info"
        )
        
        # 4. GET /api/export/info - Export system info
        await self.test_endpoint(
            "/export/info",
            "Export system info"
        )
        
        # 5. GET /api/quiz-bank/info - Quiz bank info (should return 285 quizzes)
        await self.test_endpoint(
            "/quiz-bank/info",
            "Quiz bank info (should return 285 quizzes)",
            {"total_quizzes": 285}
        )
        
        # 6. GET /api/logscraper/info - Logscraper info (should return 37 action types)
        await self.test_endpoint(
            "/logscraper/info",
            "Logscraper info (should return 37 action types)"
        )
        
        # Generate summary
        await self.generate_summary()
        
    async def generate_summary(self):
        """Generate health check summary"""
        print("\n" + "=" * 80)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Endpoints Tested: {total_tests}")
        print(f"Healthy: {passed_tests} ✅")
        print(f"Unhealthy: {failed_tests} ❌")
        print(f"Health Score: {success_rate:.1f}%")
        
        # Show detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for i, result in enumerate(self.results, 1):
            status = "✅ HEALTHY" if result["success"] else "❌ UNHEALTHY"
            print(f"{i}. {status} {result['endpoint']} - {result['description']}")
            
            if result["success"]:
                if "response_data" in result and isinstance(result["response_data"], dict):
                    data = result["response_data"]
                    # Show key response indicators
                    if "status" in data:
                        print(f"   Status: {data['status']}")
                    if "name" in data:
                        print(f"   System: {data['name']}")
                    if "total_curriculum_hours" in data:
                        print(f"   Curriculum Hours: {data['total_curriculum_hours']}")
                    if "total_quizzes" in data:
                        print(f"   Total Quizzes: {data['total_quizzes']}")
                    if "total_action_types" in data:
                        print(f"   Action Types: {data['total_action_types']}")
                    if "capabilities" in data and isinstance(data["capabilities"], list):
                        print(f"   Capabilities: {len(data['capabilities'])}")
                        
                # Show validation results
                for key, value in result.items():
                    if key.startswith("validation_"):
                        print(f"   {key.replace('validation_', '').title()}: {value}")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')[:100]}")
        
        # Show failed endpoints
        failed_results = [r for r in self.results if not r["success"]]
        if failed_results:
            print(f"\n🚨 UNHEALTHY ENDPOINTS:")
            for result in failed_results:
                print(f"  • {result['endpoint']} - Status: {result['status_code']}")
                print(f"    Error: {result.get('error', 'Unknown')[:200]}")
        
        print(f"\n🎯 HEALTH CHECK CONCLUSION:")
        if success_rate == 100:
            print("🏆 PERFECT HEALTH! All endpoints are responding correctly.")
        elif success_rate >= 90:
            print("✅ EXCELLENT HEALTH! Minor issues detected.")
        elif success_rate >= 75:
            print("⚠️  GOOD HEALTH! Some endpoints need attention.")
        elif success_rate >= 50:
            print("🔧 MODERATE HEALTH! Multiple endpoints require fixes.")
        else:
            print("🚨 CRITICAL HEALTH ISSUES! System needs immediate attention.")
        
        await self.client.aclose()

async def main():
    """Main health check runner"""
    checker = HealthChecker()
    await checker.run_health_check()

if __name__ == "__main__":
    asyncio.run(main())