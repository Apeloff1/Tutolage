#!/usr/bin/env python3
"""
Backend API Testing Suite for CodeDock CS Bible Curriculum
Tests the new 15-Year CS Bible curriculum API endpoints
"""

import requests
import json
import sys
from typing import Dict, Any, List
import time

# Backend URL from environment
BACKEND_URL = "https://codedock-ultimate.preview.emergentagent.com"

class CSBibleAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_health_check(self):
        """Test basic health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, f"Status: {data.get('status')}")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected status: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
            
    def test_languages_endpoint(self):
        """Test languages endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/languages")
            if response.status_code == 200:
                data = response.json()
                # Handle both list format and object format with 'languages' key
                if isinstance(data, list) and len(data) > 0:
                    self.log_test("Languages Endpoint", True, f"Found {len(data)} languages")
                    return True
                elif isinstance(data, dict) and "languages" in data and len(data["languages"]) > 0:
                    self.log_test("Languages Endpoint", True, f"Found {len(data['languages'])} languages")
                    return True
                else:
                    self.log_test("Languages Endpoint", False, f"Invalid response format")
                    return False
            else:
                self.log_test("Languages Endpoint", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Languages Endpoint", False, f"Exception: {str(e)}")
            return False
            
    def test_code_execution(self):
        """Test basic code execution"""
        try:
            payload = {
                "code": 'print("Hello from CS Bible test!")',
                "language": "python"
            }
            response = self.session.post(f"{self.base_url}/api/execute", json=payload)
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "output" in data["result"]:
                    self.log_test("Code Execution", True, f"Output: {data['result']['output'][:50]}...")
                    return True
                else:
                    self.log_test("Code Execution", False, f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Code Execution", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Code Execution", False, f"Exception: {str(e)}")
            return False

    def test_bible_overview(self):
        """Test GET /api/bible - Full curriculum overview"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible")
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["title", "subtitle", "total_years", "total_courses", "total_hours"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Bible Overview", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Validate specific values
                if data.get("total_years") != 15:
                    self.log_test("Bible Overview", False, f"Expected 15 years, got {data.get('total_years')}")
                    return False
                    
                if data.get("total_courses") != 180:
                    self.log_test("Bible Overview", False, f"Expected 180 courses, got {data.get('total_courses')}")
                    return False
                    
                if data.get("total_hours") != 12000:
                    self.log_test("Bible Overview", False, f"Expected 12000 hours, got {data.get('total_hours')}")
                    return False
                
                # Check certification levels
                if "certification_levels" not in data or len(data["certification_levels"]) != 5:
                    self.log_test("Bible Overview", False, f"Expected 5 certification levels")
                    return False
                
                # Check tracks
                if "tracks" not in data:
                    self.log_test("Bible Overview", False, "Missing tracks information")
                    return False
                
                # Check years summary
                if "years_summary" not in data:
                    self.log_test("Bible Overview", False, "Missing years_summary")
                    return False
                
                self.log_test("Bible Overview", True, 
                    f"Title: {data['title']}, Years: {data['total_years']}, Courses: {data['total_courses']}")
                return True
                
            else:
                self.log_test("Bible Overview", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Bible Overview", False, f"Exception: {str(e)}")
            return False

    def test_year_1_details(self):
        """Test GET /api/bible/year/1 - Year 1 details"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/year/1")
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                if data.get("year") != 1:
                    self.log_test("Year 1 Details", False, f"Expected year 1, got {data.get('year')}")
                    return False
                
                if data.get("name") != "Foundation Year":
                    self.log_test("Year 1 Details", False, f"Expected 'Foundation Year', got {data.get('name')}")
                    return False
                
                # Check tracks
                if "tracks" not in data:
                    self.log_test("Year 1 Details", False, "Missing tracks")
                    return False
                
                # Check for core track courses
                tracks = data["tracks"]
                if "core" not in tracks:
                    self.log_test("Year 1 Details", False, "Missing core track")
                    return False
                
                core_courses = tracks["core"]
                if not isinstance(core_courses, list) or len(core_courses) == 0:
                    self.log_test("Year 1 Details", False, "No core courses found")
                    return False
                
                # Check for CS 101 course
                cs101_found = False
                for course in core_courses:
                    if course.get("code") == "CS 101":
                        cs101_found = True
                        # Check course structure
                        required_course_fields = ["id", "title", "learning_objectives", "topics", "projects"]
                        missing_course_fields = [field for field in required_course_fields if field not in course]
                        if missing_course_fields:
                            self.log_test("Year 1 Details", False, f"CS 101 missing fields: {missing_course_fields}")
                            return False
                        break
                
                if not cs101_found:
                    self.log_test("Year 1 Details", False, "CS 101 course not found")
                    return False
                
                self.log_test("Year 1 Details", True, 
                    f"Year: {data['year']}, Name: {data['name']}, Tracks: {len(tracks)}")
                return True
                
            else:
                self.log_test("Year 1 Details", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Year 1 Details", False, f"Exception: {str(e)}")
            return False

    def test_year_8_details(self):
        """Test GET /api/bible/year/8 - Year 8 AI details"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/year/8")
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                if data.get("year") != 8:
                    self.log_test("Year 8 Details", False, f"Expected year 8, got {data.get('year')}")
                    return False
                
                # Should be AI Foundations Year
                year_name = data.get("name", "")
                if "AI" not in year_name:
                    self.log_test("Year 8 Details", False, f"Expected AI year, got: {year_name}")
                    return False
                
                # Check for key courses with Machine Learning and Deep Learning
                if "key_courses" in data:
                    key_courses = data["key_courses"]
                    ai_courses_found = False
                    ml_found = False
                    dl_found = False
                    
                    for course in key_courses:
                        course_title = course.get("title", "")
                        if "Machine Learning" in course_title:
                            ml_found = True
                        if "Deep Learning" in course_title:
                            dl_found = True
                    
                    ai_courses_found = ml_found and dl_found
                    
                    if not ai_courses_found:
                        self.log_test("Year 8 Details", False, f"Missing ML/DL courses. ML found: {ml_found}, DL found: {dl_found}")
                        return False
                
                self.log_test("Year 8 Details", True, 
                    f"Year: {data['year']}, Name: {data['name']}")
                return True
                
            else:
                self.log_test("Year 8 Details", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Year 8 Details", False, f"Exception: {str(e)}")
            return False

    def test_specific_course(self):
        """Test GET /api/bible/course/y1_cs101 - Specific course"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/course/y1_cs101")
            if response.status_code == 200:
                data = response.json()
                
                # Check course structure
                if data.get("id") != "y1_cs101":
                    self.log_test("Specific Course", False, f"Expected y1_cs101, got {data.get('id')}")
                    return False
                
                if data.get("title") != "Introduction to Programming":
                    self.log_test("Specific Course", False, f"Expected 'Introduction to Programming', got {data.get('title')}")
                    return False
                
                # Check required fields
                required_fields = ["weeks", "topics", "content", "projects"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Specific Course", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check topics structure
                topics = data.get("topics", [])
                if not isinstance(topics, list) or len(topics) == 0:
                    self.log_test("Specific Course", False, "No topics found")
                    return False
                
                # Check projects structure
                projects = data.get("projects", [])
                if not isinstance(projects, list) or len(projects) == 0:
                    self.log_test("Specific Course", False, "No projects found")
                    return False
                
                self.log_test("Specific Course", True, 
                    f"Course: {data['title']}, Topics: {len(topics)}, Projects: {len(projects)}")
                return True
                
            else:
                self.log_test("Specific Course", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Specific Course", False, f"Exception: {str(e)}")
            return False

    def test_courses_by_year(self):
        """Test GET /api/bible/courses?year=1 - Filter courses by year"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/courses?year=1")
            if response.status_code == 200:
                data = response.json()
                
                # Handle the actual response format with 'courses' key
                if isinstance(data, dict) and "courses" in data:
                    courses = data["courses"]
                    if not isinstance(courses, list):
                        self.log_test("Courses by Year", False, f"Expected courses list, got {type(courses)}")
                        return False
                    
                    if len(courses) == 0:
                        self.log_test("Courses by Year", False, "No courses returned for year 1")
                        return False
                    
                    # Check that all courses are from year 1
                    for course in courses:
                        if course.get("year") != 1:
                            self.log_test("Courses by Year", False, f"Non-year-1 course found: year {course.get('year')}")
                            return False
                    
                    self.log_test("Courses by Year", True, f"Found {len(courses)} courses for year 1")
                    return True
                else:
                    self.log_test("Courses by Year", False, f"Expected dict with 'courses' key, got {type(data)}")
                    return False
                
            else:
                self.log_test("Courses by Year", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Courses by Year", False, f"Exception: {str(e)}")
            return False

    def test_learning_tracks(self):
        """Test GET /api/bible/tracks - Get all learning tracks"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/tracks")
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Learning Tracks", False, f"Expected list, got {type(data)}")
                    return False
                
                if len(data) != 8:
                    self.log_test("Learning Tracks", False, f"Expected 8 tracks, got {len(data)}")
                    return False
                
                # Check for expected track names
                expected_tracks = ["Systems", "Theory", "AI/ML", "Security", "Web/Mobile", "Data", "Graphics", "Compilers"]
                track_names = [track.get("name", "") for track in data]
                
                missing_tracks = []
                for expected in expected_tracks:
                    if not any(expected.lower() in name.lower() for name in track_names):
                        missing_tracks.append(expected)
                
                if missing_tracks:
                    self.log_test("Learning Tracks", False, f"Missing tracks: {missing_tracks}")
                    return False
                
                self.log_test("Learning Tracks", True, f"Found all 8 tracks: {[t.get('name') for t in data]}")
                return True
                
            else:
                self.log_test("Learning Tracks", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Learning Tracks", False, f"Exception: {str(e)}")
            return False

    def test_certifications(self):
        """Test GET /api/bible/certifications - Get certification path"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/certifications")
            if response.status_code == 200:
                data = response.json()
                
                # Handle the actual response format with 'levels' key
                if isinstance(data, dict) and "levels" in data:
                    levels = data["levels"]
                    if not isinstance(levels, list):
                        self.log_test("Certifications", False, f"Expected levels list, got {type(levels)}")
                        return False
                    
                    if len(levels) != 5:
                        self.log_test("Certifications", False, f"Expected 5 certification levels, got {len(levels)}")
                        return False
                    
                    # Check for expected certification levels
                    expected_levels = ["Certificate", "Associate", "Bachelor", "Master", "PhD"]
                    cert_names = [cert.get("name", "") for cert in levels]
                    
                    for expected in expected_levels:
                        if expected not in cert_names:
                            self.log_test("Certifications", False, f"Missing certification: {expected}")
                            return False
                    
                    self.log_test("Certifications", True, f"Found all 5 certifications: {cert_names}")
                    return True
                else:
                    self.log_test("Certifications", False, f"Expected dict with 'levels' key, got {type(data)}")
                    return False
                
            else:
                self.log_test("Certifications", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Certifications", False, f"Exception: {str(e)}")
            return False

    def test_search_courses(self):
        """Test GET /api/bible/search?q=algorithm - Search courses"""
        try:
            response = self.session.get(f"{self.base_url}/api/bible/search?q=algorithm")
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Search Courses", False, f"Expected list, got {type(data)}")
                    return False
                
                # Should find courses related to algorithms
                if len(data) == 0:
                    self.log_test("Search Courses", False, "No courses found for 'algorithm' search")
                    return False
                
                # Check that results contain algorithm-related content
                algorithm_found = False
                for course in data:
                    course_text = json.dumps(course).lower()
                    if "algorithm" in course_text:
                        algorithm_found = True
                        break
                
                if not algorithm_found:
                    self.log_test("Search Courses", False, "Search results don't contain algorithm-related content")
                    return False
                
                self.log_test("Search Courses", True, f"Found {len(data)} courses for 'algorithm' search")
                return True
                
            else:
                self.log_test("Search Courses", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Search Courses", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all CS Bible API tests"""
        print("🧪 Starting CS Bible API Testing Suite")
        print("=" * 50)
        
        # Test existing functionality first
        print("\n📋 Testing Existing Functionality:")
        self.test_health_check()
        self.test_languages_endpoint()
        self.test_code_execution()
        
        # Test new CS Bible endpoints
        print("\n📚 Testing CS Bible Curriculum Endpoints:")
        self.test_bible_overview()
        self.test_year_1_details()
        self.test_year_8_details()
        self.test_specific_course()
        self.test_courses_by_year()
        self.test_learning_tracks()
        self.test_certifications()
        self.test_search_courses()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['test']}: {result['details']}")
        
        return passed_tests, failed_tests

def main():
    """Main test runner"""
    print("🚀 CodeDock CS Bible API Test Suite")
    print(f"🌐 Testing backend at: {BACKEND_URL}")
    
    tester = CSBibleAPITester(BACKEND_URL)
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed > 0:
        print(f"\n⚠️  {failed} test(s) failed!")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()