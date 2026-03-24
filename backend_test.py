#!/usr/bin/env python3
"""
Backend API Testing for CodeDock v15.0 - New Pipeline APIs
Testing: NPC Pipeline, Game Logic Pipeline, Animation Pipeline, Jeeves Core
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from frontend .env
BACKEND_URL = "https://synergy-learn-1.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint and return results."""
        self.total_tests += 1
        
        try:
            url = f"{BACKEND_URL}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            success = response.status_code == expected_status
            if success:
                self.passed_tests += 1
            
            result = {
                "method": method.upper(),
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_size": len(response.text),
                "error": None if success else f"Expected {expected_status}, got {response.status_code}"
            }
            
            # Try to parse JSON response
            try:
                result["response_data"] = response.json()
            except:
                result["response_data"] = {"raw": response.text[:500]}
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                "method": method.upper(),
                "endpoint": endpoint,
                "success": False,
                "error": "Request timeout (30s)",
                "status_code": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "method": method.upper(),
                "endpoint": endpoint,
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def run_npc_pipeline_tests(self):
        """Test NPC Pipeline v15.0 endpoints."""
        print("\n🎭 TESTING NPC PIPELINE v15.0")
        print("=" * 50)
        
        # Test 1: Pipeline Overview
        result = self.test_endpoint("GET", "/npc-pipeline/overview")
        self.results.append(result)
        print(f"✅ GET /npc-pipeline/overview: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   Pipeline: {data.get('pipeline', 'N/A')}")
            print(f"   Archetypes: {len(data.get('archetypes', []))} available")
        
        # Test 2: Generate NPC from description
        npc_request = {
            "description": "A wise merchant with a cunning personality",
            "include_dialogue": True,
            "include_quests": True
        }
        result = self.test_endpoint("POST", "/npc-pipeline/generate", npc_request)
        self.results.append(result)
        print(f"✅ POST /npc-pipeline/generate: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'npc' in data:
                npc = data['npc']
                print(f"   Generated NPC: {npc.get('name', 'N/A')} ({npc.get('archetype', 'N/A')})")
                print(f"   Components: {len(data.get('generation_metadata', {}).get('components_generated', []))}")
        
        # Test 3: Get NPC Archetypes
        result = self.test_endpoint("GET", "/npc-pipeline/archetypes")
        self.results.append(result)
        print(f"✅ GET /npc-pipeline/archetypes: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   Available archetypes: {len(data.get('archetypes', []))}")
    
    def run_game_logic_pipeline_tests(self):
        """Test Game Logic Pipeline v15.0 endpoints."""
        print("\n🎮 TESTING GAME LOGIC PIPELINE v15.0")
        print("=" * 50)
        
        # Test 1: Pipeline Overview
        result = self.test_endpoint("GET", "/game-logic-pipeline/overview")
        self.results.append(result)
        print(f"✅ GET /game-logic-pipeline/overview: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   Pipeline: {data.get('pipeline', 'N/A')}")
            print(f"   Combat styles: {len(data.get('combat_styles', []))}")
        
        # Test 2: Generate Combat System
        combat_request = {
            "style": "turn_based",
            "include_magic": True,
            "party_based": True
        }
        result = self.test_endpoint("POST", "/game-logic-pipeline/combat/generate", combat_request)
        self.results.append(result)
        print(f"✅ POST /game-logic-pipeline/combat/generate: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'combat_system' in data:
                combat = data['combat_system']
                print(f"   Combat style: {combat.get('style', 'N/A')}")
                print(f"   Status effects: {len(combat.get('status_effects', []))}")
        
        # Test 3: Generate Progression System
        progression_request = {
            "style": "skill_tree",
            "max_level": 50,
            "skill_tree_branches": 3
        }
        result = self.test_endpoint("POST", "/game-logic-pipeline/progression/generate", progression_request)
        self.results.append(result)
        print(f"✅ POST /game-logic-pipeline/progression/generate: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'progression_system' in data:
                prog = data['progression_system']
                print(f"   Max level: {prog.get('level_cap', 'N/A')}")
                print(f"   XP table entries: {len(prog.get('xp_table', []))}")
    
    def run_animation_pipeline_tests(self):
        """Test Animation Pipeline v15.0 endpoints."""
        print("\n🎬 TESTING ANIMATION PIPELINE v15.0")
        print("=" * 50)
        
        # Test 1: Pipeline Overview
        result = self.test_endpoint("GET", "/animation-pipeline/overview")
        self.results.append(result)
        print(f"✅ GET /animation-pipeline/overview: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   Pipeline: {data.get('pipeline', 'N/A')}")
            print(f"   Rig types: {len(data.get('rig_types', []))}")
        
        # Test 2: Generate Skeleton/Rig
        rig_request = {
            "description": "humanoid character",
            "include_fingers": True
        }
        result = self.test_endpoint("POST", "/animation-pipeline/rig/generate", rig_request)
        self.results.append(result)
        print(f"✅ POST /animation-pipeline/rig/generate: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'skeleton' in data:
                skeleton = data['skeleton']
                print(f"   Rig type: {skeleton.get('type', 'N/A')}")
                print(f"   Bone count: {skeleton.get('metadata', {}).get('bone_count', 'N/A')}")
        
        # Test 3: Generate Animation
        anim_request = {
            "description": "character walking",
            "looping": True
        }
        result = self.test_endpoint("POST", "/animation-pipeline/animation/generate", anim_request)
        self.results.append(result)
        print(f"✅ POST /animation-pipeline/animation/generate: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'animation' in data:
                anim = data['animation']
                print(f"   Animation type: {anim.get('type', 'N/A')}")
                print(f"   Duration: {anim.get('duration', 'N/A')}s")
                print(f"   Keyframes: {len(anim.get('keyframes', []))}")
    
    def run_jeeves_core_tests(self):
        """Test Jeeves Core v15.0 endpoints."""
        print("\n🤖 TESTING JEEVES CORE v15.0")
        print("=" * 50)
        
        # Test 1: Core Overview
        result = self.test_endpoint("GET", "/jeeves-core/overview")
        self.results.append(result)
        print(f"✅ GET /jeeves-core/overview: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   System: {data.get('system', 'N/A')}")
            components = data.get('components', {})
            print(f"   System laws: {components.get('system_laws', {}).get('count', 'N/A')}")
        
        # Test 2: Get All System Laws
        result = self.test_endpoint("GET", "/jeeves-core/system-laws/all")
        self.results.append(result)
        print(f"✅ GET /jeeves-core/system-laws/all: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            print(f"   Total blurbs: {data.get('total_blurbs', 'N/A')}")
            print(f"   Total characters: {data.get('total_characters', 'N/A')}")
        
        # Test 3: Get All Matrices
        result = self.test_endpoint("GET", "/jeeves-core/matrices")
        self.results.append(result)
        print(f"✅ GET /jeeves-core/matrices: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            matrices = data.get('matrices', {})
            print(f"   Available matrices: {len(matrices)}")
            for name, matrix in matrices.items():
                print(f"     - {matrix.get('name', name)}")
        
        # Test 4: Start Co-coding Session
        cocoding_request = {
            "user_id": "test_user_123",
            "pipeline": "npc",
            "initial_prompt": "Create a merchant character",
            "skill_level": "intermediate"
        }
        result = self.test_endpoint("POST", "/jeeves-core/co-coding/session", cocoding_request)
        self.results.append(result)
        print(f"✅ POST /jeeves-core/co-coding/session: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'session' in data:
                session = data['session']
                print(f"   Session ID: {session.get('id', 'N/A')[:8]}...")
                print(f"   Pipeline: {session.get('pipeline', 'N/A')}")
                print(f"   Skill level: {session.get('skill_level', 'N/A')}")
        
        # Test 5: Prompt Refinement
        prompt_request = {
            "original_prompt": "make npc",
            "context": "game development",
            "target_pipeline": "npc"
        }
        result = self.test_endpoint("POST", "/jeeves-core/prompt/refine", prompt_request)
        self.results.append(result)
        print(f"✅ POST /jeeves-core/prompt/refine: {result['success']} (Status: {result.get('status_code', 'N/A')})")
        if result['success'] and 'response_data' in result:
            data = result['response_data']
            if data.get('success') and 'refinement' in data:
                refinement = data['refinement']
                print(f"   Quality score: {refinement.get('quality_score', 'N/A')}/100")
                print(f"   Suggestions: {len(refinement.get('suggestions', []))}")
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print("🎯 CODEDOCK v15.0 BACKEND API TESTING COMPLETE")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {self.passed_tests}/{self.total_tests} tests passed ({success_rate:.1f}%)")
        print()
        
        # Group results by pipeline
        pipelines = {
            "NPC Pipeline": [r for r in self.results if "/npc-pipeline/" in r['endpoint']],
            "Game Logic Pipeline": [r for r in self.results if "/game-logic-pipeline/" in r['endpoint']],
            "Animation Pipeline": [r for r in self.results if "/animation-pipeline/" in r['endpoint']],
            "Jeeves Core": [r for r in self.results if "/jeeves-core/" in r['endpoint']]
        }
        
        for pipeline_name, pipeline_results in pipelines.items():
            if pipeline_results:
                passed = sum(1 for r in pipeline_results if r['success'])
                total = len(pipeline_results)
                rate = (passed / total * 100) if total > 0 else 0
                
                status = "✅" if rate == 100 else "⚠️" if rate >= 50 else "❌"
                print(f"{status} {pipeline_name}: {passed}/{total} ({rate:.1f}%)")
                
                # Show failed tests
                failed = [r for r in pipeline_results if not r['success']]
                if failed:
                    for fail in failed:
                        print(f"   ❌ {fail['method']} {fail['endpoint']}: {fail.get('error', 'Unknown error')}")
        
        print()
        
        # Critical issues
        critical_failures = [r for r in self.results if not r['success'] and r.get('status_code') in [500, None]]
        if critical_failures:
            print("🚨 CRITICAL ISSUES:")
            for fail in critical_failures:
                print(f"   - {fail['method']} {fail['endpoint']}: {fail.get('error', 'Unknown error')}")
            print()
        
        # Success highlights
        if success_rate >= 80:
            print("🎉 EXCELLENT: All major v15.0 pipeline APIs are functional!")
        elif success_rate >= 60:
            print("✅ GOOD: Most v15.0 pipeline APIs are working correctly.")
        else:
            print("⚠️ ATTENTION NEEDED: Several v15.0 APIs require fixes.")
        
        print(f"\n🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

def main():
    """Run all v15.0 backend API tests."""
    print("🚀 STARTING CODEDOCK v15.0 BACKEND API TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = BackendTester()
    
    try:
        # Test all v15.0 pipelines
        tester.run_npc_pipeline_tests()
        tester.run_game_logic_pipeline_tests()
        tester.run_animation_pipeline_tests()
        tester.run_jeeves_core_tests()
        
        # Print final summary
        tester.print_summary()
        
        # Return appropriate exit code
        success_rate = (tester.passed_tests / tester.total_tests * 100) if tester.total_tests > 0 else 0
        return 0 if success_rate >= 80 else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())