"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CODEDOCK CODE-TO-APP PIPELINE v11.0.0                      ║
║                                                                               ║
║  Complete Code → Production App Pipeline System                               ║
║  - Generates complete application structure                                   ║
║  - Creates deployment configurations                                          ║
║  - Builds tests, docs, and CI/CD                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import uuid
import asyncio
import os
import json

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# AI Integrations
from emergentintegrations.llm.chat import LlmChat, UserMessage

router = APIRouter(prefix="/code-to-app", tags=["Code to App Pipeline"])

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AppGenerationRequest(BaseModel):
    code: str = Field(..., min_length=10, description="Source code to transform into an app")
    language: str = Field("python", description="Programming language of the source")
    app_type: Literal["cli", "web", "api", "mobile", "game", "desktop", "fullstack"] = "web"
    framework: Optional[str] = Field(None, description="Target framework (e.g., FastAPI, React, Flutter)")
    target_platform: Literal["web", "ios", "android", "windows", "macos", "linux", "cross-platform"] = "web"
    features: Optional[List[str]] = Field(default=[], description="Additional features to include")
    include_tests: bool = True
    include_docs: bool = True
    include_deployment: bool = True
    include_cicd: bool = True
    styling: Optional[str] = Field(None, description="UI styling preference (modern, minimal, material, etc.)")

class GameGenerationRequest(BaseModel):
    description: str = Field(..., min_length=20, description="Game concept description")
    game_type: Literal["2d", "3d", "puzzle", "platformer", "rpg", "shooter", "strategy", "casual"] = "2d"
    engine: Literal["pygame", "javascript", "unity", "godot", "phaser", "love2d"] = "javascript"
    features: Optional[List[str]] = Field(default=[], description="Game features to include")
    include_assets: bool = True
    include_sounds: bool = False
    multiplayer: bool = False

class PipelineResult(BaseModel):
    id: str
    status: str
    app_structure: Dict[str, Any]
    files: List[Dict[str, str]]
    instructions: List[str]
    metadata: Dict[str, Any]
    timestamp: str

# ============================================================================
# AI HELPER FUNCTIONS
# ============================================================================

async def call_ai(prompt: str, system_prompt: str, max_tokens: int = 8192) -> str:
    """Call AI with proper error handling"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"codedock-app-{uuid.uuid4().hex[:8]}",
            system_message=system_prompt
        ).with_model("openai", "gpt-4o")
        
        response = await chat.send_message(UserMessage(text=prompt))
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

# ============================================================================
# PIPELINE ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_pipeline_info():
    """Get Code-to-App pipeline information"""
    return {
        "name": "CodeDock Code-to-App Pipeline",
        "version": "11.0.0",
        "description": "Transform code into production-ready applications",
        "supported_app_types": ["cli", "web", "api", "mobile", "game", "desktop", "fullstack"],
        "supported_platforms": ["web", "ios", "android", "windows", "macos", "linux", "cross-platform"],
        "supported_languages": ["python", "javascript", "typescript", "java", "kotlin", "swift", "cpp", "rust", "go"],
        "frameworks": {
            "web": ["react", "vue", "angular", "svelte", "nextjs", "fastapi", "flask", "django", "express"],
            "mobile": ["react-native", "flutter", "kotlin", "swift"],
            "desktop": ["electron", "tauri", "qt", "tkinter"],
            "game": ["pygame", "phaser", "unity", "godot", "love2d"]
        },
        "features": {
            "code_generation": True,
            "test_generation": True,
            "documentation": True,
            "deployment_config": True,
            "cicd_pipeline": True,
            "database_schema": True,
            "api_documentation": True
        }
    }

@router.post("/generate", response_model=PipelineResult)
async def generate_app(request: AppGenerationRequest):
    """Transform code into a complete application"""
    request_id = str(uuid.uuid4())
    
    # Determine framework based on app type if not specified
    framework_map = {
        "web": "react" if request.language in ["javascript", "typescript"] else "fastapi",
        "api": "fastapi" if request.language == "python" else "express",
        "mobile": "react-native",
        "desktop": "electron",
        "game": "pygame" if request.language == "python" else "phaser",
        "cli": None,
        "fullstack": "nextjs"
    }
    framework = request.framework or framework_map.get(request.app_type, "react")
    
    system_prompt = """You are an expert full-stack developer and software architect. 
Your task is to transform provided code into a complete, production-ready application.
Generate clean, well-structured, maintainable code following best practices.
Include proper error handling, security measures, and performance optimizations.
Output should be structured JSON with all necessary files."""

    generation_prompt = f"""Transform this {request.language} code into a complete {request.app_type} application:

```{request.language}
{request.code}
```

**Target Configuration:**
- App Type: {request.app_type}
- Framework: {framework}
- Platform: {request.target_platform}
- Additional Features: {', '.join(request.features) if request.features else 'Standard features'}
- Include Tests: {request.include_tests}
- Include Docs: {request.include_docs}
- Include Deployment: {request.include_deployment}
- Include CI/CD: {request.include_cicd}
{f'- Styling: {request.styling}' if request.styling else ''}

