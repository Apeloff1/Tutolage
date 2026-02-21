from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime
import asyncio
import subprocess
import tempfile
import shutil
import json
import re
from enum import Enum
from abc import ABC, abstractmethod
import traceback
import sys
import io
from contextlib import redirect_stdout, redirect_stderr


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="CodeDock - Multi-Language Compiler API", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#====================================================================================================
# ENUMS AND CONSTANTS
#====================================================================================================

class LanguageType(str, Enum):
    PYTHON = "python"
    HTML = "html"
    JAVASCRIPT = "javascript"
    CPP = "cpp"
    CSS = "css"
    JSON_LANG = "json"
    MARKDOWN = "markdown"
    SQL = "sql"
    CUSTOM = "custom"

class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    PENDING = "pending"
    RUNNING = "running"

class AddonStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ERROR = "error"

# Language configurations
LANGUAGE_CONFIG = {
    LanguageType.PYTHON: {
        "name": "Python",
        "extension": ".py",
        "icon": "logo-python",
        "color": "#3776AB",
        "executable": True,
        "version": "3.x",
        "description": "General-purpose programming language"
    },
    LanguageType.HTML: {
        "name": "HTML",
        "extension": ".html",
        "icon": "logo-html5",
        "color": "#E34F26",
        "executable": True,
        "version": "5",
        "description": "Markup language for web pages"
    },
    LanguageType.JAVASCRIPT: {
        "name": "JavaScript",
        "extension": ".js",
        "icon": "logo-javascript",
        "color": "#F7DF1E",
        "executable": True,
        "version": "ES6+",
        "description": "Dynamic programming language for web"
    },
    LanguageType.CPP: {
        "name": "C++",
        "extension": ".cpp",
        "icon": "code-slash",
        "color": "#00599C",
        "executable": True,
        "version": "17",
        "description": "High-performance systems language"
    },
    LanguageType.CSS: {
        "name": "CSS",
        "extension": ".css",
        "icon": "logo-css3",
        "color": "#1572B6",
        "executable": False,
        "version": "3",
        "description": "Stylesheet language for web"
    },
    LanguageType.JSON_LANG: {
        "name": "JSON",
        "extension": ".json",
        "icon": "code-working",
        "color": "#000000",
        "executable": False,
        "version": "RFC 8259",
        "description": "Data interchange format"
    },
    LanguageType.MARKDOWN: {
        "name": "Markdown",
        "extension": ".md",
        "icon": "document-text",
        "color": "#083FA1",
        "executable": False,
        "version": "CommonMark",
        "description": "Lightweight markup language"
    },
    LanguageType.SQL: {
        "name": "SQL",
        "extension": ".sql",
        "icon": "server",
        "color": "#CC2927",
        "executable": False,
        "version": "Standard",
        "description": "Database query language"
    }
}

