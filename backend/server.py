"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                         CODEDOCK QUANTUM NEXUS v4.0 - EXPANSION READY                            ║
║                    Beyond Bleeding-Edge Multi-Language Compiler Platform                         ║
║                                                                                                  ║
║  Architecture: Plugin-First | Event-Driven | AI-Native | Expansion-Ready | Zero-Trust           ║
║  Standards: 2026+ Hyperscale | Grok-Compatible | SOTA Security | Hotfix-Enabled                 ║
║                                                                                                  ║
║  Features: Teaching Mode | Advanced Hidden Panel | Language Dock System | Tooltips              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Depends, Query, Request, WebSocket
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union, AsyncGenerator, Literal, Callable
import uuid
from datetime import datetime, timedelta
import asyncio
import subprocess
import tempfile
import shutil
import json
import re
import hashlib
import time
from enum import Enum
from abc import ABC, abstractmethod
import traceback
import sys
import io
from contextlib import asynccontextmanager
from collections import defaultdict
import ast
import tokenize
from io import StringIO

# AI Integration
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB with advanced pooling
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(
    mongo_url,
    maxPoolSize=100,
    minPoolSize=20,
    maxIdleTimeMS=45000,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True,
    retryReads=True
)
db = client[os.environ['DB_NAME']]

# Advanced Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-25s | %(funcName)-20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("CodeDock.Nexus")

#====================================================================================================
# SYSTEM VERSION & BUILD INFO
#====================================================================================================

SYSTEM_VERSION = "4.0.0"
SYSTEM_CODENAME = "Nexus"
SYSTEM_BUILD = "2026.02.21-EXPANSION"
SYSTEM_FEATURES = [
    "teaching_mode",
    "tooltips_engine", 
    "hidden_advanced_panel",
    "language_dock_system",
    "expansion_ready",
    "hotfix_system",
    "plugin_architecture",
    "custom_language_support"
]

#====================================================================================================
# ENUMS - Comprehensive Type System
#====================================================================================================

class LanguageType(str, Enum):
    PYTHON = "python"
    HTML = "html"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    CPP = "cpp"
    C = "c"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    CSHARP = "csharp"
    PHP = "php"
    RUBY = "ruby"
    PERL = "perl"
    LUA = "lua"
    R = "r"
    SCALA = "scala"
    HASKELL = "haskell"
    ELIXIR = "elixir"
    CLOJURE = "clojure"
    DART = "dart"
    ZIG = "zig"
    NIM = "nim"
    CRYSTAL = "crystal"
    JULIA = "julia"
    CSS = "css"
    SCSS = "scss"
    LESS = "less"
    JSON_LANG = "json"
    YAML = "yaml"
    TOML = "toml"
    XML = "xml"
    MARKDOWN = "markdown"
    SQL = "sql"
    GRAPHQL = "graphql"
    SHELL = "shell"
    POWERSHELL = "powershell"
    DOCKERFILE = "dockerfile"
    TERRAFORM = "terraform"
    SOLIDITY = "solidity"
    WASM = "wasm"
    CUSTOM = "custom"

class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    PENDING = "pending"
    RUNNING = "running"
    KILLED = "killed"
    MEMORY_EXCEEDED = "memory_exceeded"
    SECURITY_VIOLATION = "security_violation"
    COMPILATION_ERROR = "compilation_error"
    RUNTIME_ERROR = "runtime_error"
    QUEUED = "queued"

class AIAssistantMode(str, Enum):
    EXPLAIN = "explain"
    DEBUG = "debug"
    OPTIMIZE = "optimize"
    COMPLETE = "complete"
    REFACTOR = "refactor"
    DOCUMENT = "document"
    TEST_GEN = "test_gen"
    SECURITY_AUDIT = "security_audit"
    CONVERT = "convert"
    TEACH = "teach"
    REVIEW = "review"
    ARCHITECTURE = "architecture"

class CodeComplexity(str, Enum):
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"
    EXTREME = "extreme"

class SecurityLevel(str, Enum):
    STRICT = "strict"
    STANDARD = "standard"
    PERMISSIVE = "permissive"
    SANDBOX = "sandbox"

class TooltipCategory(str, Enum):
    EDITOR = "editor"
    EXECUTION = "execution"
    AI = "ai"
    FILES = "files"
    SETTINGS = "settings"
    ADVANCED = "advanced"
    LANGUAGE = "language"
    SHORTCUTS = "shortcuts"

class TutorialStep(str, Enum):
    WELCOME = "welcome"
    SELECT_LANGUAGE = "select_language"
    WRITE_CODE = "write_code"
    USE_TEMPLATES = "use_templates"
    RUN_CODE = "run_code"
    VIEW_OUTPUT = "view_output"
    SAVE_FILE = "save_file"
    USE_AI = "use_ai"
    ANALYZE_CODE = "analyze_code"
    ADVANCED_FEATURES = "advanced_features"
    CUSTOM_LANGUAGES = "custom_languages"
    COMPLETE = "complete"

class FeatureFlag(str, Enum):
    TEACHING_MODE = "teaching_mode"
    ADVANCED_PANEL = "advanced_panel"
    AI_SUGGESTIONS = "ai_suggestions"
    CUSTOM_LANGUAGES = "custom_languages"
    EXPANSION_DOCK = "expansion_dock"
    EXPERIMENTAL = "experimental"
    BETA_FEATURES = "beta_features"
    STREAMING_OUTPUT = "streaming_output"
    COLLABORATIVE = "collaborative"
    CLOUD_SYNC = "cloud_sync"

class DockStatus(str, Enum):
    AVAILABLE = "available"
    INSTALLED = "installed"
    PENDING = "pending"
    ERROR = "error"
    DEPRECATED = "deprecated"
    COMING_SOON = "coming_soon"

class HotfixPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ENHANCEMENT = "enhancement"

#====================================================================================================
# LANGUAGE DOCK SYSTEM - Expansion Ready Infrastructure
#====================================================================================================

