#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for CodeDock Multi-Language Compiler
Tests all endpoints thoroughly as requested in the review.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List

# Get backend URL from frontend .env
BACKEND_URL = "https://codedock-ultimate.preview.emergentagent.com/api"

class CodeDockAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.created_file_id = None
        self.created_addon_id = None
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test GET /api/health"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, "API is healthy")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected status: {data.get('status')}", data)
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
        return False
    
    def test_languages_endpoint(self):
        """Test GET /api/languages"""
        try:
            response = self.session.get(f"{self.base_url}/languages", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                languages = data.get("languages", [])
                
                # Check for required languages
                required_langs = ["python", "html", "javascript", "cpp", "css", "json", "markdown", "sql"]
                found_langs = [lang.get("key") for lang in languages]
                
                missing = [lang for lang in required_langs if lang not in found_langs]
                
                if not missing:
                    self.log_test("Languages Endpoint", True, f"Found all {len(languages)} languages")
                    return True
                else:
                    self.log_test("Languages Endpoint", False, f"Missing languages: {missing}", found_langs)
            else:
                self.log_test("Languages Endpoint", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Languages Endpoint", False, f"Request failed: {str(e)}")
        return False
    
    def test_code_execution(self):
        """Test POST /api/execute with different languages"""
        test_cases = [
            {
                "name": "Python Execution",
                "payload": {
                    "code": "print('Hello World')\nfor i in range(3): print(i)",
                    "language": "python"
                },
                "expected_output": "Hello World\n0\n1\n2"
            },
            {
                "name": "C++ Execution", 
                "payload": {
                    "code": "#include <iostream>\nint main() { std::cout << \"C++ works!\" << std::endl; return 0; }",
                    "language": "cpp"
                },
                "expected_output": "C++ works!"
            },
            {
                "name": "JavaScript Execution",
                "payload": {
                    "code": "console.log('JS test'); const x = 1 + 2; console.log(x);",
                    "language": "javascript"
                },
                "expected_contains": "JS test"
            },
            {
                "name": "HTML Execution",
                "payload": {
                    "code": "<html><body><h1>Test</h1></body></html>",
                    "language": "html"
                },
                "expected_contains": "<h1>Test</h1>"
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/execute",
                    json=test_case["payload"],
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("result", {})
                    status = result.get("status")
                    output = result.get("output", "")
                    error = result.get("error", "")
                    
                    if status == "success":
                        # Check expected output
                        if "expected_output" in test_case:
                            if test_case["expected_output"].strip() in output.strip():
                                self.log_test(test_case["name"], True, "Code executed successfully")
                            else:
                                self.log_test(test_case["name"], False, f"Output mismatch. Got: {output}", test_case)
                                all_passed = False
                        elif "expected_contains" in test_case:
                            if test_case["expected_contains"] in output:
                                self.log_test(test_case["name"], True, "Code executed successfully")
                            else:
                                self.log_test(test_case["name"], False, f"Output doesn't contain expected text. Got: {output}", test_case)
                                all_passed = False
                        else:
                            self.log_test(test_case["name"], True, "Code executed successfully")
                    else:
                        self.log_test(test_case["name"], False, f"Execution failed: {error}", result)
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test(test_case["name"], False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_code_validation(self):
        """Test POST /api/validate"""
        test_cases = [
            {
                "name": "Valid Python Code",
                "payload": {
                    "code": "print('Hello World')",
                    "language": "python"
                },
                "should_be_valid": True
            },
            {
                "name": "Invalid Python Code (Forbidden Import)",
                "payload": {
                    "code": "import os",
                    "language": "python"
                },
                "should_be_valid": False
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/validate",
                    json=test_case["payload"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    is_valid = data.get("valid")
                    
                    if is_valid == test_case["should_be_valid"]:
                        self.log_test(test_case["name"], True, f"Validation correct: {is_valid}")
                    else:
                        self.log_test(test_case["name"], False, f"Expected {test_case['should_be_valid']}, got {is_valid}", data)
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test(test_case["name"], False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_templates(self):
        """Test template endpoints"""
        all_passed = True
        
        # Test GET /api/templates
        try:
            response = self.session.get(f"{self.base_url}/templates", timeout=10)
            if response.status_code == 200:
                data = response.json()
                templates = data.get("templates", {})
                if "python" in templates and "html" in templates:
                    self.log_test("All Templates", True, f"Found templates for {len(templates)} languages")
                else:
                    self.log_test("All Templates", False, "Missing expected templates", templates)
                    all_passed = False
            else:
                self.log_test("All Templates", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("All Templates", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test GET /api/templates/python
        try:
            response = self.session.get(f"{self.base_url}/templates/python", timeout=10)
            if response.status_code == 200:
                data = response.json()
                templates = data.get("templates", [])
                template_names = [t.get("name") for t in templates]
                expected = ["hello_world", "function", "class", "loop"]
                
                if all(name in template_names for name in expected):
                    self.log_test("Python Templates", True, f"Found all expected templates: {template_names}")
                else:
                    self.log_test("Python Templates", False, f"Missing templates. Found: {template_names}", expected)
                    all_passed = False
            else:
                self.log_test("Python Templates", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Python Templates", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test GET /api/templates/html
        try:
            response = self.session.get(f"{self.base_url}/templates/html", timeout=10)
            if response.status_code == 200:
                data = response.json()
                templates = data.get("templates", [])
                if len(templates) > 0:
                    self.log_test("HTML Templates", True, f"Found {len(templates)} HTML templates")
                else:
                    self.log_test("HTML Templates", False, "No HTML templates found", data)
                    all_passed = False
            else:
                self.log_test("HTML Templates", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("HTML Templates", False, f"Request failed: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def test_file_management(self):
        """Test file CRUD operations"""
        all_passed = True
        
        # Test POST /api/files - Create file
        try:
            create_payload = {
                "name": "test.py",
                "language": "python",
                "code": "print('test')"
            }
            response = self.session.post(
                f"{self.base_url}/files",
                json=create_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.created_file_id = data.get("id")
                if self.created_file_id:
                    self.log_test("Create File", True, f"File created with ID: {self.created_file_id}")
                else:
                    self.log_test("Create File", False, "No file ID returned", data)
                    all_passed = False
            else:
                self.log_test("Create File", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Create File", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test GET /api/files - List files
        try:
            response = self.session.get(f"{self.base_url}/files", timeout=10)
            if response.status_code == 200:
                data = response.json()
                files = data.get("files", [])
                self.log_test("List Files", True, f"Found {len(files)} files")
            else:
                self.log_test("List Files", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("List Files", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test GET /api/files/{id} - Get specific file
        if self.created_file_id:
            try:
                response = self.session.get(f"{self.base_url}/files/{self.created_file_id}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("name") == "test.py":
                        self.log_test("Get File", True, "Retrieved file successfully")
                    else:
                        self.log_test("Get File", False, "File data mismatch", data)
                        all_passed = False
                else:
                    self.log_test("Get File", False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test("Get File", False, f"Request failed: {str(e)}")
                all_passed = False
        
        # Test PUT /api/files/{id} - Update file
        if self.created_file_id:
            try:
                update_payload = {
                    "name": "updated_test.py",
                    "code": "print('updated test')"
                }
                response = self.session.put(
                    f"{self.base_url}/files/{self.created_file_id}",
                    json=update_payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("name") == "updated_test.py":
                        self.log_test("Update File", True, "File updated successfully")
                    else:
                        self.log_test("Update File", False, "Update failed", data)
                        all_passed = False
                else:
                    self.log_test("Update File", False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test("Update File", False, f"Request failed: {str(e)}")
                all_passed = False
        
        # Test DELETE /api/files/{id} - Delete file
        if self.created_file_id:
            try:
                response = self.session.delete(f"{self.base_url}/files/{self.created_file_id}", timeout=10)
                if response.status_code == 200:
                    self.log_test("Delete File", True, "File deleted successfully")
                else:
                    self.log_test("Delete File", False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test("Delete File", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_addons_management(self):
        """Test addon CRUD operations"""
        all_passed = True
        
        # Test POST /api/addons - Create addon
        try:
            create_payload = {
                "language_key": "go",
                "name": "Go",
                "extension": ".go",
                "description": "Go language"
            }
            response = self.session.post(
                f"{self.base_url}/addons",
                json=create_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.created_addon_id = data.get("id")
                if self.created_addon_id:
                    self.log_test("Create Addon", True, f"Addon created with ID: {self.created_addon_id}")
                else:
                    self.log_test("Create Addon", False, "No addon ID returned", data)
                    all_passed = False
            else:
                self.log_test("Create Addon", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Create Addon", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test GET /api/addons - List addons
        try:
            response = self.session.get(f"{self.base_url}/addons", timeout=10)
            if response.status_code == 200:
                data = response.json()
                addons = data.get("addons", [])
                self.log_test("List Addons", True, f"Found {len(addons)} addons")
            else:
                self.log_test("List Addons", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("List Addons", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test DELETE /api/addons/{id} - Delete addon
        if self.created_addon_id:
            try:
                response = self.session.delete(f"{self.base_url}/addons/{self.created_addon_id}", timeout=10)
                if response.status_code == 200:
                    self.log_test("Delete Addon", True, "Addon deleted successfully")
                else:
                    self.log_test("Delete Addon", False, f"HTTP {response.status_code}", response.text)
                    all_passed = False
            except Exception as e:
                self.log_test("Delete Addon", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_user_preferences(self):
        """Test user preferences endpoints"""
        all_passed = True
        
        # Test GET /api/preferences
        try:
            response = self.session.get(f"{self.base_url}/preferences", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "theme" in data and "font_size" in data:
                    self.log_test("Get Preferences", True, "Retrieved preferences successfully")
                else:
                    self.log_test("Get Preferences", False, "Missing expected preference fields", data)
                    all_passed = False
            else:
                self.log_test("Get Preferences", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Get Preferences", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test PUT /api/preferences
        try:
            update_payload = {
                "theme": "light",
                "font_size": 16
            }
            response = self.session.put(
                f"{self.base_url}/preferences",
                json=update_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("theme") == "light" and data.get("font_size") == 16:
                    self.log_test("Update Preferences", True, "Preferences updated successfully")
                else:
                    self.log_test("Update Preferences", False, "Update failed", data)
                    all_passed = False
            else:
                self.log_test("Update Preferences", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Update Preferences", False, f"Request failed: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def test_execution_history(self):
        """Test execution history endpoints"""
        all_passed = True
        
        # Test GET /api/history
        try:
            response = self.session.get(f"{self.base_url}/history", timeout=10)
            if response.status_code == 200:
                data = response.json()
                history = data.get("history", [])
                self.log_test("Get History", True, f"Retrieved {len(history)} history entries")
            else:
                self.log_test("Get History", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Get History", False, f"Request failed: {str(e)}")
            all_passed = False
        
        # Test DELETE /api/history
        try:
            response = self.session.delete(f"{self.base_url}/history", timeout=10)
            if response.status_code == 200:
                self.log_test("Clear History", True, "History cleared successfully")
            else:
                self.log_test("Clear History", False, f"HTTP {response.status_code}", response.text)
                all_passed = False
        except Exception as e:
            self.log_test("Clear History", False, f"Request failed: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print(f"🚀 Starting CodeDock API Tests against {self.base_url}")
        print("=" * 60)
        
        test_functions = [
            ("Health Check", self.test_health_check),
            ("Languages Endpoint", self.test_languages_endpoint),
            ("Code Execution", self.test_code_execution),
            ("Code Validation", self.test_code_validation),
            ("Templates", self.test_templates),
            ("File Management", self.test_file_management),
            ("Addons Management", self.test_addons_management),
            ("User Preferences", self.test_user_preferences),
            ("Execution History", self.test_execution_history)
        ]
        
        passed_categories = 0
        total_categories = len(test_functions)
        
        for category_name, test_func in test_functions:
            print(f"\n📋 Testing {category_name}...")
            if test_func():
                passed_categories += 1
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Categories: {passed_categories}/{total_categories} passed")
        print(f"Individual Tests: {passed_tests}/{total_tests} passed")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS ({failed_tests}):")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = CodeDockAPITester(BACKEND_URL)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()