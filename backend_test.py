#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CODEDOCK v11.2 API TESTING SUITE                                           ║
║  Testing NEW v11.2 APIs: Masterclass, Asset Pipeline, Game Genres,         ║
║  AI Log Vault, and Enhanced Jeeves                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from frontend/.env
BACKEND_URL = "https://march-2026-preview.preview.emergentagent.com"

class CodeDockTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if response_data and isinstance(response_data, dict):
            # Add key metrics from response
            if "total_hours" in response_data:
                result["total_hours"] = response_data["total_hours"]
            if "total_tracks" in response_data:
                result["total_tracks"] = response_data["total_tracks"]
            if "total_genres" in response_data:
                result["total_genres"] = response_data["total_genres"]
            if "total_subgenres" in response_data:
                result["total_subgenres"] = response_data["total_subgenres"]
                
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_api_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_keys: List[str] = None) -> Dict:
        """Generic API endpoint tester"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
                
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    
                    # Check for expected keys if provided
                    if expected_keys:
                        missing_keys = [key for key in expected_keys if key not in json_data]
                        if missing_keys:
                            return {
                                "success": False, 
                                "error": f"Missing expected keys: {missing_keys}",
                                "data": json_data
                            }
                    
                    return {"success": True, "data": json_data}
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response", "raw": response.text[:500]}
            else:
                return {
                    "success": False, 
                    "error": f"HTTP {response.status_code}: {response.text[:500]}"
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}

    def test_masterclass_apis(self):
        """Test all Masterclass APIs"""
        print("🎓 TESTING MASTERCLASS APIs")
        print("=" * 50)
        
        # 1. GET /api/masterclass/info
        result = self.test_api_endpoint("GET", "/api/masterclass/info", 
                                      expected_keys=["name", "total_hours", "total_tracks"])
        self.log_result("Masterclass Info", result["success"], 
                       f"Expected 2860+ hours, 12 tracks" if result["success"] else result["error"],
                       result.get("data"))
        
        # 2. GET /api/masterclass/tracks
        result = self.test_api_endpoint("GET", "/api/masterclass/tracks",
                                      expected_keys=["total_hours", "tracks"])
        if result["success"]:
            tracks_count = len(result["data"].get("tracks", []))
            total_hours = result["data"].get("total_hours", 0)
            self.log_result("Masterclass Tracks", True, 
                           f"Found {tracks_count} tracks, {total_hours} total hours")
        else:
            self.log_result("Masterclass Tracks", False, result["error"])
        
        # 3. GET /api/masterclass/track/python_mastery
        result = self.test_api_endpoint("GET", "/api/masterclass/track/python_mastery",
                                      expected_keys=["name", "total_hours", "modules"])
        if result["success"]:
            track_name = result["data"].get("name", "")
            track_hours = result["data"].get("total_hours", 0)
            modules_count = len(result["data"].get("modules", []))
            self.log_result("Python Mastery Track", True,
                           f"Track: {track_name}, {track_hours} hours, {modules_count} modules")
        else:
            self.log_result("Python Mastery Track", False, result["error"])
        
        # 4. GET /api/masterclass/certifications
        result = self.test_api_endpoint("GET", "/api/masterclass/certifications",
                                      expected_keys=["certifications"])
        if result["success"]:
            certs_count = len(result["data"].get("certifications", []))
            self.log_result("Masterclass Certifications", True,
                           f"Found {certs_count} certifications available")
        else:
            self.log_result("Masterclass Certifications", False, result["error"])
        
        # 5. POST /api/masterclass/personalized-path
        path_request = {
            "goals": ["web_development"],
            "current_level": "beginner",
            "weekly_hours": 10
        }
        result = self.test_api_endpoint("POST", "/api/masterclass/personalized-path", 
                                      data=path_request,
                                      expected_keys=["personalized_path"])
        if result["success"]:
            path = result["data"].get("personalized_path", {})
            tracks_count = len(path.get("tracks", []))
            total_hours = path.get("total_hours", 0)
            weeks = path.get("estimated_weeks", 0)
            self.log_result("Personalized Learning Path", True,
                           f"Generated path: {tracks_count} tracks, {total_hours} hours, {weeks} weeks")
        else:
            self.log_result("Personalized Learning Path", False, result["error"])

    def test_asset_pipeline_apis(self):
        """Test all Asset Pipeline APIs"""
        print("🎨 TESTING ASSET PIPELINE APIs")
        print("=" * 50)
        
        # 1. GET /api/assets/info
        result = self.test_api_endpoint("GET", "/api/assets/info",
                                      expected_keys=["name", "capabilities"])
        self.log_result("Asset Pipeline Info", result["success"],
                       "System info with 2D/3D capabilities" if result["success"] else result["error"],
                       result.get("data"))
        
        # 2. GET /api/assets/categories/2d
        result = self.test_api_endpoint("GET", "/api/assets/categories/2d")
        if result["success"]:
            categories = list(result["data"].keys()) if isinstance(result["data"], dict) else []
            self.log_result("2D Asset Categories", True,
                           f"Found categories: {', '.join(categories[:5])}")
        else:
            self.log_result("2D Asset Categories", False, result["error"])
        
        # 3. GET /api/assets/categories/3d
        result = self.test_api_endpoint("GET", "/api/assets/categories/3d")
        if result["success"]:
            categories = list(result["data"].keys()) if isinstance(result["data"], dict) else []
            self.log_result("3D Asset Categories", True,
                           f"Found categories: {', '.join(categories[:5])}")
        else:
            self.log_result("3D Asset Categories", False, result["error"])
        
        # 4. POST /api/assets/generate/sprite
        sprite_request = {
            "description": "dragon character",
            "category": "characters",
            "asset_type": "enemy",
            "style": "pixel_art",
            "resolution": "32x32"
        }
        result = self.test_api_endpoint("POST", "/api/assets/generate/sprite",
                                      data=sprite_request,
                                      expected_keys=["asset", "generation"])
        if result["success"]:
            asset_id = result["data"].get("asset", {}).get("id", "")
            generation = result["data"].get("generation", {})
            self.log_result("Generate 2D Sprite", True,
                           f"Generated sprite asset {asset_id}, includes DALL-E and Stable Diffusion prompts")
        else:
            self.log_result("Generate 2D Sprite", False, result["error"])
        
        # 5. POST /api/assets/generate/model
        model_request = {
            "description": "medieval knight",
            "category": "characters",
            "asset_type": "humanoid",
            "style": "stylized",
            "poly_count": "mid_poly"
        }
        result = self.test_api_endpoint("POST", "/api/assets/generate/model",
                                      data=model_request,
                                      expected_keys=["asset", "generation"])
        if result["success"]:
            asset_id = result["data"].get("asset", {}).get("id", "")
            poly_count = result["data"].get("technical", {}).get("poly_count", "")
            self.log_result("Generate 3D Model", True,
                           f"Generated 3D model {asset_id}, poly count: {poly_count}")
        else:
            self.log_result("Generate 3D Model", False, result["error"])
        
        # 6. POST /api/assets/generate/tileset
        tileset_request = {
            "theme": "forest",
            "style": "pixel_art",
            "tile_size": 32
        }
        result = self.test_api_endpoint("POST", "/api/assets/generate/tileset",
                                      data=tileset_request,
                                      expected_keys=["tileset", "tiles"])
        if result["success"]:
            tileset_id = result["data"].get("tileset", {}).get("id", "")
            total_tiles = result["data"].get("tileset", {}).get("total_tiles", 0)
            self.log_result("Generate Tileset", True,
                           f"Generated tileset {tileset_id} with {total_tiles} tiles")
        else:
            self.log_result("Generate Tileset", False, result["error"])

    def test_game_genres_apis(self):
        """Test all Game Genres APIs"""
        print("🎮 TESTING GAME GENRES APIs")
        print("=" * 50)
        
        # 1. GET /api/game-genres/info
        result = self.test_api_endpoint("GET", "/api/game-genres/info",
                                      expected_keys=["total_genres", "total_subgenres"])
        if result["success"]:
            genres = result["data"].get("total_genres", 0)
            subgenres = result["data"].get("total_subgenres", 0)
            self.log_result("Game Genres Info", True,
                           f"Expected 11 genres, 39+ subgenres. Found: {genres} genres, {subgenres} subgenres")
        else:
            self.log_result("Game Genres Info", False, result["error"])
        
        # 2. GET /api/game-genres/all
        result = self.test_api_endpoint("GET", "/api/game-genres/all",
                                      expected_keys=["genres"])
        if result["success"]:
            genres_list = result["data"].get("genres", [])
            genre_names = [g.get("name", "") for g in genres_list]
            self.log_result("All Game Genres", True,
                           f"Found {len(genres_list)} genres: {', '.join(genre_names[:5])}")
        else:
            self.log_result("All Game Genres", False, result["error"])
        
        # 3. GET /api/game-genres/action
        result = self.test_api_endpoint("GET", "/api/game-genres/action",
                                      expected_keys=["name", "subgenres"])
        if result["success"]:
            genre_name = result["data"].get("name", "")
            subgenres = result["data"].get("subgenres", {})
            self.log_result("Action Genre Details", True,
                           f"Genre: {genre_name}, {len(subgenres)} subgenres")
        else:
            self.log_result("Action Genre Details", False, result["error"])
        
        # 4. GET /api/game-genres/action/platformer_2d
        result = self.test_api_endpoint("GET", "/api/game-genres/action/platformer_2d",
                                      expected_keys=["genre", "subgenre", "pipeline"])
        if result["success"]:
            subgenre_info = result["data"].get("subgenre", {})
            pipeline = result["data"].get("pipeline", {})
            assets_needed = pipeline.get("asset_phase", [])
            self.log_result("2D Platformer Subgenre", True,
                           f"Subgenre with full pipeline, {len(assets_needed)} asset types needed")
        else:
            self.log_result("2D Platformer Subgenre", False, result["error"])
        
        # 5. POST /api/game-genres/create-project
        project_request = {
            "name": "My Platformer",
            "genre": "action",
            "subgenre": "platformer_2d",
            "description": "A fun platformer game"
        }
        result = self.test_api_endpoint("POST", "/api/game-genres/create-project",
                                      data=project_request,
                                      expected_keys=["id", "name", "genre"])
        if result["success"]:
            project_id = result["data"].get("id", "")
            project_name = result["data"].get("name", "")
            assets_required = result["data"].get("assets_required", [])
            self.log_result("Create Game Project", True,
                           f"Created project '{project_name}' ({project_id}) with {len(assets_required)} required assets")
        else:
            self.log_result("Create Game Project", False, result["error"])

    def test_ai_log_vault_apis(self):
        """Test all AI Log Vault APIs"""
        print("📊 TESTING AI LOG VAULT APIs")
        print("=" * 50)
        
        # 1. GET /api/ai-logs/info
        result = self.test_api_endpoint("GET", "/api/ai-logs/info",
                                      expected_keys=["name", "statistics", "features"])
        if result["success"]:
            stats = result["data"].get("statistics", {})
            features = result["data"].get("features", [])
            self.log_result("AI Log Vault Info", True,
                           f"System info with {len(features)} features, tracking {len(stats)} metrics")
        else:
            self.log_result("AI Log Vault Info", False, result["error"])
        
        # 2. POST /api/ai-logs/query
        query_log = {
            "query_type": "code_gen",
            "user_input": "write hello world",
            "ai_response": "print('hello world')",
            "model_used": "gpt-4o"
        }
        result = self.test_api_endpoint("POST", "/api/ai-logs/query",
                                      data=query_log,
                                      expected_keys=["status", "log_id"])
        if result["success"]:
            log_id = result["data"].get("log_id", "")
            status = result["data"].get("status", "")
            self.log_result("Log AI Query", True,
                           f"Logged query with ID: {log_id}, status: {status}")
        else:
            self.log_result("Log AI Query", False, result["error"])
        
        # 3. POST /api/ai-logs/action
        action_log = {
            "action_type": "code_written",
            "action_data": {
                "language": "python",
                "lines": 10
            }
        }
        result = self.test_api_endpoint("POST", "/api/ai-logs/action",
                                      data=action_log,
                                      expected_keys=["status", "log_id"])
        if result["success"]:
            log_id = result["data"].get("log_id", "")
            status = result["data"].get("status", "")
            self.log_result("Log User Action", True,
                           f"Logged action with ID: {log_id}, status: {status}")
        else:
            self.log_result("Log User Action", False, result["error"])
        
        # 4. GET /api/ai-logs/stats
        result = self.test_api_endpoint("GET", "/api/ai-logs/stats",
                                      expected_keys=["ai_queries", "user_actions"])
        if result["success"]:
            ai_queries = result["data"].get("ai_queries", {})
            user_actions = result["data"].get("user_actions", {})
            total_queries = ai_queries.get("total", 0)
            total_actions = user_actions.get("total", 0)
            self.log_result("AI Log Statistics", True,
                           f"Total queries: {total_queries}, Total actions: {total_actions}")
        else:
            self.log_result("AI Log Statistics", False, result["error"])
        
        # 5. POST /api/ai-logs/startup-train
        result = self.test_api_endpoint("POST", "/api/ai-logs/startup-train",
                                      expected_keys=["status", "startup_id"])
        if result["success"]:
            startup_id = result["data"].get("startup_id", "")
            status = result["data"].get("status", "")
            self.log_result("Startup Training", True,
                           f"Triggered startup training: {startup_id}, status: {status}")
        else:
            self.log_result("Startup Training", False, result["error"])

    def test_enhanced_jeeves_apis(self):
        """Test Enhanced Jeeves APIs"""
        print("🤖 TESTING ENHANCED JEEVES APIs")
        print("=" * 50)
        
        # 1. GET /api/jeeves/my-learning-profile
        result = self.test_api_endpoint("GET", "/api/jeeves/my-learning-profile",
                                      expected_keys=["vault_summary", "recent_activity"])
        if result["success"]:
            vault_summary = result["data"].get("vault_summary", {})
            recommended = result["data"].get("recommended_next", [])
            self.log_result("Jeeves Learning Profile", True,
                           f"Profile with vault summary and {len(recommended)} recommendations")
        else:
            self.log_result("Jeeves Learning Profile", False, result["error"])
        
        # 2. POST /api/jeeves/ask-with-context
        context_request = {
            "message": "Help me learn Python",
            "skill_level": "beginner"
        }
        result = self.test_api_endpoint("POST", "/api/jeeves/ask-with-context",
                                      data=context_request,
                                      expected_keys=["jeeves_response", "context_used"])
        if result["success"]:
            response_length = len(result["data"].get("jeeves_response", ""))
            context_used = result["data"].get("context_used", False)
            self.log_result("Jeeves Ask with Context", True,
                           f"Response length: {response_length} chars, context used: {context_used}")
        else:
            self.log_result("Jeeves Ask with Context", False, result["error"])
        
        # 3. POST /api/jeeves/interactive-lesson
        lesson_request = {
            "lesson_topic": "variables in Python",
            "skill_level": "beginner"
        }
        result = self.test_api_endpoint("POST", "/api/jeeves/interactive-lesson?lesson_topic=variables%20in%20Python&skill_level=beginner",
                                      expected_keys=["lesson_session", "lesson_content"])
        if result["success"]:
            session_id = result["data"].get("lesson_session", "")
            content_length = len(result["data"].get("lesson_content", ""))
            interactive = result["data"].get("interactive", False)
            self.log_result("Jeeves Interactive Lesson", True,
                           f"Started lesson session {session_id}, content: {content_length} chars, interactive: {interactive}")
        else:
            self.log_result("Jeeves Interactive Lesson", False, result["error"])

    def run_all_tests(self):
        """Run all v11.2 API tests"""
        print("🚀 CODEDOCK v11.2 API TESTING SUITE")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test started: {datetime.utcnow().isoformat()}")
        print()
        
        # Test all API groups
        self.test_masterclass_apis()
        self.test_asset_pipeline_apis()
        self.test_game_genres_apis()
        self.test_ai_log_vault_apis()
        self.test_enhanced_jeeves_apis()
        
        # Print summary
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        # Print failed tests
        failed_tests = [r for r in self.results if not r["success"]]
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        else:
            print("🎉 ALL TESTS PASSED!")
        
        return self.passed_tests, self.total_tests, self.results

if __name__ == "__main__":
    tester = CodeDockTester()
    passed, total, results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)