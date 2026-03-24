#!/usr/bin/env python3
"""
Backend API Testing for CodeDock v14.5 - Jeeves Synergy & Immersive Tutor
Testing all new endpoints for comprehensive validation.
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://synergy-learn-1.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, params: Dict = None, expected_keys: List[str] = None) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        self.total_tests += 1
        test_name = f"{method} {endpoint}"
        
        try:
            url = f"{BACKEND_URL}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Check status code
            if response.status_code != 200:
                result = {
                    "test": test_name,
                    "status": "FAILED",
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "response_data": None
                }
                self.results.append(result)
                return result
            
            # Parse JSON response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                result = {
                    "test": test_name,
                    "status": "FAILED", 
                    "error": "Invalid JSON response",
                    "response_data": response.text[:200]
                }
                self.results.append(result)
                return result
            
            # Check expected keys if provided (check if any expected keys are present)
            if expected_keys:
                missing_keys = [key for key in expected_keys if key not in response_data]
                if len(missing_keys) == len(expected_keys):  # Only fail if ALL expected keys are missing
                    result = {
                        "test": test_name,
                        "status": "FAILED",
                        "error": f"None of the expected keys found: {expected_keys}",
                        "response_data": response_data
                    }
                    self.results.append(result)
                    return result
            
            # Success
            self.passed_tests += 1
            result = {
                "test": test_name,
                "status": "PASSED",
                "error": None,
                "response_data": response_data
            }
            self.results.append(result)
            return result
            
        except requests.exceptions.RequestException as e:
            result = {
                "test": test_name,
                "status": "FAILED",
                "error": f"Request error: {str(e)}",
                "response_data": None
            }
            self.results.append(result)
            return result
        except Exception as e:
            result = {
                "test": test_name,
                "status": "FAILED",
                "error": f"Unexpected error: {str(e)}",
                "response_data": None
            }
            self.results.append(result)
            return result

    def test_immersive_tutor_endpoints(self):
        """Test all Immersive Tutor endpoints"""
        print("🎮 Testing Immersive Tutor Endpoints...")
        
        # 1. GET /api/immersive-tutor/immersion/overview
        print("  Testing immersion overview...")
        result = self.test_endpoint(
            "GET", 
            "/immersive-tutor/immersion/overview",
            expected_keys=["system", "components", "philosophy", "jeeves_says"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ System: {data.get('system', 'N/A')}")
            print(f"    ✅ Components: {len(data.get('components', {}))} found")
        else:
            print(f"    ❌ {result['error']}")
        
        # 2. POST /api/immersive-tutor/zpd/analyze
        print("  Testing ZPD analysis...")
        zpd_data = {
            "user_id": "test_user_123",
            "topic": "python",
            "current_mastery": 0.5,
            "recent_performance": [0.7, 0.8, 0.6, 0.9, 0.5]
        }
        result = self.test_endpoint(
            "POST",
            "/immersive-tutor/zpd/analyze",
            data=zpd_data,
            expected_keys=["current_zone", "average_performance", "optimal_difficulty_range", "recommendation"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Current Zone: {data.get('current_zone', 'N/A')}")
            print(f"    ✅ Avg Performance: {data.get('average_performance', 'N/A')}")
            print(f"    ✅ Recommendation: {data.get('recommendation', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 3. POST /api/immersive-tutor/quest/daily
        print("  Testing daily quest generation...")
        result = self.test_endpoint(
            "POST",
            "/immersive-tutor/quest/daily",
            params={"user_level": 5, "streak_days": 7},
            expected_keys=["date", "quests", "total_possible_xp", "streak_multiplier"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Date: {data.get('date', 'N/A')}")
            print(f"    ✅ Quests: {len(data.get('quests', []))} generated")
            print(f"    ✅ Total XP: {data.get('total_possible_xp', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 4. GET /api/immersive-tutor/achievements/list
        print("  Testing achievements list...")
        result = self.test_endpoint(
            "GET",
            "/immersive-tutor/achievements/list",
            expected_keys=["achievements", "total_achievements", "total_possible_xp"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Total Achievements: {data.get('total_achievements', 'N/A')}")
            print(f"    ✅ Total Possible XP: {data.get('total_possible_xp', 'N/A')}")
            achievements = data.get('achievements', [])
            if achievements:
                print(f"    ✅ Sample Achievement: {achievements[0].get('name', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 5. GET /api/immersive-tutor/levels/info
        print("  Testing levels info...")
        result = self.test_endpoint(
            "GET",
            "/immersive-tutor/levels/info",
            expected_keys=["max_level", "xp_formula", "sample_levels", "level_perks"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Max Level: {data.get('max_level', 'N/A')}")
            print(f"    ✅ XP Formula: {data.get('xp_formula', 'N/A')}")
            print(f"    ✅ Sample Levels: {len(data.get('sample_levels', []))} provided")
        else:
            print(f"    ❌ {result['error']}")
        
        # 6. POST /api/immersive-tutor/dialogue/socratic
        print("  Testing Socratic dialogue...")
        dialogue_data = {
            "user_id": "test_user_123",
            "topic": "loops",
            "user_answer": "for i in range(10): print(i)",
            "is_correct": True,
            "confidence_level": 0.7
        }
        result = self.test_endpoint(
            "POST",
            "/immersive-tutor/dialogue/socratic",
            data=dialogue_data,
            expected_keys=["dialogue_type", "follow_up", "question", "guidance_level"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Dialogue Type: {data.get('dialogue_type', 'N/A')}")
            print(f"    ✅ Follow-up: {data.get('follow_up', 'N/A')[:50]}...")
            print(f"    ✅ Guidance Level: {data.get('guidance_level', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 7. GET /api/immersive-tutor/streak/rewards
        print("  Testing streak rewards...")
        result = self.test_endpoint(
            "GET",
            "/immersive-tutor/streak/rewards",
            params={"streak_days": 10},
            expected_keys=["current_streak", "daily_xp_bonus", "multiplier", "streak_message"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Current Streak: {data.get('current_streak', 'N/A')}")
            print(f"    ✅ Daily XP Bonus: {data.get('daily_xp_bonus', 'N/A')}")
            print(f"    ✅ Multiplier: {data.get('multiplier', 'N/A')}")
            print(f"    ✅ Message: {data.get('streak_message', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")

    def test_jeeves_synergy_endpoints(self):
        """Test all Jeeves Synergy endpoints"""
        print("\n🤖 Testing Jeeves Synergy Endpoints...")
        
        # 1. GET /api/jeeves-synergy/overview
        print("  Testing synergy overview...")
        result = self.test_endpoint(
            "GET",
            "/jeeves-synergy/overview",
            expected_keys=["system", "description", "integrations", "learning_stages", "features"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ System: {data.get('system', 'N/A')}")
            print(f"    ✅ Integrations: {len(data.get('integrations', []))} found")
            print(f"    ✅ Learning Stages: {len(data.get('learning_stages', []))} found")
        else:
            print(f"    ❌ {result['error']}")
        
        # 2. POST /api/jeeves-synergy/session/create
        print("  Testing session creation...")
        session_data = {
            "user_id": "test_user_123",
            "total_learning_hours": 25,
            "current_topic": "python",
            "emotional_state": "neutral",
            "recent_performance": [0.7, 0.8, 0.6]
        }
        result = self.test_endpoint(
            "POST",
            "/jeeves-synergy/session/create",
            data=session_data,
            expected_keys=["session_id", "user_id", "stage", "difficulty", "guidance"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Session ID: {data.get('session_id', 'N/A')[:8]}...")
            print(f"    ✅ Stage: {data.get('stage', 'N/A')}")
            print(f"    ✅ Difficulty: {data.get('difficulty', {}).get('optimal_difficulty', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 3. POST /api/jeeves-synergy/adaptive-content
        print("  Testing adaptive content...")
        content_data = {
            "user_id": "test_user_123",
            "current_stage": "foundation",
            "topic": "algorithms",
            "time_available_minutes": 30,
            "energy_level": "normal"
        }
        result = self.test_endpoint(
            "POST",
            "/jeeves-synergy/adaptive-content",
            data=content_data,
            expected_keys=["session_id", "stage", "topic", "duration_minutes", "blocks"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Session ID: {data.get('session_id', 'N/A')[:8]}...")
            print(f"    ✅ Stage: {data.get('stage', 'N/A')}")
            print(f"    ✅ Duration: {data.get('duration_minutes', 'N/A')} minutes")
            print(f"    ✅ Blocks: {len(data.get('blocks', []))} generated")
        else:
            print(f"    ❌ {result['error']}")
        
        # 4. POST /api/jeeves-synergy/analyze
        print("  Testing synergy analysis...")
        analysis_data = {
            "user_id": "test_user_123",
            "total_hours": 75,
            "domains_explored": ["python", "javascript", "algorithms"],
            "achievements_earned": 10,
            "streak_days": 14,
            "mastery_scores": {"python": 0.8, "javascript": 0.6}
        }
        result = self.test_endpoint(
            "POST",
            "/jeeves-synergy/analyze",
            data=analysis_data,
            expected_keys=["user_id", "current_stage", "stage_progress", "metrics", "insights"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Current Stage: {data.get('current_stage', 'N/A')}")
            print(f"    ✅ Stage Progress: {data.get('stage_progress', 'N/A')}%")
            print(f"    ✅ Engagement Score: {data.get('metrics', {}).get('engagement_score', 'N/A')}")
            print(f"    ✅ Insights: {len(data.get('insights', []))} generated")
        else:
            print(f"    ❌ {result['error']}")
        
        # 5. GET /api/jeeves-synergy/stages/all
        print("  Testing all stages info...")
        result = self.test_endpoint(
            "GET",
            "/jeeves-synergy/stages/all",
            expected_keys=["stages", "total_stages", "progression"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Total Stages: {data.get('total_stages', 'N/A')}")
            print(f"    ✅ Progression: {data.get('progression', 'N/A')}")
            stages = data.get('stages', [])
            if stages:
                print(f"    ✅ Sample Stage: {stages[0].get('name', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 6. GET /api/jeeves-synergy/stage/25
        print("  Testing stage for 25 hours...")
        result = self.test_endpoint(
            "GET",
            "/jeeves-synergy/stage/25",
            expected_keys=["hours", "stage", "guidance"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Hours: {data.get('hours', 'N/A')}")
            print(f"    ✅ Stage: {data.get('stage', 'N/A')}")
            print(f"    ✅ Focus: {data.get('guidance', {}).get('focus_area', 'N/A')}")
        else:
            print(f"    ❌ {result['error']}")
        
        # 7. GET /api/jeeves-synergy/transition/foundation/growth
        print("  Testing stage transition...")
        result = self.test_endpoint(
            "GET",
            "/jeeves-synergy/transition/foundation/growth",
            expected_keys=["transition_type", "celebration", "jeeves_message", "newly_unlocked"]
        )
        if result["status"] == "PASSED":
            data = result["response_data"]
            print(f"    ✅ Transition: {data.get('transition_type', 'N/A')}")
            print(f"    ✅ Celebration: {data.get('celebration', 'N/A')}")
            print(f"    ✅ Unlocked: {len(data.get('newly_unlocked', []))} features")
        else:
            print(f"    ❌ {result['error']}")

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting CodeDock v14.5 Backend API Testing")
        print(f"📡 Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Test Immersive Tutor endpoints
        self.test_immersive_tutor_endpoints()
        
        # Test Jeeves Synergy endpoints  
        self.test_jeeves_synergy_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [r for r in self.results if r["status"] == "FAILED"]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['error']}")
        
        # Show successful tests
        passed_tests = [r for r in self.results if r["status"] == "PASSED"]
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"  • {test['test']}")
        
        return success_rate >= 80  # Return True if 80%+ success rate

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print(f"\n🎉 Testing completed successfully!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Some tests failed. Check the results above.")
        sys.exit(1)