# Code templates
CODE_TEMPLATES = {
    LanguageType.PYTHON: {
        "hello_world": 'print("Hello, World!")',
        "function": 'def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Developer"))',
        "class": 'class Calculator:\n    def __init__(self):\n        self.result = 0\n    \n    def add(self, x):\n        self.result += x\n        return self\n    \n    def subtract(self, x):\n        self.result -= x\n        return self\n\ncalc = Calculator()\nprint(calc.add(10).subtract(3).result)',
        "loop": 'for i in range(5):\n    print(f"Iteration {i}")'
    },
    LanguageType.HTML: {
        "hello_world": '<!DOCTYPE html>\n<html>\n<head>\n    <title>Hello World</title>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n</body>\n</html>',
        "form": '<!DOCTYPE html>\n<html>\n<head>\n    <title>Form Example</title>\n    <style>\n        body { font-family: Arial; padding: 20px; }\n        input { margin: 10px 0; padding: 8px; }\n        button { background: #007bff; color: white; padding: 10px 20px; border: none; }\n    </style>\n</head>\n<body>\n    <form>\n        <input type="text" placeholder="Name"><br>\n        <input type="email" placeholder="Email"><br>\n        <button type="submit">Submit</button>\n    </form>\n</body>\n</html>',
        "styled": '<!DOCTYPE html>\n<html>\n<head>\n    <title>Styled Page</title>\n    <style>\n        body {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            min-height: 100vh;\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            font-family: Arial;\n        }\n        .card {\n            background: white;\n            padding: 40px;\n            border-radius: 16px;\n            box-shadow: 0 10px 40px rgba(0,0,0,0.2);\n        }\n    </style>\n</head>\n<body>\n    <div class="card">\n        <h1>Welcome!</h1>\n        <p>This is a styled HTML page.</p>\n    </div>\n</body>\n</html>'
    },
    LanguageType.JAVASCRIPT: {
        "hello_world": 'console.log("Hello, World!");',
        "function": 'function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}\n\nfor (let i = 0; i < 10; i++) {\n    console.log(`Fib(${i}) = ${fibonacci(i)}`);\n}',
        "async": 'async function fetchData() {\n    console.log("Fetching data...");\n    await new Promise(r => setTimeout(r, 1000));\n    console.log("Data received!");\n    return { status: "success", data: [1, 2, 3] };\n}\n\nfetchData().then(result => console.log(result));',
        "array": 'const numbers = [1, 2, 3, 4, 5];\n\nconst doubled = numbers.map(n => n * 2);\nconst filtered = numbers.filter(n => n > 2);\nconst sum = numbers.reduce((a, b) => a + b, 0);\n\nconsole.log("Original:", numbers);\nconsole.log("Doubled:", doubled);\nconsole.log("Filtered:", filtered);\nconsole.log("Sum:", sum);'
    },
    LanguageType.CPP: {
        "hello_world": '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
        "class": '#include <iostream>\n#include <string>\n\nclass Person {\nprivate:\n    std::string name;\n    int age;\npublic:\n    Person(std::string n, int a) : name(n), age(a) {}\n    void introduce() {\n        std::cout << "Hi, I am " << name << ", " << age << " years old." << std::endl;\n    }\n};\n\nint main() {\n    Person p("Developer", 25);\n    p.introduce();\n    return 0;\n}',
        "algorithm": '#include <iostream>\n#include <vector>\n#include <algorithm>\n\nint main() {\n    std::vector<int> nums = {5, 2, 8, 1, 9, 3};\n    \n    std::sort(nums.begin(), nums.end());\n    \n    std::cout << "Sorted: ";\n    for (int n : nums) {\n        std::cout << n << " ";\n    }\n    std::cout << std::endl;\n    return 0;\n}'
    }
}

#====================================================================================================
# PYDANTIC MODELS - Complex Data Structures
#====================================================================================================

class ExecutionResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ExecutionStatus = ExecutionStatus.PENDING
    output: str = ""
    error: str = ""
    execution_time_ms: float = 0
    memory_used_kb: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CodeExecutionRequest(BaseModel):
    code: str
    language: LanguageType
    input_data: Optional[str] = None
    timeout_seconds: int = Field(default=10, ge=1, le=30)
    memory_limit_mb: int = Field(default=128, ge=32, le=512)

class CodeExecutionResponse(BaseModel):
    execution_id: str
    result: ExecutionResult
    language_info: Dict[str, Any]

class CodeFile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    language: LanguageType
    code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_template: bool = False
    tags: List[str] = []
    metadata: Dict[str, Any] = {}

class CodeFileCreate(BaseModel):
    name: str
    language: LanguageType
    code: str
    tags: List[str] = []

class CodeFileUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    tags: Optional[List[str]] = None