LANGUAGE_DOCK_REGISTRY = {
    # === TIER 1: FULLY IMPLEMENTED ===
    LanguageType.PYTHON: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "Python",
        "display_name": "Python 3.12+",
        "extension": ".py",
        "extensions_alt": [".pyw", ".pyx", ".pyi"],
        "icon": "logo-python",
        "color": "#3776AB",
        "color_secondary": "#FFD43B",
        "executable": True,
        "version": "3.12+",
        "description": "AI/ML-first programming language with type hints and async support",
        "compiler": "cpython",
        "compiler_version": "3.12.0",
        "paradigms": ["oop", "functional", "procedural", "async", "metaprogramming"],
        "features": ["type_hints", "pattern_matching", "async_await", "dataclasses", "walrus_operator", "structural_pattern_matching"],
        "mime_types": ["text/x-python", "application/x-python-code"],
        "syntax": {
            "comment_single": "#",
            "comment_multi_start": '"""',
            "comment_multi_end": '"""',
            "string_delimiters": ["'", '"', "'''", '"""'],
            "indent_style": "spaces",
            "indent_size": 4,
            "line_ending": "lf",
            "case_sensitive": True
        },
        "keywords": ["def", "class", "import", "from", "async", "await", "yield", "lambda", "match", "case", "with", "try", "except", "finally", "raise", "assert", "pass", "break", "continue", "return", "global", "nonlocal", "del", "in", "is", "not", "and", "or", "True", "False", "None"],
        "builtin_types": ["int", "float", "str", "bool", "list", "dict", "set", "tuple", "bytes", "bytearray", "complex", "frozenset", "range", "slice", "type", "object"],
        "operators": ["+", "-", "*", "/", "//", "%", "**", "@", "&", "|", "^", "~", "<<", ">>", "<", ">", "<=", ">=", "==", "!=", ":="],
        "dock_config": {
            "sandbox_enabled": True,
            "timeout_default": 10,
            "timeout_max": 60,
            "memory_default_mb": 256,
            "memory_max_mb": 1024,
            "network_allowed": False,
            "file_access": "restricted"
        },
        "expansion_hooks": ["pre_execute", "post_execute", "on_error", "on_timeout"]
    },
    LanguageType.JAVASCRIPT: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "JavaScript",
        "display_name": "JavaScript ES2026",
        "extension": ".js",
        "extensions_alt": [".mjs", ".cjs", ".jsx"],
        "icon": "logo-javascript",
        "color": "#F7DF1E",
        "color_secondary": "#323330",
        "executable": True,
        "version": "ES2026",
        "description": "Universal scripting language for web and server",
        "compiler": "v8",
        "paradigms": ["oop", "functional", "event-driven", "async", "prototype"],
        "features": ["modules", "async_await", "proxy", "decorators", "records_tuples", "temporal", "pattern_matching"],
        "syntax": {
            "comment_single": "//",
            "comment_multi_start": "/*",
            "comment_multi_end": "*/",
            "string_delimiters": ["'", '"', "`"],
            "indent_style": "spaces",
            "indent_size": 2
        },
        "keywords": ["const", "let", "var", "async", "await", "class", "import", "export", "function", "return", "if", "else", "for", "while", "do", "switch", "case", "break", "continue", "try", "catch", "finally", "throw", "new", "this", "super", "extends", "static", "get", "set", "yield", "of", "in", "typeof", "instanceof", "delete", "void", "null", "undefined", "true", "false"],
        "dock_config": {
            "sandbox_enabled": True,
            "webview_execution": True,
            "timeout_default": 10,
            "memory_default_mb": 128
        },
        "expansion_hooks": ["pre_execute", "post_execute", "console_intercept"]
    },
    LanguageType.HTML: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "HTML",
        "display_name": "HTML 5.3",
        "extension": ".html",
        "extensions_alt": [".htm", ".xhtml"],
        "icon": "logo-html5",
        "color": "#E34F26",
        "color_secondary": "#F16529",
        "executable": True,
        "version": "5.3",
        "description": "Semantic markup language for modern web applications",
        "compiler": "webview",
        "paradigms": ["declarative"],
        "features": ["web_components", "shadow_dom", "custom_elements", "template_literals", "dialog", "details"],
        "syntax": {
            "comment_single": None,
            "comment_multi_start": "<!--",
            "comment_multi_end": "-->",
            "case_sensitive": False
        },
        "dock_config": {
            "preview_enabled": True,
            "live_reload": True,
            "sanitize_scripts": True
        }
    },
    LanguageType.CPP: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "C++",
        "display_name": "C++23",
        "extension": ".cpp",
        "extensions_alt": [".cc", ".cxx", ".hpp", ".h", ".hxx"],
        "icon": "code-slash",
        "color": "#00599C",
        "color_secondary": "#004482",
        "executable": True,
        "version": "C++23",
        "description": "High-performance systems programming with modern features",
        "compiler": "g++",
        "compiler_flags": ["-std=c++20", "-O2", "-Wall", "-Wextra"],
        "paradigms": ["oop", "generic", "procedural", "functional", "metaprogramming"],
        "features": ["templates", "concepts", "coroutines", "ranges", "modules", "constexpr", "auto", "lambdas", "smart_pointers"],
        "syntax": {
            "comment_single": "//",
            "comment_multi_start": "/*",
            "comment_multi_end": "*/",
            "indent_size": 4
        },
        "keywords": ["class", "struct", "template", "concept", "constexpr", "consteval", "auto", "namespace", "virtual", "override", "final", "public", "private", "protected", "friend", "operator", "new", "delete", "sizeof", "alignof", "typeid", "static_cast", "dynamic_cast", "const_cast", "reinterpret_cast", "nullptr", "true", "false", "if", "else", "for", "while", "do", "switch", "case", "break", "continue", "return", "try", "catch", "throw", "noexcept", "co_await", "co_yield", "co_return"],
        "dock_config": {
            "compilation_required": True,
            "timeout_compile": 30,
            "timeout_execute": 10,
            "memory_default_mb": 256
        }
    },
    LanguageType.C: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "C",
        "display_name": "C23",
        "extension": ".c",
        "extensions_alt": [".h"],
        "icon": "code-slash",
        "color": "#A8B9CC",
        "executable": True,
        "version": "C23",
        "description": "Foundational systems programming language",
        "compiler": "gcc",
        "compiler_flags": ["-std=c17", "-O2", "-Wall"],
        "paradigms": ["procedural"],
        "dock_config": {
            "compilation_required": True,
            "timeout_compile": 30,
            "timeout_execute": 10
        }
    },
    LanguageType.TYPESCRIPT: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "TypeScript",
        "display_name": "TypeScript 5.6+",
        "extension": ".ts",
        "extensions_alt": [".tsx", ".mts", ".cts"],
        "icon": "logo-javascript",
        "color": "#3178C6",
        "executable": True,
        "version": "5.6+",
        "description": "Type-safe JavaScript superset with advanced type system",
        "compiler": "tsc",
        "paradigms": ["oop", "functional", "generic"],
        "features": ["static_types", "interfaces", "generics", "decorators", "mapped_types", "conditional_types", "template_literals"],
        "dock_config": {
            "transpile_to_js": True,
            "type_checking": True
        }
    },
    
    # === TIER 2: DOCK READY (Not Implemented Yet) ===
    LanguageType.RUST: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Rust",
        "display_name": "Rust 2024 Edition",
        "extension": ".rs",
        "icon": "hardware-chip",
        "color": "#DEA584",
        "executable": False,
        "version": "2024 Edition",
        "description": "Memory-safe systems programming with zero-cost abstractions",
        "compiler": "rustc",
        "paradigms": ["oop", "functional", "concurrent", "systems"],
        "features": ["ownership", "borrowing", "lifetimes", "async", "macros", "traits", "pattern_matching"],
        "dock_config": {
            "compilation_required": True,
            "cargo_support": True
        },
        "expansion_ready": True,
        "install_command": "cargo install",
        "dependencies": ["cargo", "rustc"]
    },
    LanguageType.GO: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Go",
        "display_name": "Go 1.23+",
        "extension": ".go",
        "icon": "code-working",
        "color": "#00ADD8",
        "executable": False,
        "version": "1.23+",
        "description": "Cloud-native concurrent programming language",
        "compiler": "go",
        "paradigms": ["procedural", "concurrent"],
        "features": ["goroutines", "channels", "interfaces", "generics", "defer"],
        "dock_config": {
            "go_modules": True
        },
        "expansion_ready": True
    },
    LanguageType.JAVA: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Java",
        "display_name": "Java 21 LTS",
        "extension": ".java",
        "icon": "cafe",
        "color": "#ED8B00",
        "executable": False,
        "version": "21 LTS",
        "description": "Enterprise-grade object-oriented programming",
        "compiler": "javac",
        "paradigms": ["oop", "functional"],
        "features": ["virtual_threads", "pattern_matching", "records", "sealed_classes"],
        "expansion_ready": True
    },
    LanguageType.KOTLIN: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Kotlin",
        "display_name": "Kotlin 2.0",
        "extension": ".kt",
        "extensions_alt": [".kts"],
        "icon": "code-working",
        "color": "#7F52FF",
        "executable": False,
        "version": "2.0",
        "description": "Modern JVM language with null safety and coroutines",
        "compiler": "kotlinc",
        "paradigms": ["oop", "functional"],
        "expansion_ready": True
    },
    LanguageType.SWIFT: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Swift",
        "display_name": "Swift 6.0",
        "extension": ".swift",
        "icon": "logo-apple",
        "color": "#F05138",
        "executable": False,
        "version": "6.0",
        "description": "Apple's powerful and intuitive programming language",
        "compiler": "swiftc",
        "paradigms": ["oop", "functional", "protocol-oriented"],
        "expansion_ready": True
    },
    LanguageType.CSHARP: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "C#",
        "display_name": "C# 12",
        "extension": ".cs",
        "icon": "code-slash",
        "color": "#512BD4",
        "executable": False,
        "version": "12",
        "description": ".NET programming with modern language features",
        "compiler": "dotnet",
        "paradigms": ["oop", "functional"],
        "expansion_ready": True
    },
    LanguageType.RUBY: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "Ruby",
        "display_name": "Ruby 3.3+",
        "extension": ".rb",
        "icon": "diamond",
        "color": "#CC342D",
        "executable": False,
        "version": "3.3+",
        "description": "Dynamic, elegant programming language focused on simplicity",
        "compiler": "ruby",
        "paradigms": ["oop", "functional", "metaprogramming"],
        "expansion_ready": True
    },
    LanguageType.PHP: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "PHP",
        "display_name": "PHP 8.3",
        "extension": ".php",
        "icon": "code-working",
        "color": "#777BB4",
        "executable": False,
        "version": "8.3",
        "description": "Popular server-side scripting language",
        "compiler": "php",
        "expansion_ready": True
    },
    
    # === TIER 3: EXPANSION SLOTS (Future) ===
    LanguageType.JULIA: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Julia",
        "display_name": "Julia 1.10+",
        "extension": ".jl",
        "color": "#9558B2",
        "executable": False,
        "description": "High-performance scientific computing",
        "expansion_ready": True
    },
    LanguageType.ELIXIR: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Elixir",
        "display_name": "Elixir 1.16",
        "extension": ".ex",
        "extensions_alt": [".exs"],
        "color": "#6E4A7E",
        "executable": False,
        "description": "Functional, concurrent programming on BEAM VM",
        "expansion_ready": True
    },
    LanguageType.HASKELL: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Haskell",
        "display_name": "Haskell GHC 9.8",
        "extension": ".hs",
        "color": "#5D4F85",
        "executable": False,
        "description": "Pure functional programming with strong types",
        "expansion_ready": True
    },
    LanguageType.SCALA: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Scala",
        "display_name": "Scala 3",
        "extension": ".scala",
        "color": "#DC322F",
        "executable": False,
        "description": "Functional and object-oriented on the JVM",
        "expansion_ready": True
    },
    LanguageType.DART: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Dart",
        "display_name": "Dart 3.3",
        "extension": ".dart",
        "color": "#0175C2",
        "executable": False,
        "description": "Client-optimized language for Flutter",
        "expansion_ready": True
    },
    LanguageType.ZIG: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Zig",
        "display_name": "Zig 0.12",
        "extension": ".zig",
        "color": "#F7A41D",
        "executable": False,
        "description": "Low-level systems programming with safety",
        "expansion_ready": True
    },
    LanguageType.NIM: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Nim",
        "display_name": "Nim 2.0",
        "extension": ".nim",
        "color": "#FFE953",
        "executable": False,
        "description": "Efficient, expressive, elegant",
        "expansion_ready": True
    },
    LanguageType.SOLIDITY: {
        "tier": 3,
        "status": DockStatus.COMING_SOON,
        "name": "Solidity",
        "display_name": "Solidity 0.8+",
        "extension": ".sol",
        "color": "#363636",
        "executable": False,
        "description": "Smart contract programming for Ethereum",
        "expansion_ready": True
    },
    
    # === MARKUP & DATA LANGUAGES ===
    LanguageType.CSS: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "CSS",
        "display_name": "CSS4",
        "extension": ".css",
        "icon": "logo-css3",
        "color": "#1572B6",
        "executable": False,
        "description": "Modern styling with container queries and nesting"
    },
    LanguageType.JSON_LANG: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "JSON",
        "extension": ".json",
        "icon": "code-working",
        "color": "#000000",
        "executable": False,
        "description": "Data interchange format"
    },
    LanguageType.YAML: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "YAML",
        "extension": ".yaml",
        "extensions_alt": [".yml"],
        "icon": "document-text",
        "color": "#CB171E",
        "executable": False,
        "description": "Human-readable data serialization"
    },
    LanguageType.MARKDOWN: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "Markdown",
        "extension": ".md",
        "icon": "document-text",
        "color": "#083FA1",
        "executable": False,
        "description": "Lightweight markup language"
    },
    LanguageType.SQL: {
        "tier": 1,
        "status": DockStatus.INSTALLED,
        "name": "SQL",
        "extension": ".sql",
        "icon": "server",
        "color": "#CC2927",
        "executable": False,
        "description": "Database query language"
    },
    LanguageType.GRAPHQL: {
        "tier": 2,
        "status": DockStatus.COMING_SOON,
        "name": "GraphQL",
        "extension": ".graphql",
        "extensions_alt": [".gql"],
        "color": "#E10098",
        "executable": False,
        "description": "API query language",
        "expansion_ready": True
    },
}

