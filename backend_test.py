#!/usr/bin/env python3
"""
CodeDock v11.8 Backend API Testing Suite
Testing Export & GitHub Integration, Reading Curriculum, and Jeeves EQ endpoints
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

    async def test_export_github_integration(self):
        """Test Export & GitHub Integration endpoints"""
        print("\n🔧 TESTING EXPORT & GITHUB INTEGRATION ENDPOINTS")
        print("=" * 60)
        
        # 1. GET /api/export/info
        await self.test_endpoint(
            "GET", "/export/info",
            description="Export system capabilities"
        )
        
        # 2. POST /api/export/pdf
        pdf_data = {
            "content": "print('Hello World')",
            "filename": "test_code",
            "content_type": "code",
            "language": "python"
        }
        await self.test_endpoint(
            "POST", "/export/pdf",
            data=pdf_data,
            description="PDF export with Python code"
        )
        
        # 3. POST /api/export/log-ai-interaction
        ai_interaction_data = {
            "user_id": "test_user",
            "interaction_type": "code_generation",
            "prompt": "Write a hello world",
            "response": "Here is your code",
            "model_used": "gpt-4o"
        }
        await self.test_endpoint(
            "POST", "/export/log-ai-interaction",
            data=ai_interaction_data,
            description="Log AI interaction for learning"
        )
        
        # 4. GET /api/export/ai-interactions/test_user
        await self.test_endpoint(
            "GET", "/export/ai-interactions/test_user",
            description="Get AI interaction history"
        )

    async def test_reading_curriculum(self):
        """Test Reading Curriculum endpoints"""
        print("\n📚 TESTING READING CURRICULUM ENDPOINTS")
        print("=" * 60)
        
        # 1. GET /api/reading/info
        await self.test_endpoint(
            "GET", "/reading/info",
            description="Comprehensive curriculum info (1600+ hours)"
        )
        
        # 2. GET /api/reading/tracks
        await self.test_endpoint(
            "GET", "/reading/tracks",
            description="Get 4 learning tracks"
        )
        
        # 3. GET /api/reading/track/game_development
        await self.test_endpoint(
            "GET", "/reading/track/game_development",
            description="Game dev track with sub-tracks"
        )
        
        # 4. GET /api/reading/manuals
        await self.test_endpoint(
            "GET", "/reading/manuals",
            description="Advanced and language manuals"
        )

    async def test_jeeves_eq(self):
        """Test Jeeves EQ endpoints"""
        print("\n🧠 TESTING JEEVES EQ ENDPOINTS")
        print("=" * 60)
        
        # 1. GET /api/jeeves-eq/info
        await self.test_endpoint(
            "GET", "/jeeves-eq/info",
            description="EQ capabilities"
        )
        
        # 2. POST /api/jeeves-eq/detect-emotion
        emotion_data = [
            {"action_type": "challenge_completed"},
            {"action_type": "quiz_completed"}
        ]
        await self.test_endpoint(
            "POST", "/jeeves-eq/detect-emotion",
            data=emotion_data,
            params={"user_id": "test_user"},
            description="Detect emotion from user actions"
        )
        
        # 3. GET /api/jeeves-eq/psychology-profile/test_user
        await self.test_endpoint(
            "GET", "/jeeves-eq/psychology-profile/test_user",
            description="Get psychology profile"
        )
        
        # 4. POST /api/jeeves-eq/pomodoro/start?user_id=test_user&session_type=work
        await self.test_endpoint(
            "POST", "/jeeves-eq/pomodoro/start",
            params={"user_id": "test_user", "session_type": "work"},
            description="Start Pomodoro session"
        )

    async def run_all_tests(self):
        """Run all test suites"""
        print(f"🚀 STARTING CODEDOCK v11.8 BACKEND API TESTING")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print(f"Test started at: {datetime.now().isoformat()}")
        
        # Run test suites
        await self.test_export_github_integration()
        await self.test_reading_curriculum()
        await self.test_jeeves_eq()
        
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
        export_tests = [r for r in self.results if r["endpoint"].startswith("/export")]
        reading_tests = [r for r in self.results if r["endpoint"].startswith("/reading")]
        jeeves_tests = [r for r in self.results if r["endpoint"].startswith("/jeeves-eq")]
        
        print(f"\n📊 RESULTS BY CATEGORY:")
        print(f"Export & GitHub Integration: {sum(1 for r in export_tests if r['success'])}/{len(export_tests)} passed")
        print(f"Reading Curriculum: {sum(1 for r in reading_tests if r['success'])}/{len(reading_tests)} passed")
        print(f"Jeeves EQ: {sum(1 for r in jeeves_tests if r['success'])}/{len(jeeves_tests)} passed")
        
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
                    if "total_curriculum_hours" in data:
                        print(f"    Total Hours: {data['total_curriculum_hours']}")
                    if "tracks" in data and isinstance(data["tracks"], list):
                        print(f"    Tracks: {len(data['tracks'])}")
                    if "capabilities" in data and isinstance(data["capabilities"], list):
                        print(f"    Capabilities: {len(data['capabilities'])}")
                    if "emotional_state" in data:
                        print(f"    Detected Emotion: {data['emotional_state'].get('primary', 'unknown')}")
        
        print(f"\n🎯 CONCLUSION:")
        if success_rate >= 90:
            print("🏆 EXCELLENT! All major endpoints are working correctly.")
        elif success_rate >= 75:
            print("✅ GOOD! Most endpoints are working with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE! Some endpoints need attention.")
        else:
            print("🚨 CRITICAL! Multiple endpoints are failing.")
        
        await self.client.aclose()

async def main():
    """Main test runner"""
    tester = CodeDockTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())