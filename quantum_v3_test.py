#!/usr/bin/env python3
"""
CodeDock Quantum v3.0 Enhanced Features Test Suite
Tests all 2026+ features as specified in the review request
"""

import requests
import json
import sys
import time
from typing import Dict, Any, List

# Use the correct backend URL from environment
BACKEND_URL = "https://sota-2026.preview.emergentagent.com/api"

class QuantumV3Tester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
        self.failed_tests = []
        
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result with details"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if response_data and not success:
            print(f"    Response: {str(response_data)[:200]}...")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
        if not success:
            self.failed_tests.append(test_name)
    
    def test_root_and_health(self):
        """Test 1: Root & Health endpoints with version 3.0.0 Quantum"""
        print("🔍 Testing Root & Health Endpoints")
        print("-" * 50)
        
        # Test root endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                version = data.get("version", "")
                name = data.get("name", "")
                
                # Check for version 3.0.0 Quantum edition
                if "3.0" in version and ("Quantum" in name or "Quantum" in version):
                    self.log_result("Root Endpoint - Version 3.0.0 Quantum", True, f"Version: {version}, Name: {name}")
                else:
                    self.log_result("Root Endpoint - Version 3.0.0 Quantum", False, f"Expected 3.0.0 Quantum, got Version: {version}, Name: {name}")
            else:
                self.log_result("Root Endpoint - Version 3.0.0 Quantum", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Root Endpoint - Version 3.0.0 Quantum", False, f"Exception: {str(e)}")
        
        # Test health endpoint with AI availability
        try:
            response = self.session.get(f"{BACKEND_URL}/health")
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                ai_available = data.get("ai_available")
                
                if status == "healthy":
                    self.log_result("Health Endpoint - Status", True, f"Status: {status}")
                else:
                    self.log_result("Health Endpoint - Status", False, f"Expected healthy, got: {status}")
                
                if ai_available is not None:
                    self.log_result("Health Endpoint - AI Availability", True, f"AI Available: {ai_available}")
                else:
                    self.log_result("Health Endpoint - AI Availability", False, "AI availability status not found")
            else:
                self.log_result("Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Health Endpoint", False, f"Exception: {str(e)}")
    
    def test_stats_endpoint(self):
        """Test 2: Stats endpoint with executor stats and AI request count"""
        print("📊 Testing Stats Endpoint")
        print("-" * 50)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/stats")
            if response.status_code == 200:
                data = response.json()
                
                # Check for executor stats
                executor_stats = data.get("executor_stats")
                if executor_stats:
                    self.log_result("Stats - Executor Stats", True, f"Executor stats present")
                else:
                    self.log_result("Stats - Executor Stats", False, "Executor stats not found")
                
                # Check for AI request count
                ai_request_count = data.get("ai_request_count")
                if ai_request_count is not None:
                    self.log_result("Stats - AI Request Count", True, f"AI Request Count: {ai_request_count}")
                else:
                    self.log_result("Stats - AI Request Count", False, "AI request count not found")
            else:
                self.log_result("Stats Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Stats Endpoint", False, f"Exception: {str(e)}")
    
    def test_languages_endpoint(self):
        """Test 3: Languages endpoint with all required languages and templates_available"""
        print("🌐 Testing Languages Endpoint")
        print("-" * 50)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/languages")
            if response.status_code == 200:
                data = response.json()
                languages = data.get("languages", [])
                
                # Required languages from review request
                required_languages = ["python", "javascript", "typescript", "cpp", "c", "html", "css"]
                found_languages = [lang.get("key", "").lower() for lang in languages]
                
                missing_languages = [lang for lang in required_languages if lang not in found_languages]
                
                if not missing_languages:
                    self.log_result("Languages - Required Languages", True, f"All required languages found: {required_languages}")
                else:
                    self.log_result("Languages - Required Languages", False, f"Missing languages: {missing_languages}")
                
                # Check for templates_available boolean
                has_templates_available = any("templates_available" in lang for lang in languages)
                if has_templates_available:
                    self.log_result("Languages - Templates Available Flag", True, "templates_available boolean found")
                else:
                    self.log_result("Languages - Templates Available Flag", False, "templates_available boolean not found")
            else:
                self.log_result("Languages Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Languages Endpoint", False, f"Exception: {str(e)}")
    
    def test_code_execution_with_analysis(self):
        """Test 4: Code execution with include_analysis=true"""
        print("⚡ Testing Code Execution with Analysis")
        print("-" * 50)
        
        payload = {
            "code": "class Test:\n    def run(self):\n        if True:\n            print('test')\n\nt = Test()\nt.run()",
            "language": "python",
            "include_analysis": True
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/execute", json=payload)
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                
                # Check for metrics
                metrics = result.get("metrics")
                if metrics:
                    self.log_result("Code Execution - Metrics", True, "Execution metrics present")
                else:
                    self.log_result("Code Execution - Metrics", False, "Execution metrics not found")
                
                # Check for analysis
                analysis = result.get("analysis")
                if analysis:
                    self.log_result("Code Execution - Analysis", True, "Code analysis present")
                    
                    # Check specific analysis fields
                    complexity = analysis.get("complexity")
                    cyclomatic_complexity = analysis.get("cyclomatic_complexity")
                    functions_count = analysis.get("functions_count")
                    
                    if all([complexity, cyclomatic_complexity is not None, functions_count is not None]):
                        self.log_result("Code Execution - Analysis Fields", True, f"Complexity: {complexity}, Cyclomatic: {cyclomatic_complexity}, Functions: {functions_count}")
                    else:
                        self.log_result("Code Execution - Analysis Fields", False, "Missing analysis fields")
                else:
                    self.log_result("Code Execution - Analysis", False, "Code analysis not found")
            else:
                self.log_result("Code Execution with Analysis", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Code Execution with Analysis", False, f"Exception: {str(e)}")
    
    def test_code_analysis_endpoint(self):
        """Test 5: Code analysis endpoint"""
        print("🔍 Testing Code Analysis Endpoint")
        print("-" * 50)
        
        payload = {
            "code": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)",
            "language": "python"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/analyze", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Check for required analysis fields
                required_fields = ["complexity", "cyclomatic_complexity", "functions_count"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_result("Code Analysis - Required Fields", True, f"All required fields present: {required_fields}")
                    
                    # Log specific values
                    complexity = data.get("complexity")
                    cyclomatic = data.get("cyclomatic_complexity")
                    functions = data.get("functions_count")
                    self.log_result("Code Analysis - Values", True, f"Complexity: {complexity}, Cyclomatic: {cyclomatic}, Functions: {functions}")
                else:
                    self.log_result("Code Analysis - Required Fields", False, f"Missing fields: {missing_fields}")
            else:
                self.log_result("Code Analysis Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Code Analysis Endpoint", False, f"Exception: {str(e)}")
    
    def test_code_validation_strict(self):
        """Test 6: Code validation with STRICT security level"""
        print("🔒 Testing Code Validation (STRICT)")
        print("-" * 50)
        
        payload = {
            "code": "import os",
            "language": "python",
            "security_level": "strict"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Should block the import and return security report
                is_valid = data.get("valid", True)
                if not is_valid:
                    self.log_result("Code Validation - Blocking", True, "Forbidden import 'os' correctly blocked")
                else:
                    self.log_result("Code Validation - Blocking", False, "Forbidden import 'os' was not blocked")
                
                # Check for security report
                security_report = data.get("security_report") or data.get("security")
                if security_report:
                    self.log_result("Code Validation - Security Report", True, "Security report present")
                else:
                    self.log_result("Code Validation - Security Report", False, "Security report not found")
            else:
                self.log_result("Code Validation (STRICT)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Code Validation (STRICT)", False, f"Exception: {str(e)}")
    
    def test_ai_assistant(self):
        """Test 7: AI Assistant endpoints"""
        print("🤖 Testing AI Assistant")
        print("-" * 50)
        
        # Test AI modes endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/ai/modes")
            if response.status_code == 200:
                data = response.json()
                
                # Should return 9 modes
                modes = data if isinstance(data, list) else data.get("modes", [])
                modes_count = len(modes)
                
                if modes_count == 9:
                    self.log_result("AI Assistant - Modes Count", True, f"Found {modes_count} modes (expected 9)")
                else:
                    self.log_result("AI Assistant - Modes Count", False, f"Found {modes_count} modes, expected 9")
            else:
                self.log_result("AI Assistant - Modes Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("AI Assistant - Modes Endpoint", False, f"Exception: {str(e)}")
        
        # Test AI assist endpoint with "explain" mode
        payload = {
            "code": "print('hello world')",
            "language": "python",
            "mode": "explain"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/ai/assist", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Check for AI response
                has_response = any(key in data for key in ["suggestion", "response", "explanation", "result"])
                if has_response:
                    self.log_result("AI Assistant - Response", True, "AI response generated successfully")
                else:
                    self.log_result("AI Assistant - Response", False, "No AI response found")
            else:
                self.log_result("AI Assistant - Assist Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("AI Assistant - Assist Endpoint", False, f"Exception: {str(e)}")
    
    def test_templates_enhanced(self):
        """Test 8: Templates with enhanced complexity levels"""
        print("📋 Testing Enhanced Templates")
        print("-" * 50)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/templates/python")
            if response.status_code == 200:
                data = response.json()
                templates = data.get("templates", [])
                
                if templates:
                    self.log_result("Templates - Python Templates", True, f"Found {len(templates)} Python templates")
                    
                    # Check for complexity levels in templates
                    has_complexity = any("complexity" in str(template) for template in templates)
                    if has_complexity:
                        self.log_result("Templates - Complexity Levels", True, "Templates include complexity levels")
                    else:
                        self.log_result("Templates - Complexity Levels", False, "Templates missing complexity levels")
                else:
                    self.log_result("Templates - Python Templates", False, "No Python templates found")
            else:
                self.log_result("Enhanced Templates", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Enhanced Templates", False, f"Exception: {str(e)}")
    
    def test_snippets_crud(self):
        """Test 9: Snippets CRUD operations"""
        print("📝 Testing Snippets CRUD")
        print("-" * 50)
        
        # Create snippet
        create_payload = {
            "code": "print('test')",
            "language": "python",
            "title": "Test Snippet"
        }
        
        snippet_id = None
        try:
            response = self.session.post(f"{BACKEND_URL}/snippets", json=create_payload)
            if response.status_code in [200, 201]:
                data = response.json()
                snippet_id = data.get("id") or data.get("snippet_id")
                
                # Check for share_url
                has_share_url = "share_url" in data or "url" in data
                if has_share_url:
                    self.log_result("Snippets - Create with Share URL", True, "Snippet created with share URL")
                else:
                    self.log_result("Snippets - Create with Share URL", False, "Snippet created but no share URL")
            else:
                self.log_result("Snippets - Create", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Snippets - Create", False, f"Exception: {str(e)}")
        
        # Get snippet by ID
        if snippet_id:
            try:
                response = self.session.get(f"{BACKEND_URL}/snippets/{snippet_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("title") == "Test Snippet":
                        self.log_result("Snippets - Get by ID", True, "Snippet retrieved successfully")
                    else:
                        self.log_result("Snippets - Get by ID", False, "Snippet data mismatch")
                else:
                    self.log_result("Snippets - Get by ID", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result("Snippets - Get by ID", False, f"Exception: {str(e)}")
    
    def test_all_crud_operations(self):
        """Test 10: All CRUD operations for files, addons, preferences, history"""
        print("🔧 Testing All CRUD Operations")
        print("-" * 50)
        
        # Files CRUD (basic test)
        try:
            response = self.session.get(f"{BACKEND_URL}/files")
            if response.status_code == 200:
                self.log_result("CRUD - Files List", True, "Files endpoint accessible")
            else:
                self.log_result("CRUD - Files List", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("CRUD - Files List", False, f"Exception: {str(e)}")
        
        # Addons CRUD (basic test)
        try:
            response = self.session.get(f"{BACKEND_URL}/addons")
            if response.status_code == 200:
                self.log_result("CRUD - Addons List", True, "Addons endpoint accessible")
            else:
                self.log_result("CRUD - Addons List", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("CRUD - Addons List", False, f"Exception: {str(e)}")
        
        # Preferences CRUD (basic test)
        try:
            response = self.session.get(f"{BACKEND_URL}/preferences")
            if response.status_code == 200:
                self.log_result("CRUD - Preferences Get", True, "Preferences endpoint accessible")
            else:
                self.log_result("CRUD - Preferences Get", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("CRUD - Preferences Get", False, f"Exception: {str(e)}")
        
        # History CRUD (basic test)
        try:
            response = self.session.get(f"{BACKEND_URL}/history")
            if response.status_code == 200:
                self.log_result("CRUD - History Get", True, "History endpoint accessible")
            else:
                self.log_result("CRUD - History Get", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("CRUD - History Get", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all CodeDock Quantum v3.0 tests"""
        print("🚀 CodeDock Quantum v3.0 Enhanced API Testing")
        print("=" * 80)
        print(f"Testing API at: {BACKEND_URL}")
        print("=" * 80)
        
        # Run all test categories
        self.test_root_and_health()
        self.test_stats_endpoint()
        self.test_languages_endpoint()
        self.test_code_execution_with_analysis()
        self.test_code_analysis_endpoint()
        self.test_code_validation_strict()
        self.test_ai_assistant()
        self.test_templates_enhanced()
        self.test_snippets_crud()
        self.test_all_crud_operations()
        
        # Summary
        print("=" * 80)
        print("🎯 QUANTUM v3.0 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        print(f"\n🕒 Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = QuantumV3Tester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All Quantum v3.0 tests passed!")
        return True
    else:
        print("\n💥 Some Quantum v3.0 tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)