**Generate a complete application with:**

1. **Project Structure** - Full directory layout
2. **Main Application Files** - Core application code adapted for {framework}
3. **Configuration Files** - package.json/requirements.txt, env files, configs
4. **Entry Point** - Main file to start the application
{"5. **Test Suite** - Unit and integration tests" if request.include_tests else ""}
{"6. **Documentation** - README, API docs, setup guide" if request.include_docs else ""}
{"7. **Deployment** - Docker, Kubernetes, or cloud deployment configs" if request.include_deployment else ""}
{"8. **CI/CD Pipeline** - GitHub Actions or similar" if request.include_cicd else ""}

**Output Format:**
Return a JSON object with this structure:
{{
    "project_name": "app-name",
    "structure": {{"directories": [], "description": ""}},
    "files": [
        {{"path": "relative/path/file.ext", "content": "file content", "description": "what this file does"}}
    ],
    "setup_instructions": ["step 1", "step 2"],
    "run_instructions": ["how to run"],
    "dependencies": {{"runtime": [], "dev": []}}
}}

Ensure all code is complete and functional."""

    try:
        result = await call_ai(generation_prompt, system_prompt)
        
        # Try to parse as JSON, fallback to structured response
        try:
            parsed = json.loads(result)
            files = parsed.get("files", [])
            structure = parsed.get("structure", {})
            instructions = parsed.get("setup_instructions", []) + parsed.get("run_instructions", [])
        except json.JSONDecodeError:
            # Structure the raw response
            files = [{"path": "app/main.py", "content": result, "description": "Generated application"}]
            structure = {"directories": ["app"], "description": "Application directory"}
            instructions = ["Review the generated code", "Install dependencies", "Run the application"]
        
        return PipelineResult(
            id=request_id,
            status="success",
            app_structure=structure,
            files=files,
            instructions=instructions,
            metadata={
                "app_type": request.app_type,
                "framework": framework,
                "platform": request.target_platform,
                "language": request.language,
                "features_included": {
                    "tests": request.include_tests,
                    "docs": request.include_docs,
                    "deployment": request.include_deployment,
                    "cicd": request.include_cicd
                },
                "provider": "openai-gpt4o",
                "tokens_estimated": len(result) // 4
            },
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-game", response_model=PipelineResult)
async def generate_game(request: GameGenerationRequest):
    """Generate a complete game from description"""
    request_id = str(uuid.uuid4())
    
    engine_configs = {
        "pygame": {"language": "python", "ext": "py", "run": "python main.py"},
        "javascript": {"language": "javascript", "ext": "js", "run": "open index.html"},
        "phaser": {"language": "javascript", "ext": "js", "run": "npm start"},
        "love2d": {"language": "lua", "ext": "lua", "run": "love ."},
        "godot": {"language": "gdscript", "ext": "gd", "run": "godot project.godot"},
        "unity": {"language": "csharp", "ext": "cs", "run": "open in Unity Editor"}
    }
    
    config = engine_configs.get(request.engine, engine_configs["javascript"])
    
    system_prompt = """You are an expert game developer. Create complete, playable games.
Include all necessary game logic, rendering, input handling, and game states.
Games should be fun, polished, and follow best practices for the chosen engine."""

    game_prompt = f"""Create a complete {request.game_type} game using {request.engine}:

**Game Concept:**
{request.description}

**Requirements:**
- Game Type: {request.game_type}
- Engine: {request.engine}
- Features: {', '.join(request.features) if request.features else 'Core gameplay'}
- Include Asset Placeholders: {request.include_assets}
- Multiplayer Support: {request.multiplayer}

**Must Include:**
1. Complete game loop (init, update, render)
2. Player controls and input handling
3. Game states (menu, playing, paused, game over)
4. Score/progress tracking
5. Collision detection (if applicable)
6. Win/lose conditions
7. Visual feedback and UI
{"8. Placeholder asset descriptions" if request.include_assets else ""}
{"9. Multiplayer networking logic" if request.multiplayer else ""}

**Output Format:**
Return a JSON object:
{{
    "project_name": "game-name",
    "structure": {{"directories": [], "description": ""}},
    "files": [
        {{"path": "file.ext", "content": "code", "description": "what it does"}}
    ],
    "setup_instructions": [],
    "run_instructions": [],
    "controls": {{"key": "action"}},
    "assets_needed": ["list of assets to create"]
}}