#====================================================================================================
# TOOLTIPS SYSTEM - State of the Art
#====================================================================================================

TOOLTIPS_REGISTRY = {
    # Editor tooltips
    "editor_line_numbers": {
        "id": "editor_line_numbers",
        "category": TooltipCategory.EDITOR,
        "title": "Line Numbers",
        "description": "Click a line number to set a breakpoint (when debugging is enabled)",
        "shortcut": None,
        "advanced": False,
        "learn_more_url": None
    },
    "editor_code_area": {
        "id": "editor_code_area",
        "category": TooltipCategory.EDITOR,
        "title": "Code Editor",
        "description": "Write your code here. Syntax highlighting is automatic based on the selected language.",
        "tips": [
            "Use Tab for indentation",
            "Select text and press Cmd/Ctrl+D to duplicate",
            "Long-press for AI suggestions"
        ],
        "advanced": False
    },
    "editor_filename": {
        "id": "editor_filename",
        "category": TooltipCategory.EDITOR,
        "title": "File Name",
        "description": "Tap to rename your file. Extension is added automatically.",
        "advanced": False
    },
    
    # Execution tooltips
    "run_button": {
        "id": "run_button",
        "category": TooltipCategory.EXECUTION,
        "title": "Run Code",
        "description": "Execute your code in a secure sandbox environment",
        "tips": [
            "Timeout: 10 seconds (adjustable in Advanced)",
            "Memory limit: 256MB default",
            "Network access is disabled for security"
        ],
        "shortcut": "Cmd/Ctrl + Enter",
        "advanced": False
    },
    "output_panel": {
        "id": "output_panel",
        "category": TooltipCategory.EXECUTION,
        "title": "Output Panel",
        "description": "View execution results, errors, and debug information",
        "tips": [
            "Green text indicates success",
            "Red text indicates errors",
            "Swipe down to dismiss"
        ],
        "advanced": False
    },
    "execution_time": {
        "id": "execution_time",
        "category": TooltipCategory.EXECUTION,
        "title": "Execution Time",
        "description": "Shows how long your code took to execute in milliseconds",
        "advanced": False
    },
    
    # AI tooltips
    "ai_assist_button": {
        "id": "ai_assist_button",
        "category": TooltipCategory.AI,
        "title": "AI Assistant",
        "description": "Get intelligent help with your code using GPT-4o",
        "tips": [
            "Explain: Understand what code does",
            "Debug: Find and fix bugs",
            "Optimize: Improve performance",
            "Refactor: Clean up code structure"
        ],
        "advanced": False
    },
    "ai_modes": {
        "id": "ai_modes",
        "category": TooltipCategory.AI,
        "title": "AI Modes",
        "description": "Choose how AI should help you",
        "modes": {
            "explain": "Get a detailed explanation of your code",
            "debug": "Find bugs and get fix suggestions",
            "optimize": "Improve performance and efficiency",
            "complete": "Auto-complete partial code",
            "refactor": "Restructure for better readability",
            "document": "Generate documentation",
            "test_gen": "Generate unit tests",
            "security_audit": "Check for vulnerabilities",
            "convert": "Convert to another language"
        },
        "advanced": False
    },
    
    # Files tooltips
    "save_button": {
        "id": "save_button",
        "category": TooltipCategory.FILES,
        "title": "Save File",
        "description": "Save your code to the cloud. Access it from any device.",
        "shortcut": "Cmd/Ctrl + S",
        "advanced": False
    },
    "files_button": {
        "id": "files_button",
        "category": TooltipCategory.FILES,
        "title": "My Files",
        "description": "Browse and manage your saved code files",
        "tips": [
            "Tap a file to open it",
            "Swipe left to delete",
            "Star files for quick access"
        ],
        "advanced": False
    },
    
    # Language tooltips
    "language_selector": {
        "id": "language_selector",
        "category": TooltipCategory.LANGUAGE,
        "title": "Language Selection",
        "description": "Choose the programming language for your code",
        "tips": [
            "Languages with ✓ can be executed",
            "Add custom languages via Addons",
            "Each language has its own templates"
        ],
        "advanced": False
    },
    "templates_button": {
        "id": "templates_button",
        "category": TooltipCategory.LANGUAGE,
        "title": "Code Templates",
        "description": "Quick-start with pre-written code examples",
        "tips": [
            "Templates vary by language",
            "Complexity badges show difficulty",
            "Great for learning new concepts"
        ],
        "advanced": False
    },
    
    # Advanced tooltips
    "analyze_button": {
        "id": "analyze_button",
        "category": TooltipCategory.ADVANCED,
        "title": "Code Analysis",
        "description": "Get insights about your code structure and complexity",
        "metrics": [
            "Cyclomatic complexity",
            "Lines of code",
            "Function/class count",
            "Comment ratio"
        ],
        "advanced": True
    },
    "complexity_badge": {
        "id": "complexity_badge",
        "category": TooltipCategory.ADVANCED,
        "title": "Complexity Badge",
        "description": "Shows the cyclomatic complexity of your code",
        "levels": {
            "trivial": "1-5: Very simple, single path",
            "simple": "6-10: Few decision points",
            "moderate": "11-20: Multiple paths",
            "complex": "21-50: Many branches",
            "very_complex": "51+: Consider refactoring"
        },
        "advanced": True
    },
    "hidden_panel": {
        "id": "hidden_panel",
        "category": TooltipCategory.ADVANCED,
        "title": "Advanced Panel",
        "description": "Access experimental and power-user features",
        "access": "Triple-tap the version number in Settings",
        "features": [
            "Custom execution timeout",
            "Memory limit adjustment",
            "Security level selection",
            "Experimental features toggle",
            "Debug mode",
            "Export/Import settings"
        ],
        "advanced": True
    },
    
    # Shortcuts tooltips
    "keyboard_shortcuts": {
        "id": "keyboard_shortcuts",
        "category": TooltipCategory.SHORTCUTS,
        "title": "Keyboard Shortcuts",
        "description": "Speed up your workflow with keyboard shortcuts",
        "shortcuts": {
            "run": "Cmd/Ctrl + Enter",
            "save": "Cmd/Ctrl + S",
            "new_file": "Cmd/Ctrl + N",
            "find": "Cmd/Ctrl + F",
            "ai_assist": "Cmd/Ctrl + Shift + A",
            "toggle_theme": "Cmd/Ctrl + Shift + T",
            "analyze": "Cmd/Ctrl + Shift + L"
        },
        "advanced": False
    }
}

#====================================================================================================
# TEACHING MODE SYSTEM - Step by Step Tutorial
#====================================================================================================

