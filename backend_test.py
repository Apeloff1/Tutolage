#!/usr/bin/env python3
"""
CodeDock v11.0.0 Backend API Testing Suite
Testing new features: Code-to-App Pipeline, Image Generation Pipeline, and existing v11 APIs
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from frontend/.env
BACKEND_URL = "https://devlearning-hub-1.preview.emergentagent.com/api"

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
        print(f"CODEDOCK v11.0.0 BACKEND TESTING COMPLETE")
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
                      data: Dict = None, timeout: int = 30) -> tuple[bool, Dict, str]:
    """Make HTTP request with error handling"""
    url = f"{BACKEND_URL}{endpoint}"
    try:
        async with session.request(
            method, 
            url, 
            json=data if data else None,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
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

async def test_code_to_app_pipeline(session: aiohttp.ClientSession, results: TestResult):
    """Test Code-to-App Pipeline endpoints"""
    print(f"\n🔧 TESTING CODE-TO-APP PIPELINE")
    print("-" * 50)
    
    # Test 1: GET /api/code-to-app/info
    success, data, details = await make_request(session, "GET", "/code-to-app/info")
    if success and "supported_app_types" in data:
        app_types = data.get("supported_app_types", [])
        frameworks = data.get("frameworks", {})
        expected_types = ["cli", "web", "api", "mobile", "game", "desktop", "fullstack"]
        has_expected = all(t in app_types for t in expected_types)
        results.add_result(
            "Code-to-App Info Endpoint", 
            has_expected,
            f"Found {len(app_types)} app types, {len(frameworks)} framework categories",
            data
        )
    else:
        results.add_result("Code-to-App Info Endpoint", False, details)
    
    # Test 2: GET /api/code-to-app/templates
    success, data, details = await make_request(session, "GET", "/code-to-app/templates")
    if success and "templates" in data:
        templates = data.get("templates", [])
        expected_count = 6  # Based on the code
        results.add_result(
            "Code-to-App Templates Endpoint",
            len(templates) >= expected_count,
            f"Found {len(templates)} templates (expected >= {expected_count})",
            data
        )
    else:
        results.add_result("Code-to-App Templates Endpoint", False, details)
    
    # Test 3: POST /api/code-to-app/enhance
    enhance_payload = {
        "code": "def hello(): print('hello')",
        "language": "python",
        "enhancements": ["error_handling", "typing"]
    }
    success, data, details = await make_request(session, "POST", "/code-to-app/enhance", enhance_payload)
    if success and "enhanced_code" in data:
        enhanced = data.get("enhanced_code", "")
        has_enhancements = "try" in enhanced.lower() or "except" in enhanced.lower()
        results.add_result(
            "Code Enhancement Endpoint",
            has_enhancements,
            f"Enhanced code length: {len(enhanced)} chars, contains error handling: {has_enhancements}",
            {"enhanced_length": len(enhanced)}
        )
    else:
        results.add_result("Code Enhancement Endpoint", False, details)
    
    # Test 4: POST /api/code-to-app/convert
    convert_payload = {
        "code": "def add(a, b): return a + b",
        "from_language": "python",
        "to_language": "javascript"
    }
    success, data, details = await make_request(session, "POST", "/code-to-app/convert", convert_payload)
    if success and "converted" in data:
        converted = data.get("converted", {}).get("code", "")
        is_js = "function" in converted.lower() or "=>" in converted
        results.add_result(
            "Code Conversion Endpoint",
            is_js,
            f"Converted to JavaScript: {len(converted)} chars, contains JS syntax: {is_js}",
            {"converted_length": len(converted)}
        )
    else:
        results.add_result("Code Conversion Endpoint", False, details)

async def test_image_generation_pipeline(session: aiohttp.ClientSession, results: TestResult):
    """Test Image Generation Pipeline endpoints"""
    print(f"\n🎨 TESTING IMAGE GENERATION PIPELINE")
    print("-" * 50)
    
    # Test 1: GET /api/imagine/info
    success, data, details = await make_request(session, "GET", "/imagine/info")
    if success and "providers" in data:
        providers = data.get("providers", [])
        provider_names = [p.get("name", "") for p in providers]
        expected_providers = ["OpenAI gpt-image-1", "Gemini Nano Banana", "Grok Imagine"]
        has_expected = len(providers) >= 3
        results.add_result(
            "Image Generation Info Endpoint",
            has_expected,
            f"Found {len(providers)} providers: {', '.join(provider_names)}",
            data
        )
    else:
        results.add_result("Image Generation Info Endpoint", False, details)
    
    # Test 2: POST /api/imagine/enhance-prompt (using query parameters)
    success, data, details = await make_request(session, "POST", "/imagine/enhance-prompt?prompt=a cat&style=realistic&provider=openai", None, timeout=45)
    if success and "enhanced_prompt" in data:
        enhanced = data.get("enhanced_prompt", "")
        original_prompt = "a cat"
        is_enhanced = len(enhanced) > len(original_prompt) * 2
        results.add_result(
            "Image Prompt Enhancement Endpoint",
            is_enhanced,
            f"Enhanced prompt length: {len(enhanced)} chars (original: {len(original_prompt)})",
            {"enhanced_length": len(enhanced)}
        )
    else:
        results.add_result("Image Prompt Enhancement Endpoint", False, details)

async def test_existing_v11_apis(session: aiohttp.ClientSession, results: TestResult):
    """Test existing v11 APIs to ensure they still work"""
    print(f"\n🔍 TESTING EXISTING v11 APIs")
    print("-" * 50)
    
    # Test 1: GET /api/curriculum/info (should show 10 classes)
    success, data, details = await make_request(session, "GET", "/curriculum/info")
    if success:
        classes_count = data.get("total_classes", 0)
        total_hours = data.get("total_hours", 0)
        expected_classes = 10
        results.add_result(
            "Curriculum Info (10 classes check)",
            classes_count >= expected_classes,
            f"Found {classes_count} classes, {total_hours} hours (expected >= {expected_classes} classes)",
            data
        )
    else:
        results.add_result("Curriculum Info (10 classes check)", False, details)
    
    # Test 2: GET /api/vault/info (should show vault stats)
    success, data, details = await make_request(session, "GET", "/vault/info")
    if success:
        vaults = data.get("vaults", {})
        vault_count = len(vaults)
        expected_vaults = 4  # code_blocks, assets, database_schemas, learning_data
        results.add_result(
            "Vault Info Endpoint",
            vault_count >= expected_vaults,
            f"Found {vault_count} vaults (expected >= {expected_vaults})",
            data
        )
    else:
        results.add_result("Vault Info Endpoint", False, details)
    
    # Test 3: POST /api/pipeline/text-to-code (basic text to code generation)
    text_to_code_payload = {
        "description": "Create a simple hello world function",
        "language": "python",
        "provider": "openai"
    }
    success, data, details = await make_request(session, "POST", "/pipeline/text-to-code", text_to_code_payload, timeout=45)
    if success and ("generated_code" in data or "result" in data):
        # Handle different response structures
        code = data.get("generated_code") or data.get("result", {}).get("code", "")
        has_function = "def" in code.lower() or "function" in code.lower()
        results.add_result(
            "AI Pipeline Text-to-Code",
            has_function,
            f"Generated {len(code)} chars of code, contains function definition: {has_function}",
            {"code_length": len(code)}
        )
    else:
        results.add_result("AI Pipeline Text-to-Code", False, details)
    
    # Test 4: GET /api/health
    success, data, details = await make_request(session, "GET", "/health")
    if success:
        status = data.get("status", "")
        is_healthy = status == "healthy"
        results.add_result(
            "Health Check Endpoint",
            is_healthy,
            f"Health status: {status}",
            data
        )
    else:
        results.add_result("Health Check Endpoint", False, details)

async def main():
    """Main testing function"""
    print("🚀 CODEDOCK v11.0.0 BACKEND API TESTING")
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
            "User-Agent": "CodeDock-Testing-Agent/11.0.0"
        }
    ) as session:
        
        # Test all new features
        await test_code_to_app_pipeline(session, results)
        await test_image_generation_pipeline(session, results)
        await test_existing_v11_apis(session, results)
    
    # Print final summary
    success = results.summary()
    
    # Save detailed results
    with open("/app/test_results_detailed.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "backend_url": BACKEND_URL,
            "summary": {
                "total": results.passed + results.failed,
                "passed": results.passed,
                "failed": results.failed,
                "success_rate": (results.passed / (results.passed + results.failed) * 100) if (results.passed + results.failed) > 0 else 0
            },
            "results": results.results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/test_results_detailed.json")
    
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