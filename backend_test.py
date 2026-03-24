#!/usr/bin/env python3
"""
CodeDock v12.0 Backend API Testing Suite
Testing v12.0 features as requested in review:
- Core endpoints (health, languages, ai/modes)
- New v12.0 features (logscraper, export)
- Reading curriculum
- Jeeves EQ
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from pathlib import Path

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://sota-2026.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"
USER_ID = "default_user"

class CodeDockV12Tester:
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

    async def test_core_endpoints(self):
        """Test core endpoints: health, languages, ai/modes"""
        print("\n🏥 TESTING CORE ENDPOINTS")
        print("=" * 60)
        
        # GET /api/health - Verify server health
        result = await self.test_endpoint(
            "GET", "/health",
            description="Server health check"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            status = data.get("status", "unknown")
            print(f"   Health Status: {status}")
        
        # GET /api/languages - Get available programming languages
        result = await self.test_endpoint(
            "GET", "/languages",
            description="Available programming languages"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            if isinstance(data, list):
                print(f"   Found {len(data)} languages")
                executable_count = sum(1 for lang in data if lang.get("executable", False))
                print(f"   Executable languages: {executable_count}")
            elif isinstance(data, dict) and "languages" in data:
                languages = data["languages"]
                print(f"   Found {len(languages)} languages")
                executable_count = sum(1 for lang in languages if lang.get("executable", False))
                print(f"   Executable languages: {executable_count}")
        
        # GET /api/ai/modes - Get AI modes
        result = await self.test_endpoint(
            "GET", "/ai/modes",
            description="AI assistant modes"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            if isinstance(data, list):
                print(f"   Found {len(data)} AI modes")
            elif isinstance(data, dict) and "modes" in data:
                modes = data["modes"]
                print(f"   Found {len(modes)} AI modes")
        
        return True

    async def test_v12_features(self):
        """Test new v12.0 features"""
        print("\n🚀 TESTING v12.0 NEW FEATURES")
        print("=" * 60)
        
        # GET /api/logscraper/profile/{user_id} - Test AI interaction profile
        result = await self.test_endpoint(
            "GET", f"/logscraper/profile/{USER_ID}",
            description="AI interaction profile for user"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            print(f"   Profile data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        # GET /api/logscraper/insights/{user_id} - Test AI insights
        result = await self.test_endpoint(
            "GET", f"/logscraper/insights/{USER_ID}",
            description="AI insights for user"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            print(f"   Insights data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        # GET /api/export/ai-interactions/{user_id} - Test AI interaction export
        result = await self.test_endpoint(
            "GET", f"/export/ai-interactions/{USER_ID}",
            description="AI interaction export for user"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            print(f"   Export data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            if isinstance(data, dict) and "interactions" in data:
                interactions = data["interactions"]
                print(f"   Total interactions: {len(interactions) if isinstance(interactions, list) else 'Not a list'}")
        
        return True

    async def test_reading_curriculum(self):
        """Test reading curriculum endpoints"""
        print("\n📚 TESTING READING CURRICULUM")
        print("=" * 60)
        
        # GET /api/reading/info - Get reading curriculum info
        result = await self.test_endpoint(
            "GET", "/reading/info",
            description="Reading curriculum info"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            if isinstance(data, dict):
                total_hours = data.get("total_curriculum_hours", 0)
                tracks = data.get("knowledge_tracks", [])
                print(f"   Total curriculum hours: {total_hours}")
                print(f"   Knowledge tracks: {len(tracks)}")
        
        # GET /api/reading/tracks - Get all learning tracks
        result = await self.test_endpoint(
            "GET", "/reading/tracks",
            description="All learning tracks"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            if isinstance(data, dict) and "tracks" in data:
                tracks = data["tracks"]
                print(f"   Found {len(tracks)} tracks")
                for track in tracks[:3]:  # Show first 3
                    name = track.get("name", "Unknown")
                    hours = track.get("total_hours", 0)
                    print(f"   - {name}: {hours} hours")
        
        return True

    async def test_jeeves_eq(self):
        """Test Jeeves EQ endpoints"""
        print("\n🧠 TESTING JEEVES EQ")
        print("=" * 60)
        
        # GET /api/jeeves-eq/info - Get Jeeves EQ info
        result = await self.test_endpoint(
            "GET", "/jeeves-eq/info",
            description="Jeeves EQ system info"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            if isinstance(data, dict):
                capabilities = data.get("capabilities", [])
                emotional_states = data.get("emotional_states_detected", [])
                print(f"   Capabilities: {len(capabilities)}")
                print(f"   Emotional states detected: {len(emotional_states)}")
        
        # POST /api/jeeves-eq/detect-emotion - Test emotion detection
        # This endpoint expects query parameters, not JSON body
        params = {
            "user_id": USER_ID,
            "text_input": "I'm feeling frustrated with this coding challenge. I've been stuck for hours."
        }
        
        # The recent_actions should be passed as the body (list)
        recent_actions = [
            {"action_type": "challenge_failed", "timestamp": "2026-03-24T06:45:00Z"},
            {"action_type": "hint_requested", "timestamp": "2026-03-24T06:45:30Z"},
            {"action_type": "challenge_failed", "timestamp": "2026-03-24T06:46:00Z"}
        ]
        
        result = await self.test_endpoint(
            "POST", "/jeeves-eq/detect-emotion",
            data=recent_actions,
            params=params,
            description="Emotion detection from user actions and text"
        )
        
        if result["success"] and "response_data" in result:
            data = result["response_data"]
            print(f"   Emotion detection data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            if isinstance(data, dict) and "emotional_state" in data:
                emotion_state = data["emotional_state"]
                primary = emotion_state.get("primary", "unknown")
                intensity = emotion_state.get("intensity", 0)
                print(f"   Detected emotion: {primary} (intensity: {intensity})")
        
        return True

    async def run_all_tests(self):
        """Run all test suites"""
        print(f"🚀 STARTING CODEDOCK v12.0 BACKEND API TESTING")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print(f"User ID: {USER_ID}")
        print(f"Test started at: {datetime.now().isoformat()}")
        
        # Run all test suites as requested
        await self.test_core_endpoints()
        await self.test_v12_features()
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
        core_tests = [r for r in self.results if r["endpoint"] in ["/health", "/languages", "/ai/modes"]]
        v12_tests = [r for r in self.results if r["endpoint"].startswith("/logscraper") or r["endpoint"].startswith("/export")]
        reading_tests = [r for r in self.results if r["endpoint"].startswith("/reading")]
        jeeves_tests = [r for r in self.results if r["endpoint"].startswith("/jeeves-eq")]
        
        print(f"\n📊 RESULTS BY CATEGORY:")
        print(f"Core Endpoints: {sum(1 for r in core_tests if r['success'])}/{len(core_tests)} passed")
        print(f"v12.0 Features: {sum(1 for r in v12_tests if r['success'])}/{len(v12_tests)} passed")
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
                    if "status" in data:
                        print(f"    Status: {data['status']}")
                    if "languages" in data and isinstance(data["languages"], list):
                        print(f"    Languages: {len(data['languages'])}")
                    if "modes" in data and isinstance(data["modes"], list):
                        print(f"    AI Modes: {len(data['modes'])}")
                    if "interactions" in data and isinstance(data["interactions"], list):
                        print(f"    Interactions: {len(data['interactions'])}")
                    if "emotion" in data:
                        print(f"    Detected Emotion: {data['emotion']}")
        
        print(f"\n🎯 CONCLUSION:")
        if success_rate >= 90:
            print("🏆 EXCELLENT! All v12.0 backend endpoints are working correctly.")
        elif success_rate >= 75:
            print("✅ GOOD! Most v12.0 backend endpoints are working with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE! Some v12.0 backend endpoints need attention.")
        else:
            print("🚨 CRITICAL! Multiple v12.0 backend endpoints are failing.")
        
        await self.client.aclose()

async def main():
    """Main test runner"""
    tester = CodeDockV12Tester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())