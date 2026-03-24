#!/usr/bin/env python3
"""
CodeDock Backend API Testing Suite
Testing Quiz Bank, Logscraper, and Jeeves Adaptive Tutoring APIs
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

def test_quiz_bank_api(tester: APITester):
    """Test Quiz Bank API endpoints"""
    print("🧠 TESTING QUIZ BANK API")
    print("=" * 50)
    
    # 1. GET /api/quiz-bank/info
    info_data = tester.test_get("/api/quiz-bank/info", 
                               expected_keys=["name", "total_quizzes", "categories"])
    
    if info_data:
        print(f"    Quiz Bank Info: {info_data.get('name', 'Unknown')}")
        print(f"    Total Quizzes: {info_data.get('total_quizzes', 0)}")
        categories = info_data.get('categories', {})
        for subject, topics in categories.items():
            print(f"    {subject.title()}: {len(topics) if isinstance(topics, list) else 'N/A'} categories")
    
    # 2. GET /api/quiz-bank/physics?count=3
    physics_data = tester.test_get("/api/quiz-bank/physics?count=3",
                                   expected_keys=["subject", "questions", "total_questions"])
    
    if physics_data:
        questions = physics_data.get('questions', [])
        print(f"    Physics Quizzes Retrieved: {len(questions)}")
        if questions:
            print(f"    Sample Question: {questions[0].get('question', 'N/A')[:50]}...")
    
    # 3. GET /api/quiz-bank/math?count=3
    math_data = tester.test_get("/api/quiz-bank/math?count=3",
                                expected_keys=["subject", "questions", "total_questions"])
    
    if math_data:
        questions = math_data.get('questions', [])
        print(f"    Math Quizzes Retrieved: {len(questions)}")
        if questions:
            print(f"    Sample Question: {questions[0].get('question', 'N/A')[:50]}...")
    
    # 4. GET /api/quiz-bank/cs?count=3
    cs_data = tester.test_get("/api/quiz-bank/cs?count=3",
                              expected_keys=["subject", "questions", "total_questions"])
    
    if cs_data:
        questions = cs_data.get('questions', [])
        print(f"    CS Quizzes Retrieved: {len(questions)}")
        if questions:
            print(f"    Sample Question: {questions[0].get('question', 'N/A')[:50]}...")

def test_logscraper_api(tester: APITester):
    """Test Logscraper API endpoints"""
    print("📊 TESTING LOGSCRAPER API")
    print("=" * 50)
    
    # 1. GET /api/logscraper/info
    info_data = tester.test_get("/api/logscraper/info",
                                expected_keys=["name", "capabilities", "tracked_actions"])
    
    if info_data:
        print(f"    Logscraper: {info_data.get('name', 'Unknown')}")
        capabilities = info_data.get('capabilities', [])
        print(f"    Capabilities: {len(capabilities)}")
        tracked = info_data.get('tracked_actions', {})
        print(f"    Total Tracked Actions: {tracked.get('total', 0)}")
    
    # 2. POST /api/logscraper/log
    log_payload = {
        "user_id": "test_user_123",
        "action_type": "lesson_completed",
        "action_data": {
            "topic": "python_basics",
            "duration_minutes": 15
        }
    }
    
    log_data = tester.test_post("/api/logscraper/log", log_payload,
                                expected_keys=["logged", "action_id", "timestamp"])
    
    if log_data:
        print(f"    Action Logged: {log_data.get('logged', False)}")
        print(f"    Action ID: {log_data.get('action_id', 'N/A')}")
    
    # 3. GET /api/logscraper/profile/test_user_123
    profile_data = tester.test_get("/api/logscraper/profile/test_user_123",
                                   expected_keys=["user_id", "profile"])
    
    if profile_data:
        print(f"    User Profile Retrieved: {profile_data.get('user_id', 'N/A')}")
        profile = profile_data.get('profile', {})
        if profile:
            print(f"    Study Time: {profile.get('total_study_time_minutes', 0)} minutes")
            print(f"    Topics Studied: {len(profile.get('topics_studied', []))}")

def test_jeeves_api(tester: APITester):
    """Test Jeeves Adaptive Tutoring API endpoints"""
    print("🎩 TESTING JEEVES ADAPTIVE TUTORING API")
    print("=" * 50)
    
    # 1. GET /api/jeeves/info
    info_data = tester.test_get("/api/jeeves/info",
                                expected_keys=["name", "capabilities", "personalities"])
    
    if info_data:
        print(f"    Jeeves: {info_data.get('name', 'Unknown')} {info_data.get('version', '')}")
        print(f"    Title: {info_data.get('title', 'N/A')}")
        capabilities = info_data.get('capabilities', [])
        print(f"    Capabilities: {len(capabilities)}")
        personalities = info_data.get('personalities', {})
        print(f"    Personalities: {len(personalities)}")
        languages = info_data.get('languages_fluent', [])
        print(f"    Languages: {len(languages)}")
    
    # 2. GET /api/jeeves/knowledge-base
    kb_data = tester.test_get("/api/jeeves/knowledge-base",
                              expected_keys=["name", "total_hours", "subjects"])
    
    if kb_data:
        print(f"    Knowledge Base: {kb_data.get('name', 'Unknown')}")
        print(f"    Total Hours: {kb_data.get('total_hours', 0)}")
        subjects = kb_data.get('subjects', {})
        for subject, info in subjects.items():
            hours = info.get('hours', 0) if isinstance(info, dict) else 0
            print(f"    {subject.title()}: {hours} hours")
    
    # 3. GET /api/jeeves/user-learning-summary/test_user_123
    summary_data = tester.test_get("/api/jeeves/user-learning-summary/test_user_123",
                                   expected_keys=["user_id", "status"])
    
    if summary_data:
        print(f"    User Summary: {summary_data.get('user_id', 'N/A')}")
        print(f"    Status: {summary_data.get('status', 'Unknown')}")
        if 'profile_summary' in summary_data:
            profile = summary_data['profile_summary']
            print(f"    Engagement Score: {profile.get('engagement_score', 0)}")
            print(f"    Learning Style: {profile.get('learning_style', 'Unknown')}")

def main():
    """Main testing function"""
    print("🚀 CODEDOCK BACKEND API TESTING SUITE")
    print("=" * 60)
    print(f"Testing Backend: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    print()
    
    tester = APITester(BASE_URL)
    
    # Test all three API groups
    test_quiz_bank_api(tester)
    print()
    test_logscraper_api(tester)
    print()
    test_jeeves_api(tester)
    
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