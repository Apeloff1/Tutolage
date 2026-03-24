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
                
                # Check actual response structure
                if "voice" in data and "character" in data:
                    voice_info = data.get("voice", {})
                    character = data.get("character", "unknown")
                    speech_styles = len(data.get("speech_styles", []))
                    self.log_result("GET Voice Settings", True, 
                                  f"Voice settings for {character} with {speech_styles} speech styles", data)
                else:
                    self.log_result("GET Voice Settings", False, 
                                  f"Unexpected response structure", data)
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
                
                if "types" in data and isinstance(data["types"], list):
                    types_count = len(data["types"])
                    if types_count > 0:
                        # Check if learning_path and recovery are included
                        types_list = data["types"]
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
                
                # Check actual response structure
                if "type" in data and "jeeves_says" in data and "voice" in data:
                    direction_type = data.get("type", "unknown")
                    jeeves_response = data.get("jeeves_says", "")
                    voice_info = data.get("voice", {})
                    path_info = data.get("path", {})
                    self.log_result("POST Direction (Learning Path)", True, 
                                  f"Generated {direction_type} direction with Jeeves response ({len(jeeves_response)} chars) and voice configuration", data)
                else:
                    self.log_result("POST Direction (Learning Path)", False, 
                                  f"Unexpected response structure", data)
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
                
                # Check actual response structure
                if "type" in data and "jeeves_says" in data and "voice" in data:
                    direction_type = data.get("type", "unknown")
                    jeeves_response = data.get("jeeves_says", "")
                    voice_info = data.get("voice", {})
                    emotion_detected = data.get("emotion_detected", "unknown")
                    recovery_strategy = data.get("recovery_strategy", {})
                    self.log_result("POST Direction (Recovery)", True, 
                                  f"Generated {direction_type} direction for {emotion_detected} emotion with Jeeves response ({len(jeeves_response)} chars) and recovery strategy", data)
                else:
                    self.log_result("POST Direction (Recovery)", False, 
                                  f"Unexpected response structure", data)
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
                
                # Check actual response structure
                if "content" in data and "personality" in data and "voice" in data:
                    content = data.get("content", "")
                    personality = data.get("personality", "unknown")
                    voice_info = data.get("voice", {})
                    response_type = data.get("response_type", "unknown")
                    self.log_result("GET Greeting", True, 
                                  f"Generated {response_type} greeting with {personality} personality ({len(content)} chars) and voice configuration", data)
                else:
                    self.log_result("GET Greeting", False, 
                                  f"Unexpected response structure", data)
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
                
                # Check actual response structure
                if "content" in data and "personality" in data and "voice" in data:
                    content = data.get("content", "")
                    personality = data.get("personality", "unknown")
                    voice_info = data.get("voice", {})
                    response_type = data.get("response_type", "unknown")
                    self.log_result("GET Encouragement", True, 
                                  f"Generated {response_type} encouragement with {personality} personality ({len(content)} chars) and voice configuration", data)
                else:
                    self.log_result("GET Encouragement", False, 
                                  f"Unexpected response structure", data)
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
                
                # Check actual response structure
                if "content" in data and "personality" in data and "voice" in data:
                    content = data.get("content", "")
                    personality = data.get("personality", "unknown")
                    voice_info = data.get("voice", {})
                    response_type = data.get("response_type", "unknown")
                    self.log_result("GET Farewell", True, 
                                  f"Generated {response_type} farewell with {personality} personality ({len(content)} chars) and voice configuration", data)
                else:
                    self.log_result("GET Farewell", False, 
                                  f"Unexpected response structure", data)
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