TUTORIAL_STEPS = {
    TutorialStep.WELCOME: {
        "order": 0,
        "title": "Welcome to CodeDock Quantum!",
        "description": "Your powerful mobile code compiler and AI assistant",
        "content": "CodeDock lets you write, run, and analyze code in multiple programming languages - all from your mobile device. Let's take a quick tour!",
        "action": None,
        "highlight_element": None,
        "next_step": TutorialStep.SELECT_LANGUAGE,
        "can_skip": True
    },
    TutorialStep.SELECT_LANGUAGE: {
        "order": 1,
        "title": "Choose Your Language",
        "description": "Select from 6+ executable languages",
        "content": "Tap the language selector at the top to choose a programming language. Python is selected by default - it's great for beginners!",
        "action": "tap_language_selector",
        "highlight_element": "language_selector",
        "next_step": TutorialStep.USE_TEMPLATES,
        "tips": [
            "Languages with green badges can be executed",
            "You can add custom languages later"
        ]
    },
    TutorialStep.USE_TEMPLATES: {
        "order": 2,
        "title": "Start with Templates",
        "description": "Use pre-written code to get started quickly",
        "content": "Templates are ready-made code examples. Tap 'Templates' to see what's available for your chosen language.",
        "action": "tap_templates",
        "highlight_element": "templates_button",
        "next_step": TutorialStep.WRITE_CODE,
        "tips": [
            "Templates show complexity levels",
            "Great for learning new concepts"
        ]
    },
    TutorialStep.WRITE_CODE: {
        "order": 3,
        "title": "Write Your Code",
        "description": "The code editor is your canvas",
        "content": "Type or paste your code in the editor. Line numbers help you navigate, and syntax highlighting makes code easier to read.",
        "action": None,
        "highlight_element": "code_editor",
        "next_step": TutorialStep.RUN_CODE,
        "tips": [
            "Code is auto-indented",
            "Supports copy/paste from clipboard"
        ]
    },
    TutorialStep.RUN_CODE: {
        "order": 4,
        "title": "Run Your Code",
        "description": "See your code come to life",
        "content": "Tap the green 'Run' button to execute your code. It runs in a secure sandbox - safe to experiment!",
        "action": "tap_run",
        "highlight_element": "run_button",
        "next_step": TutorialStep.VIEW_OUTPUT,
        "tips": [
            "Execution time is shown after running",
            "10 second timeout by default"
        ]
    },
    TutorialStep.VIEW_OUTPUT: {
        "order": 5,
        "title": "View Results",
        "description": "See output and errors",
        "content": "The output panel shows your program's results. Green means success, red indicates errors with helpful messages.",
        "action": None,
        "highlight_element": "output_panel",
        "next_step": TutorialStep.USE_AI,
        "tips": [
            "Tap the X to close output",
            "Output is scrollable for long results"
        ]
    },
    TutorialStep.USE_AI: {
        "order": 6,
        "title": "Meet Your AI Assistant",
        "description": "GPT-4o powered code help",
        "content": "The AI Assist button gives you intelligent help. Get explanations, find bugs, optimize code, and more!",
        "action": "tap_ai_assist",
        "highlight_element": "ai_assist_button",
        "next_step": TutorialStep.ANALYZE_CODE,
        "tips": [
            "9 different AI modes available",
            "Works with any language"
        ]
    },
    TutorialStep.ANALYZE_CODE: {
        "order": 7,
        "title": "Analyze Your Code",
        "description": "Get insights and metrics",
        "content": "The Analyze button shows code complexity, function count, and other metrics. Great for improving code quality!",
        "action": "tap_analyze",
        "highlight_element": "analyze_button",
        "next_step": TutorialStep.SAVE_FILE,
        "tips": [
            "Lower complexity is usually better",
            "Helps identify refactoring opportunities"
        ]
    },
    TutorialStep.SAVE_FILE: {
        "order": 8,
        "title": "Save Your Work",
        "description": "Never lose your code",
        "content": "Tap 'Save' to store your code in the cloud. Access your files from the 'Files' button anytime.",
        "action": "tap_save",
        "highlight_element": "save_button",
        "next_step": TutorialStep.ADVANCED_FEATURES,
        "tips": [
            "Files sync across devices",
            "Organize with favorites"
        ]
    },
    TutorialStep.ADVANCED_FEATURES: {
        "order": 9,
        "title": "Discover Advanced Features",
        "description": "Power user capabilities",
        "content": "There's more to explore! Triple-tap the version number in Settings to unlock the Advanced Panel with experimental features.",
        "action": None,
        "highlight_element": "settings_button",
        "next_step": TutorialStep.CUSTOM_LANGUAGES,
        "tips": [
            "Adjust execution timeouts",
            "Enable experimental features",
            "Custom security levels"
        ]
    },
    TutorialStep.CUSTOM_LANGUAGES: {
        "order": 10,
        "title": "Add Custom Languages",
        "description": "Expand your toolkit",
        "content": "The Language Dock lets you add support for more languages. Go to Settings > Language Addons to get started.",
        "action": None,
        "highlight_element": "addons_setting",
        "next_step": TutorialStep.COMPLETE,
        "tips": [
            "Community addons coming soon",
            "Create your own language configs"
        ]
    },
    TutorialStep.COMPLETE: {
        "order": 11,
        "title": "You're Ready!",
        "description": "Start coding with confidence",
        "content": "You've completed the tutorial! You now know all the essentials. Happy coding!",
        "action": None,
        "highlight_element": None,
        "next_step": None,
        "celebration": True
    }
}

#====================================================================================================
# HOTFIX SYSTEM
#====================================================================================================

HOTFIX_REGISTRY = {
    "HF-2026-001": {
        "id": "HF-2026-001",
        "priority": HotfixPriority.MEDIUM,
        "title": "WebView Preview on Web Platform",
        "description": "WebView component renders differently on web platform vs native",
        "status": "documented",
        "workaround": "Use native mobile app for HTML preview",
        "affected_versions": ["3.0.0", "4.0.0"],
        "fixed_in": None
    },
    "HF-2026-002": {
        "id": "HF-2026-002",
        "priority": HotfixPriority.LOW,
        "title": "Tunnel Connection Intermittent",
        "description": "Ngrok tunnel may timeout during high traffic",
        "status": "monitoring",
        "workaround": "Retry connection or use direct access",
        "affected_versions": ["*"],
        "fixed_in": None
    }
}

#====================================================================================================
# FEATURE FLAGS SYSTEM
#====================================================================================================

FEATURE_FLAGS = {
    FeatureFlag.TEACHING_MODE: {
        "enabled": True,
        "rollout_percentage": 100,
        "description": "Interactive tutorial system"
    },
    FeatureFlag.ADVANCED_PANEL: {
        "enabled": True,
        "rollout_percentage": 100,
        "description": "Hidden advanced settings panel",
        "access_method": "triple_tap_version"
    },
    FeatureFlag.AI_SUGGESTIONS: {
        "enabled": True,
        "rollout_percentage": 100,
        "description": "AI-powered code suggestions"
    },
    FeatureFlag.CUSTOM_LANGUAGES: {
        "enabled": True,
        "rollout_percentage": 100,
        "description": "Custom language addon support"
    },
    FeatureFlag.EXPANSION_DOCK: {
        "enabled": True,
        "rollout_percentage": 100,
        "description": "Language dock expansion system"
    },
    FeatureFlag.EXPERIMENTAL: {
        "enabled": False,
        "rollout_percentage": 0,
        "description": "Experimental features"
    },
    FeatureFlag.STREAMING_OUTPUT: {
        "enabled": False,
        "rollout_percentage": 0,
        "description": "Real-time streaming execution output"
    },
    FeatureFlag.COLLABORATIVE: {
        "enabled": False,
        "rollout_percentage": 0,
        "description": "Real-time collaborative editing"
    },
    FeatureFlag.CLOUD_SYNC: {
        "enabled": False,
        "rollout_percentage": 0,
        "description": "Cross-device cloud synchronization"
    }
}

#====================================================================================================
# ADVANCED CODE TEMPLATES - Comprehensive
#====================================================================================================

