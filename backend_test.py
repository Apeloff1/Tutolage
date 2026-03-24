#!/usr/bin/env python3
"""
CodeDock Backend API Testing Suite v11.7 SOTA
Testing Reading Curriculum, Jeeves EQ, and SOTA Extended APIs
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from frontend/.env
BASE_URL = "https://codedock-learn.preview.emergentagent.com"

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'CodeDock-Testing-Agent/1.0'
        })
        self.results = []
        
    def log_result(self, endpoint: str, method: str, status_code: int, 
                   response_data: Any, error: str = None, success: bool = True):
        """Log test result"""
        result = {
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'success': success,
            'error': error,
            'response_size': len(str(response_data)) if response_data else 0,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {method} {endpoint} - {status_code}")
        if error:
            print(f"    Error: {error}")
        elif response_data and isinstance(response_data, dict):
            # Print key info from response
            if 'name' in response_data:
                print(f"    Name: {response_data['name']}")
            if 'total' in response_data:
                print(f"    Total: {response_data['total']}")
            if 'capabilities' in response_data:
                print(f"    Capabilities: {len(response_data['capabilities'])}")
        print()
        
    def test_get(self, endpoint: str, expected_keys: List[str] = None) -> Dict[str, Any]:
        """Test GET endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for expected keys
                missing_keys = []
                if expected_keys:
                    for key in expected_keys:
                        if key not in data:
                            missing_keys.append(key)
                
                if missing_keys:
                    self.log_result(endpoint, "GET", response.status_code, data, 
                                  f"Missing keys: {missing_keys}", False)
                else:
                    self.log_result(endpoint, "GET", response.status_code, data, None, True)
                
                return data
            else:
                self.log_result(endpoint, "GET", response.status_code, None, 
                              f"HTTP {response.status_code}: {response.text}", False)
                return {}
                
        except Exception as e:
            self.log_result(endpoint, "GET", 0, None, str(e), False)
            return {}
    
    def test_post(self, endpoint: str, payload: Dict[str, Any], 
                  expected_keys: List[str] = None) -> Dict[str, Any]:
        """Test POST endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for expected keys
                missing_keys = []
                if expected_keys:
                    for key in expected_keys:
                        if key not in data:
                            missing_keys.append(key)
                
                if missing_keys:
                    self.log_result(endpoint, "POST", response.status_code, data, 
                                  f"Missing keys: {missing_keys}", False)
                else:
                    self.log_result(endpoint, "POST", response.status_code, data, None, True)
                
                return data
            else:
                self.log_result(endpoint, "POST", response.status_code, None, 
                              f"HTTP {response.status_code}: {response.text}", False)
                return {}
                
        except Exception as e:
            self.log_result(endpoint, "POST", 0, None, str(e), False)
            return {}

def test_reading_curriculum_api(tester: APITester):
    """Test Reading Curriculum API endpoints"""
    print("📚 TESTING READING CURRICULUM API")
    print("=" * 50)
    
    # 1. GET /api/reading/info
    info_data = tester.test_get("/api/reading/info", 
                               expected_keys=["name", "total_curriculum_hours", "knowledge_tracks", "manual_categories"])
    
    if info_data:
        print(f"    Reading System: {info_data.get('name', 'Unknown')}")
        print(f"    Total Hours: {info_data.get('total_curriculum_hours', 0)}")
        print(f"    Knowledge Tracks: {len(info_data.get('knowledge_tracks', []))}")
        print(f"    Manual Categories: {len(info_data.get('manual_categories', []))}")
        print(f"    Supported Languages: {info_data.get('supported_languages', 0)}")
    
    # 2. GET /api/reading/tracks
    tracks_data = tester.test_get("/api/reading/tracks",
                                  expected_keys=["tracks", "total_tracks"])
    
    if tracks_data:
        tracks = tracks_data.get('tracks', [])
        print(f"    Learning Tracks Retrieved: {len(tracks)}")
        for track in tracks[:4]:  # Show first 4 tracks
            print(f"      - {track.get('name', 'Unknown')}: {track.get('total_hours', 0)} hours")
    
    # 3. GET /api/reading/track/game_development
    track_data = tester.test_get("/api/reading/track/game_development",
                                 expected_keys=["track_id", "name", "sub_tracks"])
    
    if track_data:
        print(f"    Game Development Track: {track_data.get('name', 'Unknown')}")
        print(f"    Total Hours: {track_data.get('total_hours', 0)}")
        sub_tracks = track_data.get('sub_tracks', {})
        print(f"    Sub-tracks: {len(sub_tracks)}")
    
    # 4. GET /api/reading/manuals
    manuals_data = tester.test_get("/api/reading/manuals",
                                   expected_keys=["manuals", "language_manuals"])
    
    if manuals_data:
        manuals = manuals_data.get('manuals', [])
        lang_manuals = manuals_data.get('language_manuals', [])
        print(f"    Advanced Manuals: {len(manuals)}")
        print(f"    Language Manuals: {len(lang_manuals)}")


def test_jeeves_eq_api(tester: APITester):
    """Test Jeeves Emotional Intelligence API endpoints"""
    print("🧠 TESTING JEEVES EMOTIONAL INTELLIGENCE API")
    print("=" * 50)
    
    # 1. GET /api/jeeves-eq/info
    info_data = tester.test_get("/api/jeeves-eq/info",
                                expected_keys=["name", "capabilities", "emotional_states_detected"])
    
    if info_data:
        print(f"    Jeeves EQ: {info_data.get('name', 'Unknown')}")
        capabilities = info_data.get('capabilities', [])
        print(f"    Capabilities: {len(capabilities)}")
        emotions = info_data.get('emotional_states_detected', [])
        print(f"    Emotional States Detected: {len(emotions)}")
        therapeutic = info_data.get('therapeutic_features', [])
        print(f"    Therapeutic Features: {len(therapeutic)}")
    
    # 2. POST /api/jeeves-eq/detect-emotion
    emotion_data = tester.test_post("/api/jeeves-eq/detect-emotion?user_id=test_user", 
                                    [
                                        {"action_type": "challenge_failed"},
                                        {"action_type": "challenge_failed"},
                                        {"action_type": "challenge_failed"}
                                    ],
                                    expected_keys=["user_id", "emotional_state", "recommended_response_style"])
    
    if emotion_data:
        emotional_state = emotion_data.get('emotional_state', {})
        print(f"    Detected Emotion: {emotional_state.get('primary', 'Unknown')}")
        print(f"    Intensity: {emotional_state.get('intensity', 0):.2f}")
        print(f"    Response Style: {emotion_data.get('recommended_response_style', 'N/A')}")
    
    # 3. POST /api/jeeves-eq/therapeutic-response
    therapeutic_data = tester.test_post("/api/jeeves-eq/therapeutic-response?user_id=test_user&emotional_state=frustrated&intensity=0.7", {},
                                        expected_keys=["response", "emotional_state", "response_type"])
    
    if therapeutic_data:
        print(f"    Therapeutic Response Generated: {len(therapeutic_data.get('response', ''))} chars")
        print(f"    Response Type: {therapeutic_data.get('response_type', 'N/A')}")
    
    # 4. GET /api/jeeves-eq/psychology-profile/test_user
    profile_data = tester.test_get("/api/jeeves-eq/psychology-profile/test_user",
                                   expected_keys=["user_id", "profile"])
    
    if profile_data:
        print(f"    Psychology Profile: {profile_data.get('user_id', 'N/A')}")
        profile = profile_data.get('profile', {})
        print(f"    Motivation Type: {profile.get('motivation_type', 'Unknown')}")
        print(f"    Cognitive Style: {profile.get('cognitive_style', 'Unknown')}")
    
    # 5. POST /api/jeeves-eq/cognitive-load-check
    load_data = tester.test_post("/api/jeeves-eq/cognitive-load-check?user_id=test_user&session_duration_minutes=90&new_concepts_introduced=6&error_count=8&last_break_minutes_ago=60", {},
                                 expected_keys=["cognitive_load_level", "load_score"])
    
    if load_data:
        print(f"    Cognitive Load Level: {load_data.get('cognitive_load_level', 'Unknown')}")
        print(f"    Load Score: {load_data.get('load_score', 0):.2f}")
        print(f"    Break Recommended: {load_data.get('break_recommended', False)}")
    
    # 6. GET /api/jeeves-eq/wellness-reminder
    wellness_data = tester.test_get("/api/jeeves-eq/wellness-reminder",
                                    expected_keys=["type", "message"])
    
    if wellness_data:
        print(f"    Wellness Reminder Type: {wellness_data.get('type', 'Unknown')}")
        print(f"    Message Length: {len(wellness_data.get('message', ''))} chars")


def test_sota_extended_api(tester: APITester):
    """Test SOTA Extended API endpoints"""
    print("🚀 TESTING SOTA EXTENDED API")
    print("=" * 50)
    
    # 1. GET /api/sota-extended/info
    info_data = tester.test_get("/api/sota-extended/info",
                                expected_keys=["name", "total_upgrades", "high_priority", "categories"])
    
    if info_data:
        print(f"    SOTA Extended: {info_data.get('name', 'Unknown')}")
        print(f"    Version: {info_data.get('version', 'Unknown')}")
        print(f"    Total Upgrades: {info_data.get('total_upgrades', 0)}")
        print(f"    High Priority: {info_data.get('high_priority', 0)}")
        print(f"    Medium Priority: {info_data.get('medium_priority', 0)}")
        print(f"    Low Priority: {info_data.get('low_priority', 0)}")
        categories = info_data.get('categories', [])
        print(f"    Categories: {len(categories)}")
    
    # 2. GET /api/sota-extended/upgrades/high
    high_data = tester.test_get("/api/sota-extended/upgrades/high",
                                expected_keys=["upgrades"])
    
    if high_data:
        upgrades = high_data.get('upgrades', [])
        print(f"    High Priority Upgrades: {len(upgrades)}")
        for upgrade in upgrades[:3]:  # Show first 3
            print(f"      - {upgrade.get('name', 'Unknown')}: {upgrade.get('category', 'N/A')}")
    
    # 3. GET /api/sota-extended/upgrade/predictive_v2
    upgrade_data = tester.test_get("/api/sota-extended/upgrade/predictive_v2",
                                   expected_keys=["upgrade"])
    
    if upgrade_data:
        upgrade = upgrade_data.get('upgrade', {})
        print(f"    Predictive v2 Upgrade: {upgrade.get('name', 'Unknown')}")
        print(f"    Version: {upgrade.get('version', 'Unknown')}")
        print(f"    Category: {upgrade.get('category', 'Unknown')}")
        features = upgrade.get('features', [])
        print(f"    Features: {len(features)}")
    
    # 4. POST /api/sota-extended/apply/predictive_v2
    apply_payload = {"config": {"enabled": True, "intensity": "high"}}
    apply_data = tester.test_post("/api/sota-extended/apply/predictive_v2", apply_payload,
                                  expected_keys=["status", "upgrade", "applied_at"])
    
    if apply_data:
        print(f"    Apply Status: {apply_data.get('status', 'Unknown')}")
        print(f"    Applied At: {apply_data.get('applied_at', 'N/A')}")
        print(f"    Message: {apply_data.get('message', 'N/A')}")

def main():
    """Main testing function"""
    print("🚀 CODEDOCK v11.7 SOTA BACKEND API TESTING SUITE")
    print("=" * 60)
    print(f"Testing Backend: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    print()
    
    tester = APITester(BASE_URL)
    
    # Test all three v11.7 SOTA API groups
    test_reading_curriculum_api(tester)
    print()
    test_jeeves_eq_api(tester)
    print()
    test_sota_extended_api(tester)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TESTING SUMMARY")
    print("=" * 60)
    
    total_tests = len(tester.results)
    passed_tests = len([r for r in tester.results if r['success']])
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if failed_tests > 0:
        print("\n❌ FAILED TESTS:")
        for result in tester.results:
            if not result['success']:
                print(f"  - {result['method']} {result['endpoint']}: {result['error']}")
    
    print(f"\nCompleted at: {datetime.now().isoformat()}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)