Make the game fun and complete!"""

    try:
        result = await call_ai(game_prompt, system_prompt)
        
        try:
            parsed = json.loads(result)
            files = parsed.get("files", [])
            structure = parsed.get("structure", {})
            instructions = parsed.get("setup_instructions", []) + parsed.get("run_instructions", [])
        except json.JSONDecodeError:
            files = [{"path": f"main.{config['ext']}", "content": result, "description": "Main game file"}]
            structure = {"directories": ["assets", "sounds"], "description": "Game directory"}
            instructions = ["Install dependencies", f"Run: {config['run']}"]
        
        return PipelineResult(
            id=request_id,
            status="success",
            app_structure=structure,
            files=files,
            instructions=instructions,
            metadata={
                "game_type": request.game_type,
                "engine": request.engine,
                "language": config["language"],
                "run_command": config["run"],
                "multiplayer": request.multiplayer,
                "provider": "openai-gpt4o"
            },
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class EnhanceCodeRequest(BaseModel):
    code: str = Field(..., min_length=10, description="Code to enhance")
    language: str = "python"
    enhancements: List[str] = ["error_handling", "logging", "typing"]

class ConvertCodeRequest(BaseModel):
    code: str = Field(..., min_length=10)
    from_language: str = "python"
    to_language: str = "javascript"
    preserve_structure: bool = True

@router.post("/enhance")
async def enhance_code(request: EnhanceCodeRequest):
    """Enhance existing code with additional features"""
    request_id = str(uuid.uuid4())
    
    enhancement_descriptions = {
        "error_handling": "Add comprehensive try-catch blocks and error recovery",
        "logging": "Add structured logging throughout the code",
        "typing": "Add type hints and annotations",
        "validation": "Add input validation and sanitization",
        "security": "Add security best practices and sanitization",
        "performance": "Optimize for better performance",
        "testing": "Add inline test helpers",
        "documentation": "Add comprehensive docstrings and comments",
        "async": "Convert to async/await where beneficial",
        "caching": "Add caching for expensive operations"
    }
    
    selected = [enhancement_descriptions.get(e, e) for e in request.enhancements]
    
    prompt = f"""Enhance this {request.language} code with the following improvements:

```{request.language}
{request.code}
```

**Enhancements to apply:**
{chr(10).join(f'- {e}' for e in selected)}

Return the enhanced code with all improvements applied.
Maintain the original functionality while adding the requested features.
Include comments explaining the enhancements made."""

    try:
        result = await call_ai(prompt, "You are an expert code reviewer and enhancer.")
        
        return {
            "id": request_id,
            "status": "success",
            "original_code": request.code,
            "enhanced_code": result,
            "enhancements_applied": request.enhancements,
            "language": request.language,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/convert")
async def convert_code(request: ConvertCodeRequest):
    """Convert code from one language to another"""
    request_id = str(uuid.uuid4())
    
    prompt = f"""Convert this {request.from_language} code to {request.to_language}:

```{request.from_language}
{request.code}
```

**Requirements:**
- {"Preserve the original structure and naming" if request.preserve_structure else "Optimize for the target language idioms"}
- Use {request.to_language} best practices and conventions
- Maintain all functionality
- Add appropriate type annotations for {request.to_language}
- Include equivalent error handling

Return only the converted code with brief comments explaining any non-obvious translations."""

    try:
        result = await call_ai(prompt, f"You are an expert in both {request.from_language} and {request.to_language}.")
        
        return {
            "id": request_id,
            "status": "success",
            "original": {"code": request.code, "language": request.from_language},
            "converted": {"code": result, "language": request.to_language},
            "preserve_structure": request.preserve_structure,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_app_templates():
    """Get available app templates for quick start"""
    return {
        "templates": [
            {
                "id": "web-api",
                "name": "REST API",
                "description": "Production-ready REST API with authentication",
                "stack": ["FastAPI", "PostgreSQL", "Docker"],
                "features": ["JWT Auth", "CRUD", "Validation", "OpenAPI Docs"]
            },
            {
                "id": "web-fullstack",
                "name": "Fullstack Web App",
                "description": "Complete web application with frontend and backend",
                "stack": ["Next.js", "FastAPI", "PostgreSQL"],
                "features": ["Auth", "Dashboard", "Real-time", "Responsive"]
            },
            {
                "id": "mobile-app",
                "name": "Cross-Platform Mobile",
                "description": "iOS and Android app from single codebase",
                "stack": ["React Native", "Expo", "Firebase"],
                "features": ["Push Notifications", "Offline Mode", "Auth"]
            },
            {
                "id": "game-2d",
                "name": "2D Browser Game",
                "description": "Complete 2D game playable in browser",
                "stack": ["Phaser", "TypeScript", "Vite"],
                "features": ["Physics", "Sprites", "Audio", "Leaderboard"]
            },
            {
                "id": "cli-tool",
                "name": "CLI Application",
                "description": "Command-line tool with rich interface",
                "stack": ["Python", "Rich", "Click"],
                "features": ["Subcommands", "Config", "Progress Bars"]
            },
            {
                "id": "desktop-app",
                "name": "Desktop Application",
                "description": "Cross-platform desktop app",
                "stack": ["Electron", "React", "SQLite"],
                "features": ["Tray Icon", "Auto-Update", "Native Menus"]
            }
        ]
    }
