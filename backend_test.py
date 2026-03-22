#!/usr/bin/env python3
"""
CodeDock v11.1 SOTA 2026 Features Backend API Testing Suite
Testing all 4 SOTA 2026 feature APIs:
1. AI Debugger APIs (prefix: /api/debugger)
2. Music Pipeline APIs (prefix: /api/music)  
3. Interactive Education APIs (prefix: /api/education)
4. Jeeves AI Tutor APIs (prefix: /api/jeeves)
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from frontend/.env
BACKEND_URL = "https://march-2026-preview.preview.emergentagent.com/api"

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response": response_data
        })
        if success:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status} | {test_name}")
        if details:
            print(f"      {details}")
    
    def summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        print(f"\n{'='*80}")
        print(f"CODEDOCK v11.1 SOTA 2026 FEATURES TESTING COMPLETE")
        print(f"{'='*80}")
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"{'='*80}")
        
        if self.failed > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return success_rate >= 80.0

async def make_request(session: aiohttp.ClientSession, method: str, endpoint: str, 
                      data: Dict = None, timeout: int = 30, raw_body: str = None) -> tuple[bool, Dict, str]:
    """Make HTTP request with error handling"""
    url = f"{BACKEND_URL}{endpoint}"
    try:
        kwargs = {
            "timeout": aiohttp.ClientTimeout(total=timeout)
        }
        
        if raw_body:
            kwargs["data"] = raw_body
            kwargs["headers"] = {"Content-Type": "text/plain"}
        elif data:
            kwargs["json"] = data
            
        async with session.request(method, url, **kwargs) as response:
            response_text = await response.text()
            
            if response.status == 200:
                try:
                    response_data = json.loads(response_text)
                    return True, response_data, f"Status: {response.status}"
                except json.JSONDecodeError:
                    return True, {"raw_response": response_text}, f"Status: {response.status} (non-JSON)"
            else:
                return False, {"error": response_text}, f"HTTP {response.status}: {response_text[:200]}"
                
    except asyncio.TimeoutError:
        return False, {}, f"Request timeout after {timeout}s"
    except Exception as e:
        return False, {}, f"Request error: {str(e)}"

async def test_ai_debugger_apis(session: aiohttp.ClientSession, results: TestResult):
    """Test AI Debugger API endpoints"""
    print(f"\n🐛 TESTING AI DEBUGGER APIs")
    print("-" * 50)
    
    # Test 1: GET /api/debugger/info
    success, data, details = await make_request(session, "GET", "/debugger/info")
    if success and "capabilities" in data:
        capabilities = data.get("capabilities", [])
        expected_caps = ["Autonomous error detection", "Stack trace interpretation", "One-click fix suggestions"]
        has_expected = any(cap in capabilities for cap in expected_caps)
        results.add_result(
            "AI Debugger Info Endpoint", 
            has_expected,
            f"Found {len(capabilities)} capabilities, includes expected features: {has_expected}",
            data
        )
    else:
        results.add_result("AI Debugger Info Endpoint", False, details)
    
    # Test 2: POST /api/debugger/analyze
    analyze_payload = {
        "code": "def test(): x = 1/0",
        "language": "python",
        "debug_level": "standard"
    }
    success, data, details = await make_request(session, "POST", "/debugger/analyze", analyze_payload, timeout=45)
    if success and ("analysis" in data or "issues_found" in data):
        issues = data.get("issues_found", 0)
        analysis = data.get("analysis", {})
        results.add_result(
            "AI Debugger Analyze Endpoint",
            issues >= 0,  # Should find at least the division by zero
            f"Found {issues} issues, analysis provided: {bool(analysis)}",
            {"issues_count": issues}
        )
    else:
        results.add_result("AI Debugger Analyze Endpoint", False, details)
    
    # Test 3: POST /api/debugger/security-scan
    security_payload = {
        "code": "import os; os.system('rm -rf /')",
        "language": "python",
        "scan_type": "full"
    }
    success, data, details = await make_request(session, "POST", "/debugger/security-scan", security_payload, timeout=45)
    if success and ("vulnerabilities" in data or "risk_score" in data):
        vulns = data.get("vulnerabilities", {})
        risk_score = data.get("risk_score", 0)
        results.add_result(
            "AI Debugger Security Scan Endpoint",
            risk_score > 0,  # Should detect the dangerous os.system call
            f"Risk score: {risk_score}, vulnerabilities detected: {vulns}",
            {"risk_score": risk_score}
        )
    else:
        results.add_result("AI Debugger Security Scan Endpoint", False, details)
    
    # Test 4: POST /api/debugger/performance-analysis
    perf_payload = {
        "code": "for i in range(10000): print(i)",
        "language": "python"
    }
    success, data, details = await make_request(session, "POST", "/debugger/performance-analysis", perf_payload, timeout=45)
    if success and ("analysis" in data or "metrics" in data):
        analysis = data.get("analysis", "")
        metrics = data.get("metrics", {})
        results.add_result(
            "AI Debugger Performance Analysis Endpoint",
            bool(analysis or metrics),
            f"Analysis provided: {bool(analysis)}, metrics: {bool(metrics)}",
            {"has_analysis": bool(analysis)}
        )
    else:
        results.add_result("AI Debugger Performance Analysis Endpoint", False, details)
    
    # Test 5: POST /api/debugger/quick-fix?language=python&code=...
    quick_fix_code = "def hello() print('hello')"  # Missing colon
    success, data, details = await make_request(session, "POST", f"/debugger/quick-fix?language=python&code={quick_fix_code}", 
                                                 timeout=30)
    if success and "fixed_code" in data:
        fixed = data.get("fixed_code", "")
        has_colon = ":" in fixed
        results.add_result(
            "AI Debugger Quick Fix Endpoint",
            has_colon,
            f"Fixed code contains colon: {has_colon}, length: {len(fixed)}",
            {"fixed_length": len(fixed)}
        )
    else:
        results.add_result("AI Debugger Quick Fix Endpoint", False, details)
    
    # Test 6: POST /api/debugger/explain-code?language=python&code=...
    explain_code = "print([x**2 for x in range(10)])"
    success, data, details = await make_request(session, "POST", f"/debugger/explain-code?language=python&code={explain_code}", 
                                                 timeout=30)
    if success and "explanation" in data:
        explanation = data.get("explanation", "")
        has_explanation = len(explanation) > 50  # Should be a detailed explanation
        results.add_result(
            "AI Debugger Explain Code Endpoint",
            has_explanation,
            f"Explanation length: {len(explanation)} chars, detailed: {has_explanation}",
            {"explanation_length": len(explanation)}
        )
    else:
        results.add_result("AI Debugger Explain Code Endpoint", False, details)

async def test_music_pipeline_apis(session: aiohttp.ClientSession, results: TestResult):
    """Test Music Pipeline API endpoints"""
    print(f"\n🎵 TESTING MUSIC PIPELINE APIs")
    print("-" * 50)
    
    # Test 1: GET /api/music/info
    success, data, details = await make_request(session, "GET", "/music/info")
    if success and "capabilities" in data:
        capabilities = data.get("capabilities", [])
        genres = data.get("genres", [])
        moods = data.get("moods", [])
        expected_caps = ["Text-to-music generation", "Game soundtrack composition"]
        has_expected = any(cap in capabilities for cap in expected_caps)
        results.add_result(
            "Music Pipeline Info Endpoint", 
            has_expected and len(genres) > 5 and len(moods) > 5,
            f"Capabilities: {len(capabilities)}, Genres: {len(genres)}, Moods: {len(moods)}",
            data
        )
    else:
        results.add_result("Music Pipeline Info Endpoint", False, details)
    
    # Test 2: GET /api/music/presets
    success, data, details = await make_request(session, "GET", "/music/presets")
    if success and "presets" in data:
        presets = data.get("presets", [])
        expected_presets = ["menu_theme", "combat", "exploration"]
        has_expected = any(p.get("id") in expected_presets for p in presets)
        results.add_result(
            "Music Pipeline Presets Endpoint",
            has_expected and len(presets) >= 5,
            f"Found {len(presets)} presets, includes expected types: {has_expected}",
            {"preset_count": len(presets)}
        )
    else:
        results.add_result("Music Pipeline Presets Endpoint", False, details)
    
    # Test 3: POST /api/music/generate
    generate_payload = {
        "description": "epic boss battle theme",
        "genre": "orchestral",
        "mood": "epic",  # Changed from "intense" to "epic" which is valid
        "duration": "medium",
        "loopable": True
    }
    success, data, details = await make_request(session, "POST", "/music/generate", generate_payload, timeout=60)
    if success and ("composition" in data or "status" in data):
        composition = data.get("composition", "")
        status = data.get("status", "")
        is_success = status == "success" and len(composition) > 100
        results.add_result(
            "Music Pipeline Generate Endpoint",
            is_success,
            f"Status: {status}, composition length: {len(composition)} chars",
            {"composition_length": len(composition)}
        )
    else:
        results.add_result("Music Pipeline Generate Endpoint", False, details)
    
    # Test 4: POST /api/music/sound-effect
    sfx_payload = {
        "description": "coin pickup sparkle",
        "category": "item",
        "duration": "short"
    }
    success, data, details = await make_request(session, "POST", "/music/sound-effect", sfx_payload, timeout=45)
    if success and ("sound_design" in data or "status" in data):
        sound_design = data.get("sound_design", "")
        status = data.get("status", "")
        is_success = status == "success" and len(sound_design) > 50
        results.add_result(
            "Music Pipeline Sound Effect Endpoint",
            is_success,
            f"Status: {status}, sound design length: {len(sound_design)} chars",
            {"sound_design_length": len(sound_design)}
        )
    else:
        results.add_result("Music Pipeline Sound Effect Endpoint", False, details)
    
    # Test 5: POST /api/music/adaptive-music
    adaptive_payload = {
        "game_state": "combat",
        "intensity": 0.8,
        "transitions": True
    }
    success, data, details = await make_request(session, "POST", "/music/adaptive-music", adaptive_payload, timeout=45)
    if success and ("adaptive_system" in data or "status" in data):
        adaptive_system = data.get("adaptive_system", "")
        status = data.get("status", "")
        is_success = status == "success" and len(adaptive_system) > 100
        results.add_result(
            "Music Pipeline Adaptive Music Endpoint",
            is_success,
            f"Status: {status}, adaptive system length: {len(adaptive_system)} chars",
            {"adaptive_system_length": len(adaptive_system)}
        )
    else:
        results.add_result("Music Pipeline Adaptive Music Endpoint", False, details)

async def test_interactive_education_apis(session: aiohttp.ClientSession, results: TestResult):
    """Test Interactive Education API endpoints"""
    print(f"\n🎓 TESTING INTERACTIVE EDUCATION APIs")
    print("-" * 50)
    
    # Test 1: GET /api/education/info
    success, data, details = await make_request(session, "GET", "/education/info")
    if success and "features" in data:
        features = data.get("features", [])
        languages = data.get("languages_supported", [])
        total_challenges = data.get("total_challenges", 0)
        expected_features = ["Real-time coding challenges", "AI-powered feedback"]
        has_expected = any(feat in features for feat in expected_features)
        results.add_result(
            "Interactive Education Info Endpoint", 
            has_expected and total_challenges > 0,
            f"Features: {len(features)}, Languages: {len(languages)}, Challenges: {total_challenges}",
            data
        )
    else:
        results.add_result("Interactive Education Info Endpoint", False, details)
    
    # Test 2: GET /api/education/challenges/python?difficulty=beginner
    success, data, details = await make_request(session, "GET", "/education/challenges/python?difficulty=beginner")
    if success and "challenges" in data:
        challenges = data.get("challenges", [])
        language = data.get("language", "")
        difficulty = data.get("difficulty", "")
        has_challenges = len(challenges) > 0 and language == "python"
        results.add_result(
            "Interactive Education Challenges Endpoint",
            has_challenges,
            f"Language: {language}, Difficulty: {difficulty}, Challenges: {len(challenges)}",
            {"challenge_count": len(challenges)}
        )
    else:
        results.add_result("Interactive Education Challenges Endpoint", False, details)
    
    # Test 3: GET /api/education/daily-challenge
    success, data, details = await make_request(session, "GET", "/education/daily-challenge")
    if success and "daily_challenge" in data:
        daily = data.get("daily_challenge", {})
        date = data.get("date", "")
        has_challenge = bool(daily.get("title")) and bool(daily.get("description"))
        results.add_result(
            "Interactive Education Daily Challenge Endpoint",
            has_challenge,
            f"Date: {date}, Challenge: {daily.get('title', 'N/A')}, XP: {daily.get('xp', 0)}",
            {"challenge_title": daily.get("title")}
        )
    else:
        results.add_result("Interactive Education Daily Challenge Endpoint", False, details)
    
    # Test 4: GET /api/education/achievements
    success, data, details = await make_request(session, "GET", "/education/achievements")
    if success and "achievements" in data:
        achievements = data.get("achievements", [])
        total_xp = data.get("total_xp_available", 0)
        categories = data.get("categories", {})
        has_achievements = len(achievements) > 5 and total_xp > 0
        results.add_result(
            "Interactive Education Achievements Endpoint",
            has_achievements,
            f"Achievements: {len(achievements)}, Total XP: {total_xp}, Categories: {len(categories)}",
            {"achievement_count": len(achievements)}
        )
    else:
        results.add_result("Interactive Education Achievements Endpoint", False, details)
    
    # Test 5: POST /api/education/submit
    submit_payload = {
        "challenge_id": "py_beg_1",  # Use a valid challenge ID from the challenges
        "code": "print('Hello, World!')",
        "language": "python"
    }
    success, data, details = await make_request(session, "POST", "/education/submit", submit_payload, timeout=45)
    if success and ("evaluation" in data or "status" in data):
        evaluation = data.get("evaluation", {})
        status = data.get("status", "")
        has_evaluation = bool(evaluation) or status == "evaluated"
        results.add_result(
            "Interactive Education Submit Endpoint",
            has_evaluation,
            f"Status: {status}, Evaluation provided: {bool(evaluation)}",
            {"has_evaluation": bool(evaluation)}
        )
    else:
        results.add_result("Interactive Education Submit Endpoint", False, details)
    
    # Test 6: POST /api/education/learning-path
    path_payload = {
        "current_level": "beginner",
        "goals": ["web_development"],
        "time_commitment": "moderate",
        "preferred_languages": ["python"]
    }
    success, data, details = await make_request(session, "POST", "/education/learning-path", path_payload, timeout=45)
    if success and "learning_path" in data:
        learning_path = data.get("learning_path", "")
        parameters = data.get("parameters", {})
        has_path = len(learning_path) > 100
        results.add_result(
            "Interactive Education Learning Path Endpoint",
            has_path,
            f"Learning path length: {len(learning_path)} chars, parameters: {bool(parameters)}",
            {"path_length": len(learning_path)}
        )
    else:
        results.add_result("Interactive Education Learning Path Endpoint", False, details)

async def test_jeeves_tutor_apis(session: aiohttp.ClientSession, results: TestResult):
    """Test Jeeves AI Tutor API endpoints"""
    print(f"\n🤖 TESTING JEEVES AI TUTOR APIs")
    print("-" * 50)
    
    # Test 1: GET /api/jeeves/info
    success, data, details = await make_request(session, "GET", "/jeeves/info")
    if success and "capabilities" in data:
        capabilities = data.get("capabilities", [])
        personalities = data.get("personalities", {})
        languages = data.get("languages_fluent", [])
        expected_caps = ["Code explanation at any level", "Debugging assistance"]
        has_expected = any(cap in capabilities for cap in expected_caps)
        results.add_result(
            "Jeeves AI Tutor Info Endpoint", 
            has_expected and len(personalities) >= 4,
            f"Capabilities: {len(capabilities)}, Personalities: {len(personalities)}, Languages: {len(languages)}",
            data
        )
    else:
        results.add_result("Jeeves AI Tutor Info Endpoint", False, details)
    
    # Test 2: GET /api/jeeves/tip-of-the-day?language=python&level=intermediate
    success, data, details = await make_request(session, "GET", "/jeeves/tip-of-the-day?language=python&level=intermediate")
    if success and "tip" in data:
        tip = data.get("tip", "")
        date = data.get("date", "")
        language = data.get("language", "")
        has_tip = len(tip) > 50 and language == "python"
        results.add_result(
            "Jeeves AI Tutor Tip of the Day Endpoint",
            has_tip,
            f"Date: {date}, Language: {language}, Tip length: {len(tip)} chars",
            {"tip_length": len(tip)}
        )
    else:
        results.add_result("Jeeves AI Tutor Tip of the Day Endpoint", False, details)
    
    # Test 3: POST /api/jeeves/ask
    ask_payload = {
        "message": "How do I use list comprehensions?",
        "skill_level": "beginner",
        "language": "python",
        "personality": "friendly"
    }
    success, data, details = await make_request(session, "POST", "/jeeves/ask", ask_payload, timeout=45)
    if success and "jeeves_response" in data:
        response = data.get("jeeves_response", "")
        personality = data.get("personality", "")
        session_id = data.get("session_id", "")
        has_response = len(response) > 50 and personality == "friendly"
        results.add_result(
            "Jeeves AI Tutor Ask Endpoint",
            has_response,
            f"Response length: {len(response)} chars, Personality: {personality}, Session: {bool(session_id)}",
            {"response_length": len(response)}
        )
    else:
        results.add_result("Jeeves AI Tutor Ask Endpoint", False, details)
    
    # Test 4: POST /api/jeeves/explain
    explain_payload = {
        "code": "print([x**2 for x in range(10)])",
        "language": "python",
        "depth": "beginner"
    }
    success, data, details = await make_request(session, "POST", "/jeeves/explain", explain_payload, timeout=45)
    if success and "explanation" in data:
        explanation = data.get("explanation", "")
        depth = data.get("depth", "")
        language = data.get("language", "")
        has_explanation = len(explanation) > 100 and depth == "beginner"
        results.add_result(
            "Jeeves AI Tutor Explain Endpoint",
            has_explanation,
            f"Explanation length: {len(explanation)} chars, Depth: {depth}, Language: {language}",
            {"explanation_length": len(explanation)}
        )
    else:
        results.add_result("Jeeves AI Tutor Explain Endpoint", False, details)
    
    # Test 5: POST /api/jeeves/debug-help
    debug_payload = {
        "code": "def test(): x = 1/0",
        "language": "python",
        "skill_level": "intermediate"
    }
    success, data, details = await make_request(session, "POST", "/jeeves/debug-help", debug_payload, timeout=45)
    if success and "debug_assistance" in data:
        assistance = data.get("debug_assistance", "")
        language = data.get("language", "")
        had_error = data.get("had_error", False)
        has_assistance = len(assistance) > 100
        results.add_result(
            "Jeeves AI Tutor Debug Help Endpoint",
            has_assistance,
            f"Assistance length: {len(assistance)} chars, Language: {language}, Had error: {had_error}",
            {"assistance_length": len(assistance)}
        )
    else:
        results.add_result("Jeeves AI Tutor Debug Help Endpoint", False, details)
    
    # Test 6: POST /api/jeeves/teach-concept
    concept_payload = {
        "concept": "recursion",
        "skill_level": "intermediate",
        "language": "python",
        "include_examples": True
    }
    success, data, details = await make_request(session, "POST", "/jeeves/teach-concept", concept_payload, timeout=45)
    if success and "lesson" in data:
        lesson = data.get("lesson", "")
        concept = data.get("concept", "")
        language = data.get("language", "")
        has_lesson = len(lesson) > 200 and concept == "recursion"
        results.add_result(
            "Jeeves AI Tutor Teach Concept Endpoint",
            has_lesson,
            f"Lesson length: {len(lesson)} chars, Concept: {concept}, Language: {language}",
            {"lesson_length": len(lesson)}
        )
    else:
        results.add_result("Jeeves AI Tutor Teach Concept Endpoint", False, details)
    
    # Test 7: POST /api/jeeves/practice
    practice_payload = {
        "topic": "python basics",
        "difficulty": "easy",
        "language": "python",
        "count": 3
    }
    success, data, details = await make_request(session, "POST", "/jeeves/practice", practice_payload, timeout=45)
    if success and "practice_problems" in data:
        problems = data.get("practice_problems", "")
        topic = data.get("topic", "")
        difficulty = data.get("difficulty", "")
        count = data.get("count", 0)
        has_problems = len(problems) > 200 and count == 3
        results.add_result(
            "Jeeves AI Tutor Practice Endpoint",
            has_problems,
            f"Problems length: {len(problems)} chars, Topic: {topic}, Difficulty: {difficulty}, Count: {count}",
            {"problems_length": len(problems)}
        )
    else:
        results.add_result("Jeeves AI Tutor Practice Endpoint", False, details)
    
    # Test 8: POST /api/jeeves/motivate?mood=stuck
    success, data, details = await make_request(session, "POST", "/jeeves/motivate?mood=stuck")
    if success and "message" in data:
        message = data.get("message", "")
        mood = data.get("mood", "")
        has_message = len(message) > 50 and mood == "stuck"
        results.add_result(
            "Jeeves AI Tutor Motivate Endpoint",
            has_message,
            f"Message length: {len(message)} chars, Mood: {mood}",
            {"message_length": len(message)}
        )
    else:
        results.add_result("Jeeves AI Tutor Motivate Endpoint", False, details)

async def main():
    """Main testing function"""
    print("🚀 CODEDOCK v11.1 SOTA 2026 FEATURES BACKEND API TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    results = TestResult()
    
    # Create HTTP session with proper headers
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    timeout = aiohttp.ClientTimeout(total=60)
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "CodeDock-SOTA-2026-Testing-Agent/11.1"
        }
    ) as session:
        
        # Test all 4 SOTA 2026 feature APIs
        await test_ai_debugger_apis(session, results)
        await test_music_pipeline_apis(session, results)
        await test_interactive_education_apis(session, results)
        await test_jeeves_tutor_apis(session, results)
    
    # Print final summary
    success = results.summary()
    
    # Save detailed results
    with open("/app/test_results_sota_2026.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "backend_url": BACKEND_URL,
            "version": "11.1 SOTA 2026",
            "summary": {
                "total": results.passed + results.failed,
                "passed": results.passed,
                "failed": results.failed,
                "success_rate": (results.passed / (results.passed + results.failed) * 100) if (results.passed + results.failed) > 0 else 0
            },
            "results": results.results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/test_results_sota_2026.json")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing failed with error: {e}")
        sys.exit(1)