CODE_TEMPLATES = {
    LanguageType.PYTHON: {
        "hello_world": {
            "name": "Hello World",
            "code": 'print("Hello, World!")',
            "description": "Your first program",
            "complexity": CodeComplexity.TRIVIAL,
            "tags": ["beginner", "basics"]
        },
        "async_fetch": {
            "name": "Async Data Fetch",
            "code": '''import asyncio

async def fetch_data(url: str) -> dict:
    """Asynchronously fetch data from a URL."""
    print(f"Fetching: {url}")
    await asyncio.sleep(0.5)  # Simulated network delay
    return {"status": "success", "data": [1, 2, 3]}

async def main():
    urls = ["api/users", "api/posts", "api/comments"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for url, result in zip(urls, results):
        print(f"{url}: {result}")

asyncio.run(main())''',
            "description": "Modern async/await pattern for concurrent operations",
            "complexity": CodeComplexity.MODERATE,
            "tags": ["async", "networking", "concurrency"]
        },
        "dataclass_model": {
            "name": "Dataclass Model",
            "code": '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity with validation."""
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("Invalid email format")
    
    @property
    def display_name(self) -> str:
        return f"@{self.username}"

# Usage
user = User(1, "developer", "dev@example.com")
print(f"Created user: {user.display_name}")
print(f"Active: {user.is_active}")''',
            "description": "Modern Python dataclass with validation",
            "complexity": CodeComplexity.MODERATE,
            "tags": ["dataclass", "oop", "validation"]
        },
        "pattern_matching": {
            "name": "Pattern Matching",
            "code": '''def process_command(command: dict) -> str:
    """Process command using structural pattern matching (Python 3.10+)."""
    match command:
        case {"action": "create", "type": type_name, "data": data}:
            return f"Creating {type_name} with {len(data)} items"
        case {"action": "delete", "id": id_val} if isinstance(id_val, int):
            return f"Deleting item #{id_val}"
        case {"action": "update", "id": id_val, **rest}:
            return f"Updating #{id_val}: {rest}"
        case {"action": action}:
            return f"Unknown action: {action}"
        case _:
            return "Invalid command format"

# Test cases
commands = [
    {"action": "create", "type": "user", "data": [1, 2, 3]},
    {"action": "delete", "id": 42},
    {"action": "update", "id": 1, "name": "New Name"},
]

for cmd in commands:
    print(f"{cmd} -> {process_command(cmd)}")''',
            "description": "Python 3.10+ structural pattern matching",
            "complexity": CodeComplexity.MODERATE,
            "tags": ["pattern-matching", "python310", "advanced"]
        },
        "generator_pipeline": {
            "name": "Generator Pipeline",
            "code": '''from typing import Generator, Iterable
from functools import reduce

def read_data() -> Generator[int, None, None]:
    """Generate sample data stream."""
    for i in range(1, 11):
        yield i

def filter_even(data: Iterable[int]) -> Generator[int, None, None]:
    """Filter even numbers."""
    for x in data:
        if x % 2 == 0:
            yield x

def square(data: Iterable[int]) -> Generator[int, None, None]:
    """Square each number."""
    for x in data:
        yield x ** 2

def pipeline(*functions):
    """Compose functions into a pipeline."""
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

# Create and execute pipeline
process = pipeline(read_data, filter_even, square, list)
result = process(None)
print(f"Pipeline result: {result}")
print(f"Sum: {sum(result)}")''',
            "description": "Functional programming with generators",
            "complexity": CodeComplexity.COMPLEX,
            "tags": ["functional", "generators", "pipeline"]
        },
        "context_manager": {
            "name": "Context Manager",
            "code": '''from contextlib import contextmanager
from time import perf_counter
from typing import Generator

@contextmanager
def timer(operation: str) -> Generator[None, None, None]:
    """Context manager for timing operations."""
    start = perf_counter()
    print(f"[START] {operation}")
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"[END] {operation}: {elapsed:.4f}s")

@contextmanager  
def transaction(name: str) -> Generator[list, None, None]:
    """Simulated database transaction context."""
    operations = []
    print(f"BEGIN TRANSACTION: {name}")
    try:
        yield operations
        print(f"COMMIT: {len(operations)} operations")
    except Exception as e:
        print(f"ROLLBACK: {e}")
        raise

# Usage
with timer("Data Processing"):
    with transaction("user_update") as ops:
        ops.append("UPDATE users SET active = true")
        ops.append("INSERT INTO audit_log VALUES (...)")
        print(f"Queued {len(ops)} operations")''',
            "description": "Custom context managers for resource management",
            "complexity": CodeComplexity.MODERATE,
            "tags": ["context-manager", "resources", "patterns"]
        },
        "decorator_factory": {
            "name": "Decorator Factory",
            "code": '''from functools import wraps
from time import perf_counter
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator factory for retry logic."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
            raise last_exception
        return wrapper
    return decorator

def measure_time(func: Callable) -> Callable:
    """Decorator to measure execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@measure_time
@retry(max_attempts=3)
def unstable_operation():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success!"

# Test (may succeed or fail randomly)
try:
    result = unstable_operation()
    print(f"Result: {result}")
except Exception as e:
    print(f"All attempts failed: {e}")''',
            "description": "Advanced decorator patterns with factories",
            "complexity": CodeComplexity.COMPLEX,
            "tags": ["decorators", "metaprogramming", "patterns"]
        }
    },
    LanguageType.JAVASCRIPT: {
        "hello_world": {
            "name": "Hello World",
            "code": 'console.log("Hello, World!");',
            "description": "Your first JavaScript program",
            "complexity": CodeComplexity.TRIVIAL
        },
        "async_iterator": {
            "name": "Async Iterator",
            "code": '''// Modern Async Iterator with AbortController
async function* fetchPaginated(baseUrl, options = {}) {
    let page = 1;
    let hasMore = true;
    
    try {
        while (hasMore) {
            console.log(\`Fetching page \${page}...\`);
            await new Promise(r => setTimeout(r, 100));
            const data = Array.from({length: 5}, (_, i) => ({
                id: (page - 1) * 5 + i + 1,
                value: Math.random().toFixed(2)
            }));
            
            yield { page, data, timestamp: Date.now() };
            hasMore = page < 3;
            page++;
        }
    } finally {
        console.log('Iterator cleanup complete');
    }
}

// Consume
async function processData() {
    const results = [];
    for await (const { page, data } of fetchPaginated('/api')) {
        console.log(\`Page \${page}: \${data.length} items\`);
        results.push(...data);
    }
    console.log(\`Total: \${results.length} items\`);
}

processData();''',
            "description": "Async generators for paginated data",
            "complexity": CodeComplexity.COMPLEX
        },
        "proxy_reactive": {
            "name": "Reactive State",
            "code": '''// Reactive State Management using Proxy
function createReactive(target, onChange) {
    return new Proxy(target, {
        get(obj, prop) {
            const value = obj[prop];
            if (typeof value === 'object' && value !== null) {
                return createReactive(value, onChange);
            }
            return value;
        },
        set(obj, prop, value) {
            const oldValue = obj[prop];
            obj[prop] = value;
            onChange(prop, value, oldValue);
            return true;
        }
    });
}

const state = createReactive(
    { user: { name: 'Dev', level: 1 }, items: [] },
    (prop, newVal, oldVal) => {
        console.log(\`Changed: \${prop} = \${JSON.stringify(newVal)}\`);
    }
);

state.user.name = 'Advanced Dev';
state.user.level = 5;
state.items.push({ id: 1 });
console.log('Final:', JSON.stringify(state, null, 2));''',
            "description": "Vue-style reactivity with Proxy",
            "complexity": CodeComplexity.COMPLEX
        },
        "promise_pool": {
            "name": "Promise Pool",
            "code": '''// Concurrent Promise Pool with Rate Limiting
class PromisePool {
    constructor(concurrency = 3) {
        this.concurrency = concurrency;
        this.running = 0;
        this.queue = [];
    }
    
    async add(taskFn) {
        if (this.running >= this.concurrency) {
            await new Promise(resolve => this.queue.push(resolve));
        }
        this.running++;
        try {
            return await taskFn();
        } finally {
            this.running--;
            if (this.queue.length > 0) this.queue.shift()();
        }
    }
    
    async map(items, asyncFn) {
        return Promise.all(items.map(item => this.add(() => asyncFn(item))));
    }
}

const simulateTask = async (id) => {
    const duration = Math.random() * 300 + 100;
    console.log(\`Task \${id} started\`);
    await new Promise(r => setTimeout(r, duration));
    console.log(\`Task \${id} done\`);
    return { id, duration };
};

const pool = new PromisePool(3);
pool.map([1,2,3,4,5,6], simulateTask).then(r => {
    console.log(\`All done: \${r.length} tasks\`);
});''',
            "description": "Concurrent task execution with limit",
            "complexity": CodeComplexity.COMPLEX
        }
    },
    LanguageType.CPP: {
        "hello_world": {
            "name": "Hello World",
            "code": '''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}''',
            "description": "Your first C++ program",
            "complexity": CodeComplexity.TRIVIAL
        },
        "smart_pointers": {
            "name": "Smart Pointers",
            "code": '''#include <iostream>
#include <memory>
#include <vector>
#include <string>

class Resource {
    std::string name;
public:
    Resource(const std::string& n) : name(n) {
        std::cout << "Resource '" << name << "' created\\n";
    }
    ~Resource() {
        std::cout << "Resource '" << name << "' destroyed\\n";
    }
    void use() const { std::cout << "Using: " << name << "\\n"; }
};

int main() {
    // unique_ptr - exclusive ownership
    {
        auto unique = std::make_unique<Resource>("Unique");
        unique->use();
    }
    
    std::cout << "---\\n";
    
    // shared_ptr - shared ownership
    {
        auto shared1 = std::make_shared<Resource>("Shared");
        {
            auto shared2 = shared1;
            std::cout << "Ref count: " << shared1.use_count() << "\\n";
        }
        std::cout << "Ref count: " << shared1.use_count() << "\\n";
    }
    
    std::cout << "Program end\\n";
    return 0;
}''',
            "description": "Modern C++ memory management",
            "complexity": CodeComplexity.MODERATE
        },
        "concepts_templates": {
            "name": "Concepts (C++20)",
            "code": '''#include <iostream>
#include <concepts>
#include <vector>

template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T sum(const std::vector<T>& values) {
    T result{};
    for (const auto& v : values) result += v;
    return result;
}

template<typename T>
auto process(T value) {
    if constexpr (std::integral<T>) return value * 2;
    else if constexpr (std::floating_point<T>) return value * 1.5;
    else return value;
}

int main() {
    std::vector<int> ints = {1, 2, 3, 4, 5};
    std::vector<double> doubles = {1.1, 2.2, 3.3};
    
    std::cout << "Sum ints: " << sum(ints) << "\\n";
    std::cout << "Sum doubles: " << sum(doubles) << "\\n";
    std::cout << "Process 10: " << process(10) << "\\n";
    std::cout << "Process 10.0: " << process(10.0) << "\\n";
    
    return 0;
}''',
            "description": "C++20 concepts for type constraints",
            "complexity": CodeComplexity.COMPLEX
        }
    },
    LanguageType.HTML: {
        "hello_world": {
            "name": "Hello World",
            "code": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>''',
            "description": "Basic HTML page",
            "complexity": CodeComplexity.TRIVIAL
        },
        "modern_layout": {
            "name": "Modern Layout",
            "code": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Layout</title>
    <style>
        :root { --primary: #6366f1; --surface: #1e1b4b; --text: #e0e7ff; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63);
            min-height: 100vh; color: var(--text);
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem; padding: 2rem; max-width: 1200px; margin: 0 auto;
        }
        .card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 1rem; padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }
        .card:hover { transform: translateY(-5px); }
        .card h2 { color: var(--primary); margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card"><h2>Feature One</h2><p>Glassmorphism design</p></div>
        <div class="card"><h2>Feature Two</h2><p>Responsive grid</p></div>
        <div class="card"><h2>Feature Three</h2><p>CSS custom properties</p></div>
    </div>
</body>
</html>''',
            "description": "Glassmorphism UI with CSS Grid",
            "complexity": CodeComplexity.MODERATE
        },
        "web_component": {
            "name": "Web Component",
            "code": '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Web Component</title>
    <style>body { font-family: system-ui; background: #1a1a2e; padding: 2rem; color: #eee; }</style>
</head>
<body>
    <h1>Custom Counter</h1>
    <my-counter initial="5"></my-counter>
    
    <script>
        class MyCounter extends HTMLElement {
            constructor() {
                super();
                this.attachShadow({ mode: 'open' });
                this.count = parseInt(this.getAttribute('initial') || '0');
            }
            connectedCallback() { this.render(); }
            render() {
                this.shadowRoot.innerHTML = \`
                    <style>
                        .counter { background: linear-gradient(135deg, #667eea, #764ba2);
                            padding: 1.5rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; }
                        button { width: 40px; height: 40px; border-radius: 50%; border: none;
                            background: rgba(255,255,255,0.2); color: white; font-size: 1.5rem; cursor: pointer; }
                        span { font-size: 2rem; font-weight: bold; color: white; min-width: 60px; text-align: center; }
                    </style>
                    <div class="counter">
                        <button id="dec">-</button>
                        <span id="val">\${this.count}</span>
                        <button id="inc">+</button>
                    </div>\`;
                this.shadowRoot.getElementById('inc').onclick = () => { this.count++; this.update(); };
                this.shadowRoot.getElementById('dec').onclick = () => { this.count--; this.update(); };
            }
            update() { this.shadowRoot.getElementById('val').textContent = this.count; }
        }
        customElements.define('my-counter', MyCounter);
    </script>
</body>
</html>''',
            "description": "Custom element with Shadow DOM",
            "complexity": CodeComplexity.COMPLEX
        }
    }
}

#====================================================================================================
# PYDANTIC MODELS
#====================================================================================================

class ExecutionMetrics(BaseModel):
    execution_time_ms: float = 0
    memory_peak_kb: Optional[float] = None
    cpu_time_ms: Optional[float] = None
    lines_executed: Optional[int] = None

class SecurityReport(BaseModel):
    risk_level: str = "low"
    issues_found: List[Dict[str, Any]] = []
    blocked_operations: List[str] = []
    recommendations: List[str] = []

class CodeAnalysis(BaseModel):
    complexity: CodeComplexity = CodeComplexity.TRIVIAL
    cyclomatic_complexity: int = 1
    lines_of_code: int = 0
    functions_count: int = 0
    classes_count: int = 0
    imports_count: int = 0
    comments_ratio: float = 0.0
    issues: List[Dict[str, Any]] = []
    suggestions: List[str] = []

class ExecutionResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ExecutionStatus = ExecutionStatus.PENDING
    output: str = ""
    error: str = ""
    metrics: ExecutionMetrics = Field(default_factory=ExecutionMetrics)
    security: Optional[SecurityReport] = None
    analysis: Optional[CodeAnalysis] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])

class CodeExecutionRequest(BaseModel):
    code: str
    language: LanguageType
    input_data: Optional[str] = None
    timeout_seconds: int = Field(default=10, ge=1, le=60)
    memory_limit_mb: int = Field(default=256, ge=64, le=1024)
    security_level: SecurityLevel = SecurityLevel.STANDARD
    include_analysis: bool = False

class CodeExecutionResponse(BaseModel):
    execution_id: str
    result: ExecutionResult
    language_info: Dict[str, Any]

class AIAssistRequest(BaseModel):
    code: str
    language: LanguageType
    mode: AIAssistantMode
    context: Optional[str] = None
    target_language: Optional[LanguageType] = None

class AIAssistResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    mode: AIAssistantMode
    suggestion: str
    explanation: Optional[str] = None
    code_blocks: List[Dict[str, str]] = []
    confidence: float = 0.0
    model: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CodeFile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    language: LanguageType
    code: str
    version: int = 1
    checksum: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_favorite: bool = False
    tags: List[str] = []

class UserPreferences(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    theme: str = "dark"
    font_size: int = 14
    tab_size: int = 4
    auto_save: bool = True
    show_line_numbers: bool = True
    word_wrap: bool = True
    default_language: LanguageType = LanguageType.PYTHON
    ai_suggestions: bool = True
    teaching_mode_completed: bool = False
    current_tutorial_step: Optional[str] = None
    tooltips_enabled: bool = True
    advanced_panel_unlocked: bool = False
    advanced_settings: Dict[str, Any] = {}
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LanguageAddon(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    language_key: str
    name: str
    extension: str
    icon: str = "code-slash"
    color: str = "#6B7280"
    description: str = ""
    executable: bool = False
    version: str = "1.0"
    syntax_config: Optional[Dict[str, Any]] = None
    dock_config: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TutorialProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_step: TutorialStep = TutorialStep.WELCOME
    completed_steps: List[str] = []
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    skipped: bool = False

class AdvancedSettings(BaseModel):
    execution_timeout: int = 10
    memory_limit_mb: int = 256
    security_level: SecurityLevel = SecurityLevel.STANDARD
    debug_mode: bool = False
    experimental_features: bool = False
    streaming_output: bool = False
    custom_compiler_flags: Dict[str, List[str]] = {}

#====================================================================================================
# CODE EXECUTORS
#====================================================================================================

class CodeAnalyzer:
    @staticmethod
    def analyze_python(code: str) -> CodeAnalysis:
        analysis = CodeAnalysis()
        try:
            tree = ast.parse(code)
            analysis.lines_of_code = len(code.splitlines())
            analysis.functions_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
            analysis.classes_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
            analysis.imports_count = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)))
            
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            
            analysis.cyclomatic_complexity = complexity
            
            if complexity <= 5: analysis.complexity = CodeComplexity.TRIVIAL
            elif complexity <= 10: analysis.complexity = CodeComplexity.SIMPLE
            elif complexity <= 20: analysis.complexity = CodeComplexity.MODERATE
            elif complexity <= 50: analysis.complexity = CodeComplexity.COMPLEX
            else: analysis.complexity = CodeComplexity.VERY_COMPLEX
                
        except SyntaxError as e:
            analysis.issues.append({"type": "syntax_error", "line": e.lineno, "message": str(e.msg)})
        except Exception as e:
            analysis.issues.append({"type": "analysis_error", "message": str(e)})
        return analysis

class ExecutionContext:
    def __init__(self, request: CodeExecutionRequest):
        self.request = request
        self.start_time = None
        self.end_time = None
        self.trace_id = uuid.uuid4().hex[:16]
        
    def start(self): self.start_time = time.perf_counter()
    def end(self): self.end_time = time.perf_counter()
    
    @property
    def elapsed_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0

class CodeExecutor(ABC):
    def __init__(self):
        self.execution_count = 0
        self.total_time_ms = 0
        
    @abstractmethod
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult: pass
    
    @abstractmethod
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]: pass
    
    def sanitize_output(self, output: str, max_length: int = 50000) -> str:
        if len(output) > max_length:
            half = max_length // 2
            return f"{output[:half]}\n\n... [Truncated] ...\n\n{output[-half:]}"
        return output

class PythonExecutor(CodeExecutor):
    FORBIDDEN = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'pickle', 'ctypes', 'importlib'}
    
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        is_valid, error_msg, security = self.validate(ctx.request.code, ctx.request.security_level)
        result.security = security
        
        if not is_valid:
            result.status = ExecutionStatus.SECURITY_VIOLATION
            result.error = error_msg
            ctx.end()
            return result
        
        if ctx.request.include_analysis:
            result.analysis = CodeAnalyzer.analyze_python(ctx.request.code)
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(ctx.request.code)
                temp_file = f.name
            
            try:
                process = await asyncio.create_subprocess_exec(
                    sys.executable, '-u', temp_file,
                    stdin=asyncio.subprocess.PIPE if ctx.request.input_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=ctx.request.input_data.encode() if ctx.request.input_data else None),
                    timeout=ctx.request.timeout_seconds
                )
                
                result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
                result.error = stderr.decode('utf-8', errors='replace')
                result.status = ExecutionStatus.SUCCESS if process.returncode == 0 else ExecutionStatus.ERROR
                    
            except asyncio.TimeoutError:
                process.kill()
                result.status = ExecutionStatus.TIMEOUT
                result.error = f"Timeout after {ctx.request.timeout_seconds}s"
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = str(e)
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        report = SecurityReport()
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        
        for module in self.FORBIDDEN:
            if f'import {module}' in code or f'from {module}' in code:
                report.risk_level = "high"
                report.blocked_operations.append(f"import:{module}")
                return False, f"Forbidden module: {module}", report
        return True, "", report

class JavaScriptExecutor(CodeExecutor):
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        wrapped_code = f'''
(function() {{
    const __output = [];
    console.log = (...args) => __output.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    try {{
        {ctx.request.code}
        return {{ status: 'success', output: __output.join('\\n') }};
    }} catch(e) {{ return {{ status: 'error', error: e.message }}; }}
}})()'''
        
        result.status = ExecutionStatus.SUCCESS
        result.output = wrapped_code
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        return True, "", SecurityReport()

class CppExecutor(CodeExecutor):
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        is_valid, error_msg, security = self.validate(ctx.request.code, ctx.request.security_level)
        if not is_valid:
            result.status = ExecutionStatus.SECURITY_VIOLATION
            result.error = error_msg
            result.security = security
            ctx.end()
            return result
        
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            source_file = os.path.join(temp_dir, 'main.cpp')
            output_file = os.path.join(temp_dir, 'main')
            
            with open(source_file, 'w') as f:
                f.write(ctx.request.code)
            
            compile_process = await asyncio.create_subprocess_exec(
                'g++', '-std=c++20', '-O2', '-Wall', '-o', output_file, source_file,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            
            compile_stdout, compile_stderr = await asyncio.wait_for(compile_process.communicate(), timeout=30)
            
            if compile_process.returncode != 0:
                result.status = ExecutionStatus.COMPILATION_ERROR
                result.error = f"Compilation failed:\n{compile_stderr.decode()}"
                ctx.end()
                return result
            
            run_process = await asyncio.create_subprocess_exec(
                output_file,
                stdin=asyncio.subprocess.PIPE if ctx.request.input_data else None,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                run_process.communicate(input=ctx.request.input_data.encode() if ctx.request.input_data else None),
                timeout=ctx.request.timeout_seconds
            )
            
            result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
            result.error = stderr.decode('utf-8', errors='replace')
            result.status = ExecutionStatus.SUCCESS if run_process.returncode == 0 else ExecutionStatus.RUNTIME_ERROR
            
        except asyncio.TimeoutError:
            result.status = ExecutionStatus.TIMEOUT
            result.error = f"Timeout after {ctx.request.timeout_seconds}s"
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = str(e)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        report = SecurityReport()
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        dangerous = ['system(', 'popen(', 'fork(', 'exec']
        for d in dangerous:
            if d in code:
                return False, f"Blocked: {d}", report
        return True, "", report

class CExecutor(CppExecutor):
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        # Similar to C++ but with gcc
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            source_file = os.path.join(temp_dir, 'main.c')
            output_file = os.path.join(temp_dir, 'main')
            
            with open(source_file, 'w') as f:
                f.write(ctx.request.code)
            
            compile_process = await asyncio.create_subprocess_exec(
                'gcc', '-std=c17', '-O2', '-Wall', '-o', output_file, source_file,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            
            await asyncio.wait_for(compile_process.communicate(), timeout=30)
            
            if compile_process.returncode != 0:
                result.status = ExecutionStatus.COMPILATION_ERROR
                ctx.end()
                return result
            
            run_process = await asyncio.create_subprocess_exec(
                output_file, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(run_process.communicate(), timeout=ctx.request.timeout_seconds)
            result.output = stdout.decode()
            result.status = ExecutionStatus.SUCCESS if run_process.returncode == 0 else ExecutionStatus.ERROR
            
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = str(e)
        finally:
            if temp_dir: shutil.rmtree(temp_dir, ignore_errors=True)
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        return result

class HTMLExecutor(CodeExecutor):
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        result = ExecutionResult()
        result.status = ExecutionStatus.SUCCESS
        result.output = ctx.request.code
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        return True, "", SecurityReport()

class TypeScriptExecutor(JavaScriptExecutor):
    pass

# Executor Factory
class ExecutorFactory:
    _executors = {
        LanguageType.PYTHON: PythonExecutor(),
        LanguageType.JAVASCRIPT: JavaScriptExecutor(),
        LanguageType.TYPESCRIPT: TypeScriptExecutor(),
        LanguageType.CPP: CppExecutor(),
        LanguageType.C: CExecutor(),
        LanguageType.HTML: HTMLExecutor(),
    }
    
    @classmethod
    def get_executor(cls, language: LanguageType):
        return cls._executors.get(language)
    
    @classmethod
    def is_executable(cls, language: LanguageType) -> bool:
        return language in cls._executors

#====================================================================================================
# AI SERVICE
#====================================================================================================

class AIAssistantService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.model = "gpt-4o"
        
    async def assist(self, request: AIAssistRequest) -> AIAssistResponse:
        if not self.api_key:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        prompts = {
            AIAssistantMode.EXPLAIN: "You are a code explanation expert. Explain the code clearly and thoroughly.",
            AIAssistantMode.DEBUG: "You are a debugging expert. Find bugs and suggest fixes.",
            AIAssistantMode.OPTIMIZE: "You are an optimization specialist. Suggest performance improvements.",
            AIAssistantMode.COMPLETE: "You are a code completion assistant. Complete the partial code.",
            AIAssistantMode.REFACTOR: "You are a refactoring expert. Improve code structure.",
            AIAssistantMode.DOCUMENT: "You are a documentation specialist. Generate comprehensive docs.",
            AIAssistantMode.TEST_GEN: "You are a test generation expert. Create unit tests.",
            AIAssistantMode.SECURITY_AUDIT: "You are a security auditor. Find vulnerabilities.",
            AIAssistantMode.CONVERT: f"Convert the code to {request.target_language or 'another language'}.",
            AIAssistantMode.TEACH: "You are a programming teacher. Explain concepts for beginners.",
            AIAssistantMode.REVIEW: "You are a code reviewer. Provide constructive feedback.",
            AIAssistantMode.ARCHITECTURE: "You are a software architect. Suggest architectural improvements.",
        }
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"codedock-{uuid.uuid4().hex[:8]}",
                system_message=prompts.get(request.mode, prompts[AIAssistantMode.EXPLAIN])
            ).with_model("openai", self.model)
            
            response = await chat.send_message(UserMessage(text=f"Language: {request.language.value}\n\nCode:\n```\n{request.code}\n```"))
            
            code_blocks = []
            for match in re.findall(r'```(\w+)?\n(.*?)```', response, re.DOTALL):
                code_blocks.append({"language": match[0] or request.language.value, "code": match[1].strip()})
            
            return AIAssistResponse(mode=request.mode, suggestion=response, code_blocks=code_blocks, confidence=0.85, model=self.model)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

#====================================================================================================
# APP LIFECYCLE
#====================================================================================================

executor_factory = ExecutorFactory()
ai_service = AIAssistantService()
app_start_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 80)
    logger.info(f"CodeDock Quantum Nexus v{SYSTEM_VERSION} ({SYSTEM_CODENAME}) Starting...")
    logger.info("=" * 80)
    
    await db.code_files.create_index("id", unique=True)
    await db.execution_history.create_index("created_at")
    await db.language_addons.create_index("language_key", unique=True)
    await db.tutorial_progress.create_index("id", unique=True)
    
    yield
    
    logger.info("Shutting down...")
    client.close()

app = FastAPI(
    title="CodeDock Quantum Nexus",
    description="Beyond Bleeding-Edge Multi-Language Compiler Platform",
    version=SYSTEM_VERSION,
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

api_router = APIRouter(prefix="/api")

#====================================================================================================
# API ROUTES
#====================================================================================================

@api_router.get("/")
async def root():
    return {
        "name": "CodeDock Quantum Nexus",
        "version": SYSTEM_VERSION,
        "codename": SYSTEM_CODENAME,
        "build": SYSTEM_BUILD,
        "features": SYSTEM_FEATURES,
        "api_version": "v4"
    }

@api_router.get("/health")
async def health():
    return {
        "status": "healthy",
        "uptime_seconds": time.time() - app_start_time,
        "ai_available": bool(ai_service.api_key),
        "features_enabled": [f.value for f, cfg in FEATURE_FLAGS.items() if cfg["enabled"]]
    }

@api_router.get("/system/info")
async def system_info():
    return {
        "version": SYSTEM_VERSION,
        "codename": SYSTEM_CODENAME,
        "build": SYSTEM_BUILD,
        "features": SYSTEM_FEATURES,
        "feature_flags": {k.value: v for k, v in FEATURE_FLAGS.items()},
        "hotfixes": list(HOTFIX_REGISTRY.keys()),
        "languages_installed": sum(1 for l in LANGUAGE_DOCK_REGISTRY.values() if l.get("status") == DockStatus.INSTALLED),
        "languages_available": len(LANGUAGE_DOCK_REGISTRY)
    }

# Languages & Dock System
@api_router.get("/languages")
async def get_languages():
    languages = []
    for lang_type, config in LANGUAGE_DOCK_REGISTRY.items():
        languages.append({
            "key": lang_type.value,
            "type": "builtin",
            **{k: v for k, v in config.items() if k not in ['dock_config', 'syntax', 'expansion_hooks']},
            "executable": executor_factory.is_executable(lang_type),
            "templates_available": lang_type in CODE_TEMPLATES
        })
    
    addons = await db.language_addons.find().to_list(100)
    for addon in addons:
        addon['_id'] = str(addon['_id'])
        addon['type'] = 'addon'
        languages.append(addon)
    
    return {"languages": languages, "count": len(languages)}

@api_router.get("/languages/{language_key}")
async def get_language(language_key: str):
    try:
        lang_type = LanguageType(language_key)
        if lang_type in LANGUAGE_DOCK_REGISTRY:
            config = LANGUAGE_DOCK_REGISTRY[lang_type]
            templates = CODE_TEMPLATES.get(lang_type, {})
            return {
                "key": lang_type.value,
                **config,
                "executable": executor_factory.is_executable(lang_type),
                "templates": [{"key": k, **v} for k, v in templates.items()]
            }
    except ValueError:
        pass
    
    addon = await db.language_addons.find_one({"language_key": language_key})
    if addon:
        addon['_id'] = str(addon['_id'])
        return addon
    
    raise HTTPException(status_code=404, detail="Language not found")

@api_router.get("/dock/available")
async def get_available_docks():
    """Get all available language docks for expansion"""
    docks = []
    for lang_type, config in LANGUAGE_DOCK_REGISTRY.items():
        docks.append({
            "key": lang_type.value,
            "name": config.get("name", lang_type.value),
            "display_name": config.get("display_name", config.get("name")),
            "tier": config.get("tier", 3),
            "status": config.get("status", DockStatus.COMING_SOON).value if isinstance(config.get("status"), DockStatus) else config.get("status", "coming_soon"),
            "color": config.get("color", "#6B7280"),
            "icon": config.get("icon", "code-slash"),
            "description": config.get("description", ""),
            "expansion_ready": config.get("expansion_ready", False),
            "executable": executor_factory.is_executable(lang_type)
        })
    return {"docks": sorted(docks, key=lambda x: (x["tier"], x["name"])), "total": len(docks)}

# Execution
@api_router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    executor = executor_factory.get_executor(request.language)
    if not executor:
        raise HTTPException(status_code=400, detail=f"Language '{request.language.value}' not executable")
    
    ctx = ExecutionContext(request)
    result = await executor.execute(ctx)
    
    return CodeExecutionResponse(
        execution_id=result.id,
        result=result,
        language_info=LANGUAGE_DOCK_REGISTRY.get(request.language, {})
    )

@api_router.post("/analyze")
async def analyze_code(request: CodeExecutionRequest):
    analysis = None
    if request.language == LanguageType.PYTHON:
        analysis = CodeAnalyzer.analyze_python(request.code)
    else:
        analysis = CodeAnalysis(lines_of_code=len(request.code.splitlines()))
    return {"language": request.language.value, "analysis": analysis.dict()}

@api_router.post("/validate")
async def validate_code(request: CodeExecutionRequest):
    executor = executor_factory.get_executor(request.language)
    if not executor:
        return {"valid": True, "message": "No validation available"}
    
    is_valid, error_msg, security = executor.validate(request.code, request.security_level)
    return {"valid": is_valid, "message": error_msg or "Valid", "security": security.dict()}

# AI
@api_router.get("/ai/modes")
async def get_ai_modes():
    modes = [
        {"key": m.value, "name": m.value.replace("_", " ").title(), "description": d}
        for m, d in [
            (AIAssistantMode.EXPLAIN, "Get detailed code explanation"),
            (AIAssistantMode.DEBUG, "Find and fix bugs"),
            (AIAssistantMode.OPTIMIZE, "Improve performance"),
            (AIAssistantMode.COMPLETE, "Auto-complete code"),
            (AIAssistantMode.REFACTOR, "Improve structure"),
            (AIAssistantMode.DOCUMENT, "Generate documentation"),
            (AIAssistantMode.TEST_GEN, "Generate unit tests"),
            (AIAssistantMode.SECURITY_AUDIT, "Security analysis"),
            (AIAssistantMode.CONVERT, "Convert to another language"),
            (AIAssistantMode.TEACH, "Explain for beginners"),
            (AIAssistantMode.REVIEW, "Code review feedback"),
            (AIAssistantMode.ARCHITECTURE, "Architecture suggestions"),
        ]
    ]
    return {"modes": modes, "ai_available": bool(ai_service.api_key)}

@api_router.post("/ai/assist", response_model=AIAssistResponse)
async def ai_assist(request: AIAssistRequest):
    return await ai_service.assist(request)

# Templates
@api_router.get("/templates")
async def get_templates():
    templates = {}
    for lang_type, lang_templates in CODE_TEMPLATES.items():
        templates[lang_type.value] = [{"key": k, **v} for k, v in lang_templates.items()]
    return {"templates": templates}

@api_router.get("/templates/{language}")
async def get_language_templates(language: str):
    try:
        lang_type = LanguageType(language)
        if lang_type in CODE_TEMPLATES:
            return {"language": language, "templates": [{"key": k, **v} for k, v in CODE_TEMPLATES[lang_type].items()]}
    except ValueError:
        pass
    raise HTTPException(status_code=404, detail="No templates")

# Tooltips System
@api_router.get("/tooltips")
async def get_tooltips(category: Optional[str] = None):
    tooltips = TOOLTIPS_REGISTRY
    if category:
        tooltips = {k: v for k, v in tooltips.items() if v.get("category", "").value == category}
    return {"tooltips": tooltips, "categories": [c.value for c in TooltipCategory]}

@api_router.get("/tooltips/{tooltip_id}")
async def get_tooltip(tooltip_id: str):
    if tooltip_id in TOOLTIPS_REGISTRY:
        return TOOLTIPS_REGISTRY[tooltip_id]
    raise HTTPException(status_code=404, detail="Tooltip not found")

# Tutorial/Teaching Mode
@api_router.get("/tutorial/steps")
async def get_tutorial_steps():
    steps = []
    for step, config in TUTORIAL_STEPS.items():
        steps.append({"key": step.value, **config})
    return {"steps": sorted(steps, key=lambda x: x["order"]), "total_steps": len(steps)}

@api_router.get("/tutorial/step/{step_key}")
async def get_tutorial_step(step_key: str):
    try:
        step = TutorialStep(step_key)
        if step in TUTORIAL_STEPS:
            return {"key": step.value, **TUTORIAL_STEPS[step]}
    except ValueError:
        pass
    raise HTTPException(status_code=404, detail="Step not found")

@api_router.get("/tutorial/progress")
async def get_tutorial_progress():
    progress = await db.tutorial_progress.find_one({})
    if not progress:
        default = TutorialProgress()
        await db.tutorial_progress.insert_one(default.dict())
        return default
    return TutorialProgress(**progress)

@api_router.put("/tutorial/progress")
async def update_tutorial_progress(data: dict):
    await db.tutorial_progress.update_one({}, {"$set": data}, upsert=True)
    progress = await db.tutorial_progress.find_one({})
    return TutorialProgress(**progress)

@api_router.post("/tutorial/complete-step")
async def complete_tutorial_step(data: dict):
    step_key = data.get("step")
    progress = await db.tutorial_progress.find_one({})
    
    if not progress:
        progress = TutorialProgress().dict()
    
    completed = progress.get("completed_steps", [])
    if step_key not in completed:
        completed.append(step_key)
    
    # Find next step
    try:
        current = TutorialStep(step_key)
        next_step = TUTORIAL_STEPS.get(current, {}).get("next_step")
        
        update = {
            "completed_steps": completed,
            "current_step": next_step.value if next_step else "complete"
        }
        
        if next_step is None:
            update["completed_at"] = datetime.utcnow()
        
        await db.tutorial_progress.update_one({}, {"$set": update}, upsert=True)
    except ValueError:
        pass
    
    return {"success": True, "completed_steps": completed}

# Advanced Settings (Hidden Panel)
@api_router.get("/advanced/settings")
async def get_advanced_settings():
    prefs = await db.user_preferences.find_one({})
    if prefs and prefs.get("advanced_panel_unlocked"):
        return {
            "unlocked": True,
            "settings": prefs.get("advanced_settings", AdvancedSettings().dict()),
            "feature_flags": {k.value: v for k, v in FEATURE_FLAGS.items()}
        }
    return {"unlocked": False, "message": "Triple-tap version to unlock"}

@api_router.post("/advanced/unlock")
async def unlock_advanced_panel(data: dict):
    """Unlock with triple-tap gesture verification"""
    secret = data.get("secret")
    # Simple validation - in production would be more secure
    if secret == "quantum_nexus_unlock" or data.get("gesture") == "triple_tap_version":
        await db.user_preferences.update_one({}, {"$set": {"advanced_panel_unlocked": True}}, upsert=True)
        return {"success": True, "message": "Advanced panel unlocked!"}
    return {"success": False, "message": "Invalid unlock gesture"}

@api_router.put("/advanced/settings")
async def update_advanced_settings(settings: dict):
    await db.user_preferences.update_one({}, {"$set": {"advanced_settings": settings}}, upsert=True)
    return {"success": True}

# Hotfixes
@api_router.get("/hotfixes")
async def get_hotfixes():
    return {"hotfixes": list(HOTFIX_REGISTRY.values()), "count": len(HOTFIX_REGISTRY)}

@api_router.get("/hotfixes/{hotfix_id}")
async def get_hotfix(hotfix_id: str):
    if hotfix_id in HOTFIX_REGISTRY:
        return HOTFIX_REGISTRY[hotfix_id]
    raise HTTPException(status_code=404, detail="Hotfix not found")

# Files CRUD
@api_router.post("/files", response_model=CodeFile)
async def create_file(data: dict):
    code_file = CodeFile(**data)
    await db.code_files.insert_one(code_file.dict())
    return code_file

@api_router.get("/files")
async def get_files(language: Optional[str] = None, limit: int = 50):
    query = {"language": language} if language else {}
    files = await db.code_files.find(query).sort("updated_at", -1).to_list(limit)
    return {"files": [CodeFile(**f) for f in files]}

@api_router.get("/files/{file_id}")
async def get_file(file_id: str):
    file = await db.code_files.find_one({"id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return CodeFile(**file)

@api_router.put("/files/{file_id}")
async def update_file(file_id: str, data: dict):
    data["updated_at"] = datetime.utcnow()
    await db.code_files.update_one({"id": file_id}, {"$set": data})
    file = await db.code_files.find_one({"id": file_id})
    return CodeFile(**file)

@api_router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    await db.code_files.delete_one({"id": file_id})
    return {"success": True}

# Addons
@api_router.post("/addons", response_model=LanguageAddon)
async def create_addon(data: dict):
    existing = await db.language_addons.find_one({"language_key": data.get("language_key")})
    if existing:
        raise HTTPException(status_code=400, detail="Addon exists")
    addon = LanguageAddon(**data)
    await db.language_addons.insert_one(addon.dict())
    return addon

@api_router.get("/addons")
async def get_addons():
    addons = await db.language_addons.find().to_list(100)
    return {"addons": [LanguageAddon(**a) for a in addons]}

@api_router.delete("/addons/{addon_id}")
async def delete_addon(addon_id: str):
    await db.language_addons.delete_one({"id": addon_id})
    return {"success": True}

# Preferences
@api_router.get("/preferences")
async def get_preferences():
    prefs = await db.user_preferences.find_one({})
    if not prefs:
        default = UserPreferences()
        await db.user_preferences.insert_one(default.dict())
        return default
    return UserPreferences(**prefs)

@api_router.put("/preferences")
async def update_preferences(data: dict):
    data["updated_at"] = datetime.utcnow()
    await db.user_preferences.update_one({}, {"$set": data}, upsert=True)
    prefs = await db.user_preferences.find_one({})
    return UserPreferences(**prefs)

# Snippets
@api_router.post("/snippets")
async def create_snippet(data: dict):
    snippet_id = uuid.uuid4().hex[:8]
    snippet = {
        "id": snippet_id,
        "code": data.get("code"),
        "language": data.get("language"),
        "title": data.get("title", "Untitled"),
        "created_at": datetime.utcnow(),
        "views": 0
    }
    await db.snippets.insert_one(snippet)
    return {"id": snippet_id, "share_url": f"/snippets/{snippet_id}"}

@api_router.get("/snippets/{snippet_id}")
async def get_snippet(snippet_id: str):
    snippet = await db.snippets.find_one({"id": snippet_id})
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    await db.snippets.update_one({"id": snippet_id}, {"$inc": {"views": 1}})
    snippet['_id'] = str(snippet['_id'])
    return snippet

# History
@api_router.get("/history")
async def get_history(limit: int = 50):
    history = await db.execution_history.find().sort("created_at", -1).to_list(limit)
    return {"history": history}

@api_router.delete("/history")
async def clear_history():
    await db.execution_history.delete_many({})
    return {"success": True}

app.include_router(api_router)
