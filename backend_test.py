#!/usr/bin/env python3
"""
Backend API Testing for Jeeves Hyperion v13.0 API
Testing all 7 endpoints as specified in the review request
"""

import requests
import json
import sys
from typing import Dict, Any

# Base URL from the review request
BASE_URL = "https://sota-2026.preview.emergentagent.com"

class JeevesHyperionTester:
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
        
    def test_knowledge_base_stats(self):
        """Test GET /api/jeeves-hyperion/knowledge-base/stats"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/knowledge-base/stats"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify expected fields
                expected_fields = ["version", "knowledge_expansion", "total_concepts", 
                                 "total_learning_hours", "domains", "sub_domains"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("Knowledge Base Stats", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    self.log_result("Knowledge Base Stats", True, 
                                  f"Returns {data.get('total_concepts', 0)} concepts across {data.get('domains', 0)} domains", data)
            else:
                self.log_result("Knowledge Base Stats", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Knowledge Base Stats", False, f"Exception: {str(e)}")
    
    def test_get_all_domains(self):
        """Test GET /api/jeeves-hyperion/knowledge-base/domains"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/knowledge-base/domains"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if "domains" in data and isinstance(data["domains"], list):
                    domain_count = len(data["domains"])
                    if domain_count > 0:
                        # Check first domain structure
                        first_domain = data["domains"][0]
                        expected_fields = ["id", "name", "total_concepts", "estimated_hours"]
                        missing_fields = [f for f in expected_fields if f not in first_domain]
                        
                        if missing_fields:
                            self.log_result("Get All Domains", False, 
                                          f"Domain missing fields: {missing_fields}", data)
                        else:
                            self.log_result("Get All Domains", True, 
                                          f"Returns {domain_count} domains with proper structure", data)
                    else:
                        self.log_result("Get All Domains", False, "No domains returned", data)
                else:
                    self.log_result("Get All Domains", False, "Invalid response structure", data)
            else:
                self.log_result("Get All Domains", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get All Domains", False, f"Exception: {str(e)}")
    
    def test_get_domain_details(self):
        """Test GET /api/jeeves-hyperion/knowledge-base/domain/core_programming"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/knowledge-base/domain/core_programming"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["id", "name", "total_concepts", "estimated_hours", "sub_domains"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("Get Domain Details", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    sub_domain_count = len(data.get("sub_domains", {}))
                    self.log_result("Get Domain Details", True, 
                                  f"Core programming domain with {data.get('total_concepts', 0)} concepts and {sub_domain_count} sub-domains", data)
            else:
                self.log_result("Get Domain Details", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get Domain Details", False, f"Exception: {str(e)}")
    
    def test_matrices_overview(self):
        """Test GET /api/jeeves-hyperion/matrices/overview"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/matrices/overview"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if "matrices" in data and isinstance(data["matrices"], list):
                    matrix_count = len(data["matrices"])
                    if matrix_count > 0:
                        # Check first matrix structure
                        first_matrix = data["matrices"][0]
                        expected_fields = ["id", "name", "description", "endpoint"]
                        missing_fields = [f for f in expected_fields if f not in first_matrix]
                        
                        if missing_fields:
                            self.log_result("Matrices Overview", False, 
                                          f"Matrix missing fields: {missing_fields}", data)
                        else:
                            self.log_result("Matrices Overview", True, 
                                          f"Returns {matrix_count} development matrices with proper structure", data)
                    else:
                        self.log_result("Matrices Overview", False, "No matrices returned", data)
                else:
                    self.log_result("Matrices Overview", False, "Invalid response structure", data)
            else:
                self.log_result("Matrices Overview", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Matrices Overview", False, f"Exception: {str(e)}")
    
    def test_mastery_score_calculation(self):
        """Test POST /api/jeeves-hyperion/self-learning/mastery-score"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/self-learning/mastery-score"
            params = {
                "correct_answers": 8,
                "total_attempts": 10,
                "time_spent_seconds": 300,
                "hint_usage": 1,
                "days_since_last_practice": 2
            }
            
            response = requests.post(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["mastery_score", "mastery_level", "components"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("Mastery Score Calculation", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    mastery_score = data.get("mastery_score", 0)
                    mastery_level = data.get("mastery_level", "unknown")
                    self.log_result("Mastery Score Calculation", True, 
                                  f"Calculated mastery score: {mastery_score} ({mastery_level})", data)
            else:
                self.log_result("Mastery Score Calculation", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Mastery Score Calculation", False, f"Exception: {str(e)}")
    
    def test_adaptive_difficulty(self):
        """Test POST /api/jeeves-hyperion/self-learning/adapt-difficulty"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/self-learning/adapt-difficulty"
            payload = {
                "recent_performance": [0.7, 0.8, 0.75, 0.85, 0.9],
                "current_difficulty": 0.5
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["previous_difficulty", "new_difficulty", "change", 
                                 "average_performance", "zone"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("Adaptive Difficulty", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    prev_diff = data.get("previous_difficulty", 0)
                    new_diff = data.get("new_difficulty", 0)
                    zone = data.get("zone", "unknown")
                    self.log_result("Adaptive Difficulty", True, 
                                  f"Difficulty adapted from {prev_diff} to {new_diff} (zone: {zone})", data)
            else:
                self.log_result("Adaptive Difficulty", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Adaptive Difficulty", False, f"Exception: {str(e)}")
    
    def test_retention_prediction(self):
        """Test POST /api/jeeves-hyperion/matrices/retention-prediction"""
        try:
            url = f"{self.base_url}/api/jeeves-hyperion/matrices/retention-prediction"
            params = {
                "topic": "algorithms",
                "review_count": 3,
                "days_since_learned": 5
            }
            
            response = requests.post(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                expected_fields = ["topic", "current_retention", "stability_days", 
                                 "review_count", "predictions", "optimal_review_date", 
                                 "review_urgency", "recommendation"]
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_result("Retention Prediction", False, 
                                  f"Missing fields: {missing_fields}", data)
                else:
                    retention = data.get("current_retention", 0)
                    urgency = data.get("review_urgency", "unknown")
                    self.log_result("Retention Prediction", True, 
                                  f"Retention prediction for {data.get('topic', 'unknown')}: {retention} (urgency: {urgency})", data)
            else:
                self.log_result("Retention Prediction", False, 
                              f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Retention Prediction", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all Jeeves Hyperion v13.0 API tests"""
        print("=" * 80)
        print("JEEVES HYPERION v13.0 API TESTING")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print()
        
        # Run all tests
        self.test_knowledge_base_stats()
        self.test_get_all_domains()
        self.test_get_domain_details()
        self.test_matrices_overview()
        self.test_mastery_score_calculation()
        self.test_adaptive_difficulty()
        self.test_retention_prediction()
        
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
            print("🎉 ALL TESTS PASSED! Jeeves Hyperion v13.0 API is fully functional.")
        else:
            print("❌ Some tests failed. Details above.")
            failed_tests = [r["test"] for r in self.results if not r["success"]]
            print(f"Failed tests: {', '.join(failed_tests)}")
        
        return passed, total

if __name__ == "__main__":
    tester = JeevesHyperionTester()
    passed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)