class LanguageAddon(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    language_key: str
    name: str
    extension: str
    icon: str
    color: str
    description: str
    status: AddonStatus = AddonStatus.ACTIVE
    executable: bool = False
    custom_executor: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class LanguageAddonCreate(BaseModel):
    language_key: str
    name: str
    extension: str
    icon: str = "code-slash"
    color: str = "#6B7280"
    description: str = ""
    executable: bool = False

class ExecutionHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_id: Optional[str] = None
    language: LanguageType
    code_snippet: str  # First 100 chars
    result: ExecutionResult
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserPreferences(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    theme: str = "dark"
    font_size: int = 14
    tab_size: int = 4
    auto_save: bool = True
    show_line_numbers: bool = True
    word_wrap: bool = True
    default_language: LanguageType = LanguageType.PYTHON
    recent_files: List[str] = []
    favorite_templates: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    font_size: Optional[int] = None
    tab_size: Optional[int] = None
    auto_save: Optional[bool] = None
    show_line_numbers: Optional[bool] = None
    word_wrap: Optional[bool] = None
    default_language: Optional[LanguageType] = None

#====================================================================================================
# CODE EXECUTORS - Abstract Factory Pattern
#====================================================================================================

class CodeExecutor(ABC):
    """Abstract base class for all code executors"""
    
    @abstractmethod
    async def execute(self, code: str, input_data: Optional[str] = None, 
                     timeout: int = 10, memory_limit: int = 128) -> ExecutionResult:
        pass
    
    @abstractmethod
    def validate(self, code: str) -> tuple[bool, str]:
        pass
    
    def sanitize_output(self, output: str, max_length: int = 10000) -> str:
        """Sanitize and truncate output"""
        if len(output) > max_length:
            return output[:max_length] + "\n... [Output truncated]"
        return output

class PythonExecutor(CodeExecutor):
    """Python code executor with sandboxing"""
    
    FORBIDDEN_IMPORTS = [
        'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests',
        'urllib', 'http', 'ftplib', 'smtplib', 'pickle', 'shelve',
        '__builtins__', 'eval', 'exec', 'compile', 'open', 'file'
    ]
    
    async def execute(self, code: str, input_data: Optional[str] = None,
                     timeout: int = 10, memory_limit: int = 128) -> ExecutionResult:
        start_time = datetime.utcnow()
        result = ExecutionResult()
        
        # Validate code first
        is_valid, error_msg = self.validate(code)
        if not is_valid:
            result.status = ExecutionStatus.ERROR
            result.error = error_msg
            return result
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute with timeout
                process = await asyncio.create_subprocess_exec(
                    sys.executable, temp_file,
                    stdin=asyncio.subprocess.PIPE if input_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=input_data.encode() if input_data else None),
                        timeout=timeout
                    )
                    
                    result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
                    result.error = stderr.decode('utf-8', errors='replace')
                    result.status = ExecutionStatus.SUCCESS if process.returncode == 0 else ExecutionStatus.ERROR
                    
                except asyncio.TimeoutError:
                    process.kill()
                    result.status = ExecutionStatus.TIMEOUT
                    result.error = f"Execution timed out after {timeout} seconds"
                    
            finally:
                # Clean up temp file
                os.unlink(temp_file)
                
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = f"Execution failed: {str(e)}"
            logger.error(f"Python execution error: {traceback.format_exc()}")
        
        # Calculate execution time
        end_time = datetime.utcnow()
        result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return result
    
    def validate(self, code: str) -> tuple[bool, str]:
        """Validate Python code for security issues"""
        code_lower = code.lower()
        
        # Check for forbidden imports
        for forbidden in self.FORBIDDEN_IMPORTS:
            patterns = [
                f'import {forbidden}',
                f'from {forbidden}',
                f'__import__("{forbidden}")',
                f"__import__('{forbidden}')"
            ]
            for pattern in patterns:
                if pattern in code_lower:
                    return False, f"Forbidden module: {forbidden}"
        
        # Check for dangerous functions
        dangerous = ['eval(', 'exec(', 'compile(', '__import__(']
        for d in dangerous:
            if d in code_lower:
                return False, f"Forbidden function: {d[:-1]}"
        
        return True, ""

class JavaScriptExecutor(CodeExecutor):
    """JavaScript executor - returns code for WebView execution"""
    
    async def execute(self, code: str, input_data: Optional[str] = None,
                     timeout: int = 10, memory_limit: int = 128) -> ExecutionResult:
        result = ExecutionResult()
        
        is_valid, error_msg = self.validate(code)
        if not is_valid:
            result.status = ExecutionStatus.ERROR
            result.error = error_msg
            return result
        
        # For JavaScript, we return a wrapped version that captures console output
        wrapped_code = f"""
(function() {{
    var __output = [];
    var __originalConsole = console.log;
    console.log = function(...args) {{
        __output.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    }};
    try {{
        {code}
        return {{ status: 'success', output: __output.join('\\n') }};
    }} catch(e) {{
        return {{ status: 'error', error: e.message }};
    }}
}})()
"""
        result.status = ExecutionStatus.SUCCESS
        result.output = wrapped_code
        result.execution_time_ms = 0
        
        return result
    
    def validate(self, code: str) -> tuple[bool, str]:
        # Basic validation for JavaScript
        dangerous = ['eval(', 'Function(', 'document.cookie', 'localStorage', 'sessionStorage']
        for d in dangerous:
            if d in code:
                return False, f"Potentially unsafe: {d}"
        return True, ""

class CppExecutor(CodeExecutor):
    """C++ code executor"""
    
    async def execute(self, code: str, input_data: Optional[str] = None,
                     timeout: int = 10, memory_limit: int = 128) -> ExecutionResult:
        start_time = datetime.utcnow()
        result = ExecutionResult()
        
        is_valid, error_msg = self.validate(code)
        if not is_valid:
            result.status = ExecutionStatus.ERROR
            result.error = error_msg
            return result
        
        temp_dir = None
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            source_file = os.path.join(temp_dir, 'main.cpp')
            output_file = os.path.join(temp_dir, 'main')
            
            # Write source code
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Compile
            compile_process = await asyncio.create_subprocess_exec(
                'g++', '-std=c++17', '-o', output_file, source_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                compile_stdout, compile_stderr = await asyncio.wait_for(
                    compile_process.communicate(),
                    timeout=30
                )
            except asyncio.TimeoutError:
                compile_process.kill()
                result.status = ExecutionStatus.TIMEOUT
                result.error = "Compilation timed out"
                return result
            
            if compile_process.returncode != 0:
                result.status = ExecutionStatus.ERROR
                result.error = f"Compilation failed:\n{compile_stderr.decode('utf-8', errors='replace')}"
                return result
            
            # Execute
            run_process = await asyncio.create_subprocess_exec(
                output_file,
                stdin=asyncio.subprocess.PIPE if input_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    run_process.communicate(input=input_data.encode() if input_data else None),
                    timeout=timeout
                )
                
                result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
                result.error = stderr.decode('utf-8', errors='replace')
                result.status = ExecutionStatus.SUCCESS if run_process.returncode == 0 else ExecutionStatus.ERROR
                
            except asyncio.TimeoutError:
                run_process.kill()
                result.status = ExecutionStatus.TIMEOUT
                result.error = f"Execution timed out after {timeout} seconds"
                
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = f"Execution failed: {str(e)}"
            logger.error(f"C++ execution error: {traceback.format_exc()}")
            
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        end_time = datetime.utcnow()
        result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return result
    
    def validate(self, code: str) -> tuple[bool, str]:
        """Basic C++ code validation"""
        dangerous = ['system(', 'popen(', 'fork(', 'exec', 'unlink(']
        for d in dangerous:
            if d in code:
                return False, f"Potentially unsafe system call: {d}"
        return True, ""

class HTMLExecutor(CodeExecutor):
    """HTML executor - validates and returns for WebView rendering"""
    
    async def execute(self, code: str, input_data: Optional[str] = None,
                     timeout: int = 10, memory_limit: int = 128) -> ExecutionResult:
        result = ExecutionResult()
        
        is_valid, error_msg = self.validate(code)
        if not is_valid:
            result.status = ExecutionStatus.ERROR
            result.error = error_msg
            return result
        
        result.status = ExecutionStatus.SUCCESS
        result.output = code  # Return HTML as-is for WebView
        result.execution_time_ms = 0
        
        return result
    
    def validate(self, code: str) -> tuple[bool, str]:
        # Remove potentially dangerous script content
        dangerous_patterns = [
            r'javascript:',
            r'onclick\s*=',
            r'onerror\s*=',
            r'onload\s*='
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Potentially unsafe pattern detected"
        return True, ""

# Executor Factory
class ExecutorFactory:
    """Factory for creating code executors"""
    
    _executors: Dict[LanguageType, CodeExecutor] = {
        LanguageType.PYTHON: PythonExecutor(),
        LanguageType.JAVASCRIPT: JavaScriptExecutor(),
        LanguageType.CPP: CppExecutor(),
        LanguageType.HTML: HTMLExecutor(),
    }
    
    @classmethod
    def get_executor(cls, language: LanguageType) -> Optional[CodeExecutor]:
        return cls._executors.get(language)
    
    @classmethod
    def is_executable(cls, language: LanguageType) -> bool:
        return language in cls._executors

#====================================================================================================
# API ROUTES
#====================================================================================================

@api_router.get("/")
async def root():
    return {
        "message": "CodeDock API",
        "version": "2.0.0",
        "description": "Multi-Language Compiler Docking System"
    }

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected",
            "executors": "ready"
        }
    }

# Language Routes
@api_router.get("/languages")
async def get_languages():
    """Get all supported languages with their configurations"""
    languages = []
    for lang_type, config in LANGUAGE_CONFIG.items():
        languages.append({
            "key": lang_type.value,
            "type": "builtin",
            **config,
            "executable": ExecutorFactory.is_executable(lang_type)
        })
    
    # Add custom addons from database
    addons = await db.language_addons.find({"status": AddonStatus.ACTIVE}).to_list(100)
    for addon in addons:
        addon['_id'] = str(addon['_id'])
        addon['type'] = 'addon'
        languages.append(addon)
    
    return {"languages": languages}

@api_router.get("/languages/{language_key}")
async def get_language(language_key: str):
    """Get specific language configuration"""
    try:
        lang_type = LanguageType(language_key)
        if lang_type in LANGUAGE_CONFIG:
            return {
                "key": lang_type.value,
                "type": "builtin",
                **LANGUAGE_CONFIG[lang_type],
                "templates": list(CODE_TEMPLATES.get(lang_type, {}).keys())
            }
    except ValueError:
        pass
    
    # Check addons
    addon = await db.language_addons.find_one({"language_key": language_key})
    if addon:
        addon['_id'] = str(addon['_id'])
        return addon
    
    raise HTTPException(status_code=404, detail="Language not found")

# Code Execution Routes
@api_router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute code in the specified language"""
    executor = ExecutorFactory.get_executor(request.language)
    
    if not executor:
        raise HTTPException(
            status_code=400, 
            detail=f"Language {request.language.value} is not executable on server"
        )
    
    result = await executor.execute(
        code=request.code,
        input_data=request.input_data,
        timeout=request.timeout_seconds,
        memory_limit=request.memory_limit_mb
    )
    
    # Store in execution history
    history_entry = ExecutionHistory(
        language=request.language,
        code_snippet=request.code[:100],
        result=result
    )
    await db.execution_history.insert_one(history_entry.dict())
    
    return CodeExecutionResponse(
        execution_id=result.id,
        result=result,
        language_info=LANGUAGE_CONFIG.get(request.language, {})
    )

@api_router.post("/validate")
async def validate_code(request: CodeExecutionRequest):
    """Validate code without executing"""
    executor = ExecutorFactory.get_executor(request.language)
    
    if not executor:
        return {"valid": True, "message": "No validation available for this language"}
    
    is_valid, error_msg = executor.validate(request.code)
    return {"valid": is_valid, "message": error_msg if not is_valid else "Code is valid"}

# Templates Routes
@api_router.get("/templates")
async def get_templates():
    """Get all code templates"""
    templates = {}
    for lang_type, lang_templates in CODE_TEMPLATES.items():
        templates[lang_type.value] = [
            {"name": name, "code": code}
            for name, code in lang_templates.items()
        ]
    return {"templates": templates}

@api_router.get("/templates/{language}")
async def get_language_templates(language: str):
    """Get templates for a specific language"""
    try:
        lang_type = LanguageType(language)
        if lang_type in CODE_TEMPLATES:
            return {
                "language": language,
                "templates": [
                    {"name": name, "code": code}
                    for name, code in CODE_TEMPLATES[lang_type].items()
                ]
            }
    except ValueError:
        pass
    
    raise HTTPException(status_code=404, detail="No templates for this language")

# File Management Routes
@api_router.post("/files", response_model=CodeFile)
async def create_file(file_data: CodeFileCreate):
    """Create a new code file"""
    code_file = CodeFile(**file_data.dict())
    await db.code_files.insert_one(code_file.dict())
    return code_file

@api_router.get("/files")
async def get_files(language: Optional[str] = None, limit: int = 50):
    """Get all saved files"""
    query = {}
    if language:
        query["language"] = language
    
    files = await db.code_files.find(query).sort("updated_at", -1).to_list(limit)
    return {"files": [CodeFile(**f) for f in files]}

@api_router.get("/files/{file_id}")
async def get_file(file_id: str):
    """Get a specific file"""
    file = await db.code_files.find_one({"id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return CodeFile(**file)

@api_router.put("/files/{file_id}", response_model=CodeFile)
async def update_file(file_id: str, update_data: CodeFileUpdate):
    """Update a code file"""
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.code_files.update_one(
        {"id": file_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    
    file = await db.code_files.find_one({"id": file_id})
    return CodeFile(**file)

@api_router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete a code file"""
    result = await db.code_files.delete_one({"id": file_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted successfully"}

# Addon Management Routes
@api_router.post("/addons", response_model=LanguageAddon)
async def create_addon(addon_data: LanguageAddonCreate):
    """Create a new language addon"""
    # Check for duplicate
    existing = await db.language_addons.find_one({"language_key": addon_data.language_key})
    if existing:
        raise HTTPException(status_code=400, detail="Addon with this key already exists")
    
    addon = LanguageAddon(**addon_data.dict())
    await db.language_addons.insert_one(addon.dict())
    return addon

@api_router.get("/addons")
async def get_addons():
    """Get all language addons"""
    addons = await db.language_addons.find().to_list(100)
    return {"addons": [LanguageAddon(**a) for a in addons]}

@api_router.delete("/addons/{addon_id}")
async def delete_addon(addon_id: str):
    """Delete a language addon"""
    result = await db.language_addons.delete_one({"id": addon_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Addon not found")
    return {"message": "Addon deleted successfully"}

# User Preferences Routes
@api_router.get("/preferences")
async def get_preferences():
    """Get user preferences"""
    prefs = await db.user_preferences.find_one({})
    if not prefs:
        # Create default preferences
        default_prefs = UserPreferences()
        await db.user_preferences.insert_one(default_prefs.dict())
        return default_prefs
    return UserPreferences(**prefs)

@api_router.put("/preferences")
async def update_preferences(update_data: UserPreferencesUpdate):
    """Update user preferences"""
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.user_preferences.update_one(
        {},
        {"$set": update_dict},
        upsert=True
    )
    
    prefs = await db.user_preferences.find_one({})
    return UserPreferences(**prefs)

# Execution History Routes
@api_router.get("/history")
async def get_execution_history(limit: int = 20):
    """Get execution history"""
    history = await db.execution_history.find().sort("created_at", -1).to_list(limit)
    return {"history": [ExecutionHistory(**h) for h in history]}

@api_router.delete("/history")
async def clear_execution_history():
    """Clear execution history"""
    await db.execution_history.delete_many({})
    return {"message": "History cleared"}

# Include the router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
