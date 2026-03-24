#!/usr/bin/env python3
"""
Backend API Testing for Jeeves Voice & Personality API v13.5
Testing all 8 endpoints as specified in the review request
"""

import requests
import json
import sys
from typing import Dict, Any

# Base URL from the review request
BASE_URL = "https://sota-2026.preview.emergentagent.com"

class JeevesVoiceTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data
        }
        self.results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response keys: {list(response_data.keys())}")
        print()
        
    def test_personality_profile(self):
        """Test GET /api/jeeves-voice/personality"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/personality"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check actual response structure
                if "name" in data and "traits" in data and "voice" in data:
                    name = data.get("name", "unknown")
                    traits_count = len(data.get("traits", []))
                    voice_info = data.get("voice", {})
                    self.log_result("GET Personality Profile", True, 
                                  f"Returns {name} personality with {traits_count} traits and voice configuration", data)
                else:
                    self.log_result("GET Personality Profile", False, 
                                  f"Unexpected response structure", data)
            else:
                self.log_result("GET Personality Profile", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Personality Profile", False, f"Exception: {str(e)}")
    
    def test_voice_settings(self):
        """Test GET /api/jeeves-voice/voice/settings"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/voice/settings"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify expected fields for voice settings
                expected_fields = ["voice_model", "tone", "speed", "pitch"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("GET Voice Settings", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    voice_model = data.get("voice_model", "unknown")
                    tone = data.get("tone", "unknown")
                    self.log_result("GET Voice Settings", True, 
                                  f"Voice model: {voice_model}, tone: {tone}", data)
            else:
                self.log_result("GET Voice Settings", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Voice Settings", False, f"Exception: {str(e)}")
    
    def test_direction_types(self):
        """Test GET /api/jeeves-voice/direction/types"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/direction/types"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if "direction_types" in data and isinstance(data["direction_types"], list):
                    types_count = len(data["direction_types"])
                    if types_count > 0:
                        # Check if learning_path and recovery are included
                        types_list = data["direction_types"]
                        has_learning_path = "learning_path" in types_list
                        has_recovery = "recovery" in types_list
                        
                        self.log_result("GET Direction Types", True, 
                                      f"Returns {types_count} direction types (learning_path: {has_learning_path}, recovery: {has_recovery})", data)
                    else:
                        self.log_result("GET Direction Types", False, "No direction types returned", data)
                else:
                    self.log_result("GET Direction Types", False, "Invalid response structure", data)
            else:
                self.log_result("GET Direction Types", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Direction Types", False, f"Exception: {str(e)}")
    
    def test_direction_learning_path(self):
        """Test POST /api/jeeves-voice/direction (learning path)"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/direction"
            payload = {
                "user_id": "test_user",
                "direction_type": "learning_path",
                "mastery_level": 0.5,
                "streak_days": 5,
                "emotional_state": "neutral",
                "time_available_minutes": 30,
                "current_topic": "algorithms"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["direction", "voice_response", "personality_context"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("POST Direction (Learning Path)", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    direction = data.get("direction", "")
                    voice_response = data.get("voice_response", "")
                    self.log_result("POST Direction (Learning Path)", True, 
                                  f"Generated learning path direction with voice response ({len(voice_response)} chars)", data)
            else:
                self.log_result("POST Direction (Learning Path)", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("POST Direction (Learning Path)", False, f"Exception: {str(e)}")
    
    def test_direction_recovery(self):
        """Test POST /api/jeeves-voice/direction (recovery with frustration)"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/direction"
            payload = {
                "user_id": "test_user",
                "direction_type": "recovery",
                "emotional_state": "frustrated"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["direction", "voice_response", "personality_context"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("POST Direction (Recovery)", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    direction = data.get("direction", "")
                    voice_response = data.get("voice_response", "")
                    emotional_context = data.get("personality_context", {}).get("emotional_state", "unknown")
                    self.log_result("POST Direction (Recovery)", True, 
                                  f"Generated recovery direction for {emotional_context} state with voice response ({len(voice_response)} chars)", data)
            else:
                self.log_result("POST Direction (Recovery)", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("POST Direction (Recovery)", False, f"Exception: {str(e)}")
    
    def test_greeting(self):
        """Test GET /api/jeeves-voice/greet"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/greet"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["greeting", "voice_response", "personality_tone"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("GET Greeting", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    greeting = data.get("greeting", "")
                    voice_response = data.get("voice_response", "")
                    tone = data.get("personality_tone", "unknown")
                    self.log_result("GET Greeting", True, 
                                  f"Generated greeting with {tone} tone ({len(voice_response)} chars voice response)", data)
            else:
                self.log_result("GET Greeting", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Greeting", False, f"Exception: {str(e)}")
    
    def test_encouragement(self):
        """Test GET /api/jeeves-voice/encourage"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/encourage"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["encouragement", "voice_response", "motivational_context"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("GET Encouragement", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    encouragement = data.get("encouragement", "")
                    voice_response = data.get("voice_response", "")
                    context = data.get("motivational_context", {})
                    self.log_result("GET Encouragement", True, 
                                  f"Generated encouragement with voice response ({len(voice_response)} chars)", data)
            else:
                self.log_result("GET Encouragement", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Encouragement", False, f"Exception: {str(e)}")
    
    def test_farewell(self):
        """Test GET /api/jeeves-voice/farewell"""
        try:
            url = f"{self.base_url}/api/jeeves-voice/farewell"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["farewell", "voice_response", "session_summary"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("GET Farewell", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    farewell = data.get("farewell", "")
                    voice_response = data.get("voice_response", "")
                    summary = data.get("session_summary", {})
                    self.log_result("GET Farewell", True, 
                                  f"Generated farewell with voice response ({len(voice_response)} chars) and session summary", data)
            else:
                self.log_result("GET Farewell", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("GET Farewell", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all Jeeves Voice & Personality API v13.5 tests"""
        print("=" * 80)
        print("JEEVES VOICE & PERSONALITY API v13.5 TESTING")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print()
        
        # Run all tests in order
        self.test_personality_profile()
        self.test_voice_settings()
        self.test_direction_types()
        self.test_direction_learning_path()
        self.test_direction_recovery()
        self.test_greeting()
        self.test_encouragement()
        self.test_farewell()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        print()
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Jeeves Voice & Personality API v13.5 is fully functional.")
        else:
            print("❌ Some tests failed. Details above.")
            failed_tests = [r["test"] for r in self.results if not r["success"]]
            print(f"Failed tests: {', '.join(failed_tests)}")
        
        return passed, total

if __name__ == "__main__":
    tester = JeevesVoiceTester()
    passed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)