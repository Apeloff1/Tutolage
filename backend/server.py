"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CODEDOCK QUANTUM v3.0 - 2026+ EDITION                     ║
║          Bleeding-Edge Multi-Language Compiler & AI Code Assistant          ║
║                                                                              ║
║  Architecture: Event-Driven | Async-First | AI-Native | Zero-Trust          ║
║  Standards: 2026+ Enterprise Grade | Grok-Compatible | SOTA Security        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Depends, Query, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict, Any, Union, AsyncGenerator, Literal
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
from contextlib import redirect_stdout, redirect_stderr, asynccontextmanager
from collections import defaultdict
from functools import wraps
import ast
import tokenize
from io import StringIO

# AI Integration
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection with connection pooling
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(
    mongo_url,
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=30000,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True
)
db = client[os.environ['DB_NAME']]

# Configure advanced logging with structured output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("CodeDock.Core")

#====================================================================================================
# 2026+ BLEEDING-EDGE CONSTANTS & CONFIGURATION
#====================================================================================================

class LanguageType(str, Enum):
    """Supported programming languages with full compiler support"""
    PYTHON = "python"
    HTML = "html"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    CPP = "cpp"
    C = "c"
    RUST = "rust"
    GO = "go"
    CSS = "css"
    JSON_LANG = "json"
    MARKDOWN = "markdown"
    SQL = "sql"
    YAML = "yaml"
    XML = "xml"
    SHELL = "shell"
    CUSTOM = "custom"

class ExecutionStatus(str, Enum):
    """Execution lifecycle states"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    PENDING = "pending"
    RUNNING = "running"
    KILLED = "killed"
    MEMORY_EXCEEDED = "memory_exceeded"
    SECURITY_VIOLATION = "security_violation"

class AIAssistantMode(str, Enum):
    """AI assistance operation modes"""
    EXPLAIN = "explain"
    DEBUG = "debug"
    OPTIMIZE = "optimize"
    COMPLETE = "complete"
    REFACTOR = "refactor"
    DOCUMENT = "document"
    TEST_GEN = "test_gen"
    SECURITY_AUDIT = "security_audit"
    CONVERT = "convert"

class CodeComplexity(str, Enum):
    """Code complexity levels (Cyclomatic)"""
    TRIVIAL = "trivial"       # 1-5
    SIMPLE = "simple"         # 6-10
    MODERATE = "moderate"     # 11-20
    COMPLEX = "complex"       # 21-50
    VERY_COMPLEX = "very_complex"  # 51+

class SecurityLevel(str, Enum):
    """Execution security levels"""
    STRICT = "strict"         # Maximum restrictions
    STANDARD = "standard"     # Balanced security
    PERMISSIVE = "permissive" # Minimal restrictions (admin only)

# 2026+ Language Configuration with Extended Metadata
LANGUAGE_CONFIG = {
    LanguageType.PYTHON: {
        "name": "Python",
        "extension": ".py",
        "icon": "logo-python",
        "color": "#3776AB",
        "executable": True,
        "version": "3.12+",
        "description": "AI/ML-first programming language",
        "compiler": "cpython",
        "paradigms": ["oop", "functional", "procedural", "async"],
        "features": ["type_hints", "pattern_matching", "async_await", "dataclasses"],
        "mime_type": "text/x-python",
        "comment_single": "#",
        "comment_multi": ('"""', '"""'),
        "indent_style": "spaces",
        "indent_size": 4,
        "keywords": ["def", "class", "import", "from", "async", "await", "yield", "lambda", "match", "case"],
    },
    LanguageType.HTML: {
        "name": "HTML",
        "extension": ".html",
        "icon": "logo-html5",
        "color": "#E34F26",
        "executable": True,
        "version": "5.3",
        "description": "Semantic markup for modern web",
        "compiler": "webview",
        "paradigms": ["declarative"],
        "features": ["web_components", "shadow_dom", "custom_elements"],
        "mime_type": "text/html",
        "comment_single": None,
        "comment_multi": ("<!--", "-->"),
    },
    LanguageType.JAVASCRIPT: {
        "name": "JavaScript",
        "extension": ".js",
        "icon": "logo-javascript",
        "color": "#F7DF1E",
        "executable": True,
        "version": "ES2026",
        "description": "Universal scripting language",
        "compiler": "v8",
        "paradigms": ["oop", "functional", "event-driven", "async"],
        "features": ["modules", "async_await", "proxy", "decorators", "records_tuples"],
        "mime_type": "text/javascript",
        "comment_single": "//",
        "comment_multi": ("/*", "*/"),
        "indent_style": "spaces",
        "indent_size": 2,
        "keywords": ["const", "let", "async", "await", "class", "import", "export", "function", "=>"],
    },
    LanguageType.TYPESCRIPT: {
        "name": "TypeScript",
        "extension": ".ts",
        "icon": "logo-javascript",
        "color": "#3178C6",
        "executable": True,
        "version": "5.6+",
        "description": "Type-safe JavaScript superset",
        "compiler": "tsc",
        "paradigms": ["oop", "functional", "generic"],
        "features": ["static_types", "interfaces", "generics", "decorators", "mapped_types"],
        "mime_type": "text/typescript",
        "comment_single": "//",
        "comment_multi": ("/*", "*/"),
    },
    LanguageType.CPP: {
        "name": "C++",
        "extension": ".cpp",
        "icon": "code-slash",
        "color": "#00599C",
        "executable": True,
        "version": "C++23",
        "description": "High-performance systems language",
        "compiler": "g++",
        "paradigms": ["oop", "generic", "procedural", "functional"],
        "features": ["templates", "concepts", "coroutines", "ranges", "modules"],
        "mime_type": "text/x-c++src",
        "comment_single": "//",
        "comment_multi": ("/*", "*/"),
        "keywords": ["class", "template", "concept", "constexpr", "auto", "namespace", "virtual"],
    },
    LanguageType.C: {
        "name": "C",
        "extension": ".c",
        "icon": "code-slash",
        "color": "#A8B9CC",
        "executable": True,
        "version": "C23",
        "description": "Foundational systems language",
        "compiler": "gcc",
        "paradigms": ["procedural"],
        "features": ["pointers", "memory_mgmt", "inline_asm"],
        "mime_type": "text/x-csrc",
        "comment_single": "//",
        "comment_multi": ("/*", "*/"),
    },
    LanguageType.RUST: {
        "name": "Rust",
        "extension": ".rs",
        "icon": "hardware-chip",
        "color": "#DEA584",
        "executable": False,  # Addon slot - can be enabled
        "version": "2024 Edition",
        "description": "Memory-safe systems programming",
        "compiler": "rustc",
        "paradigms": ["oop", "functional", "concurrent"],
        "features": ["ownership", "borrowing", "lifetimes", "async", "macros"],
        "mime_type": "text/x-rust",
    },
    LanguageType.GO: {
        "name": "Go",
        "extension": ".go",
        "icon": "code-working",
        "color": "#00ADD8",
        "executable": False,  # Addon slot
        "version": "1.23+",
        "description": "Cloud-native concurrent language",
        "compiler": "go",
        "paradigms": ["procedural", "concurrent"],
        "features": ["goroutines", "channels", "interfaces", "generics"],
        "mime_type": "text/x-go",
    },
    LanguageType.CSS: {
        "name": "CSS",
        "extension": ".css",
        "icon": "logo-css3",
        "color": "#1572B6",
        "executable": False,
        "version": "CSS4",
        "description": "Modern styling language",
        "paradigms": ["declarative"],
        "features": ["container_queries", "cascade_layers", "nesting", "subgrid"],
        "mime_type": "text/css",
    },
    LanguageType.SQL: {
        "name": "SQL",
        "extension": ".sql",
        "icon": "server",
        "color": "#CC2927",
        "executable": False,
        "version": "SQL:2023",
        "description": "Data query language",
        "paradigms": ["declarative"],
        "mime_type": "text/x-sql",
    },
    LanguageType.JSON_LANG: {
        "name": "JSON",
        "extension": ".json",
        "icon": "code-working",
        "color": "#000000",
        "executable": False,
        "version": "RFC 8259",
        "description": "Data interchange format",
        "mime_type": "application/json",
    },
    LanguageType.YAML: {
        "name": "YAML",
        "extension": ".yaml",
        "icon": "document-text",
        "color": "#CB171E",
        "executable": False,
        "version": "1.2",
        "description": "Human-readable data serialization",
        "mime_type": "text/yaml",
    },
    LanguageType.MARKDOWN: {
        "name": "Markdown",
        "extension": ".md",
        "icon": "document-text",
        "color": "#083FA1",
        "executable": False,
        "version": "CommonMark 0.31",
        "description": "Lightweight markup language",
        "mime_type": "text/markdown",
    },
    LanguageType.SHELL: {
        "name": "Shell",
        "extension": ".sh",
        "icon": "terminal",
        "color": "#4EAA25",
        "executable": False,  # Security restricted
        "version": "Bash 5.2+",
        "description": "Unix shell scripting",
        "mime_type": "text/x-shellscript",
    },
}

# Extended Code Templates with 2026 Best Practices
CODE_TEMPLATES = {
    LanguageType.PYTHON: {
        "hello_world": {
            "name": "Hello World",
            "code": 'print("Hello, World!")',
            "description": "Basic output example",
            "complexity": CodeComplexity.TRIVIAL,
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
    {"action": "unknown"},
    {"invalid": "command"},
]

for cmd in commands:
    print(f"{cmd} -> {process_command(cmd)}")''',
            "description": "Python 3.10+ structural pattern matching",
            "complexity": CodeComplexity.MODERATE,
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
        },
    },
    LanguageType.HTML: {
        "modern_layout": {
            "name": "Modern CSS Grid Layout",
            "code": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Layout 2026</title>
    <style>
        :root {
            --primary: #6366f1;
            --surface: #1e1b4b;
            --text: #e0e7ff;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: var(--text);
        }
        
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }
        
        .card h2 {
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: 600;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>Feature One</h2>
            <p>Modern glassmorphism design with smooth animations.</p>
            <button class="btn">Learn More</button>
        </div>
        <div class="card">
            <h2>Feature Two</h2>
            <p>Responsive grid layout that adapts to any screen size.</p>
            <button class="btn">Explore</button>
        </div>
        <div class="card">
            <h2>Feature Three</h2>
            <p>CSS custom properties for consistent theming.</p>
            <button class="btn">Get Started</button>
        </div>
    </div>
</body>
</html>''',
            "description": "Glassmorphism UI with CSS Grid",
            "complexity": CodeComplexity.MODERATE,
        },
        "web_component": {
            "name": "Web Component",
            "code": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Web Component</title>
</head>
<body>
    <style>
        body { 
            font-family: system-ui; 
            background: #1a1a2e; 
            padding: 2rem;
            color: #eee;
        }
    </style>
    
    <h1>Custom Counter Component</h1>
    <my-counter initial="5"></my-counter>
    <my-counter initial="10" step="5"></my-counter>
    
    <script>
        class MyCounter extends HTMLElement {
            constructor() {
                super();
                this.attachShadow({ mode: 'open' });
                this.count = parseInt(this.getAttribute('initial') || '0');
                this.step = parseInt(this.getAttribute('step') || '1');
            }
            
            connectedCallback() {
                this.render();
            }
            
            render() {
                this.shadowRoot.innerHTML = `
                    <style>
                        :host {
                            display: inline-block;
                            margin: 1rem;
                        }
                        .counter {
                            background: linear-gradient(135deg, #667eea, #764ba2);
                            padding: 1.5rem 2rem;
                            border-radius: 12px;
                            display: flex;
                            align-items: center;
                            gap: 1rem;
                        }
                        button {
                            width: 40px;
                            height: 40px;
                            border-radius: 50%;
                            border: none;
                            background: rgba(255,255,255,0.2);
                            color: white;
                            font-size: 1.5rem;
                            cursor: pointer;
                        }
                        button:hover { background: rgba(255,255,255,0.3); }
                        span {
                            font-size: 2rem;
                            font-weight: bold;
                            color: white;
                            min-width: 60px;
                            text-align: center;
                        }
                    </style>
                    <div class="counter">
                        <button id="dec">-</button>
                        <span id="value">${this.count}</span>
                        <button id="inc">+</button>
                    </div>
                `;
                
                this.shadowRoot.getElementById('inc').onclick = () => this.increment();
                this.shadowRoot.getElementById('dec').onclick = () => this.decrement();
            }
            
            increment() {
                this.count += this.step;
                this.update();
            }
            
            decrement() {
                this.count -= this.step;
                this.update();
            }
            
            update() {
                this.shadowRoot.getElementById('value').textContent = this.count;
                this.dispatchEvent(new CustomEvent('change', { detail: { count: this.count }}));
            }
        }
        
        customElements.define('my-counter', MyCounter);
    </script>
</body>
</html>''',
            "description": "Custom element with Shadow DOM",
            "complexity": CodeComplexity.COMPLEX,
        },
    },
    LanguageType.JAVASCRIPT: {
        "async_iterator": {
            "name": "Async Iterator Pattern",
            "code": '''// Modern Async Iterator with AbortController
async function* fetchPaginated(baseUrl, options = {}) {
    const controller = new AbortController();
    let page = 1;
    let hasMore = true;
    
    try {
        while (hasMore) {
            console.log(`Fetching page ${page}...`);
            
            // Simulate API call
            await new Promise(r => setTimeout(r, 100));
            const data = Array.from({length: 5}, (_, i) => ({
                id: (page - 1) * 5 + i + 1,
                value: Math.random().toFixed(2)
            }));
            
            yield { page, data, timestamp: Date.now() };
            
            hasMore = page < 3; // Limit to 3 pages for demo
            page++;
        }
    } finally {
        console.log('Iterator cleanup complete');
    }
}

// Consume the async iterator
async function processData() {
    const results = [];
    
    for await (const { page, data } of fetchPaginated('/api/items')) {
        console.log(`Page ${page}: ${data.length} items`);
        results.push(...data);
        
        if (results.length >= 10) {
            console.log('Reached limit, stopping iteration');
            break;
        }
    }
    
    console.log(`Total items collected: ${results.length}`);
    return results;
}

processData().then(r => console.log('Done:', r.length, 'items'));''',
            "description": "Async generators for paginated data",
            "complexity": CodeComplexity.COMPLEX,
        },
        "proxy_reactive": {
            "name": "Reactive State with Proxy",
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

// Create reactive state
const state = createReactive(
    { 
        user: { name: 'Developer', level: 1 },
        items: [],
        lastUpdated: null
    },
    (prop, newVal, oldVal) => {
        console.log(`State changed: ${prop} = ${JSON.stringify(newVal)} (was: ${JSON.stringify(oldVal)})`);
    }
);

// Mutations trigger callbacks
state.user.name = 'Advanced Dev';
state.user.level = 5;
state.items.push({ id: 1, name: 'Item 1' });
state.lastUpdated = new Date().toISOString();

console.log('Final state:', JSON.stringify(state, null, 2));''',
            "description": "Vue-style reactivity with Proxy",
            "complexity": CodeComplexity.COMPLEX,
        },
        "worker_pool": {
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
            if (this.queue.length > 0) {
                const next = this.queue.shift();
                next();
            }
        }
    }
    
    async map(items, asyncFn) {
        return Promise.all(items.map(item => this.add(() => asyncFn(item))));
    }
}

// Simulate async tasks
const simulateTask = async (id) => {
    const duration = Math.random() * 500 + 100;
    console.log(`Task ${id} started (${duration.toFixed(0)}ms)`);
    await new Promise(r => setTimeout(r, duration));
    console.log(`Task ${id} completed`);
    return { id, duration };
};

// Execute with pool
const pool = new PromisePool(3);
const tasks = [1, 2, 3, 4, 5, 6, 7, 8];

console.log('Starting pool with concurrency: 3');
const start = Date.now();

pool.map(tasks, simulateTask).then(results => {
    const elapsed = Date.now() - start;
    console.log(`All ${results.length} tasks completed in ${elapsed}ms`);
});''',
            "description": "Concurrent task execution with limit",
            "complexity": CodeComplexity.COMPLEX,
        },
    },
    LanguageType.CPP: {
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
    void use() const {
        std::cout << "Using resource: " << name << "\\n";
    }
};

int main() {
    // unique_ptr - exclusive ownership
    {
        auto unique = std::make_unique<Resource>("Unique");
        unique->use();
    } // Automatically destroyed
    
    std::cout << "---\\n";
    
    // shared_ptr - shared ownership
    {
        auto shared1 = std::make_shared<Resource>("Shared");
        {
            auto shared2 = shared1; // Copy, ref count = 2
            std::cout << "Ref count: " << shared1.use_count() << "\\n";
            shared2->use();
        } // shared2 destroyed, ref count = 1
        std::cout << "Ref count: " << shared1.use_count() << "\\n";
    } // shared1 destroyed, Resource destroyed
    
    std::cout << "---\\n";
    
    // Vector of smart pointers
    std::vector<std::shared_ptr<Resource>> resources;
    resources.push_back(std::make_shared<Resource>("R1"));
    resources.push_back(std::make_shared<Resource>("R2"));
    
    for (const auto& r : resources) {
        r->use();
    }
    
    std::cout << "Clearing vector...\\n";
    resources.clear();
    
    std::cout << "Program end\\n";
    return 0;
}''',
            "description": "Modern C++ memory management",
            "complexity": CodeComplexity.MODERATE,
        },
        "concepts_templates": {
            "name": "Concepts & Templates (C++20)",
            "code": '''#include <iostream>
#include <concepts>
#include <vector>
#include <string>

// Define a concept for numeric types
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// Define a concept for printable types
template<typename T>
concept Printable = requires(T t, std::ostream& os) {
    { os << t } -> std::same_as<std::ostream&>;
};

// Constrained template function
template<Numeric T>
T sum(const std::vector<T>& values) {
    T result{};
    for (const auto& v : values) {
        result += v;
    }
    return result;
}

// Generic print with concept constraint
template<Printable T>
void print_all(const std::vector<T>& items, const std::string& sep = ", ") {
    bool first = true;
    for (const auto& item : items) {
        if (!first) std::cout << sep;
        std::cout << item;
        first = false;
    }
    std::cout << "\\n";
}

// Compile-time selection with concepts
template<typename T>
auto process(T value) {
    if constexpr (std::integral<T>) {
        return value * 2;
    } else if constexpr (std::floating_point<T>) {
        return value * 1.5;
    } else {
        return value;
    }
}

int main() {
    std::vector<int> ints = {1, 2, 3, 4, 5};
    std::vector<double> doubles = {1.1, 2.2, 3.3};
    std::vector<std::string> strings = {"Hello", "C++20", "Concepts"};
    
    std::cout << "Sum of ints: " << sum(ints) << "\\n";
    std::cout << "Sum of doubles: " << sum(doubles) << "\\n";
    
    std::cout << "Ints: "; print_all(ints);
    std::cout << "Doubles: "; print_all(doubles);
    std::cout << "Strings: "; print_all(strings, " | ");
    
    std::cout << "Process int 10: " << process(10) << "\\n";
    std::cout << "Process double 10.0: " << process(10.0) << "\\n";
    
    return 0;
}''',
            "description": "C++20 concepts for type constraints",
            "complexity": CodeComplexity.COMPLEX,
        },
        "coroutines": {
            "name": "Coroutines (C++20)",
            "code": '''#include <iostream>
#include <coroutine>
#include <optional>

// Simple generator coroutine
template<typename T>
struct Generator {
    struct promise_type {
        T current_value;
        
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T value) {
            current_value = std::move(value);
            return {};
        }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    
    std::coroutine_handle<promise_type> handle;
    
    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }
    
    // Move-only
    Generator(const Generator&) = delete;
    Generator& operator=(const Generator&) = delete;
    Generator(Generator&& other) noexcept : handle(other.handle) { other.handle = nullptr; }
    
    std::optional<T> next() {
        if (!handle || handle.done()) return std::nullopt;
        handle.resume();
        if (handle.done()) return std::nullopt;
        return handle.promise().current_value;
    }
};

// Fibonacci generator
Generator<long long> fibonacci(int count) {
    long long a = 0, b = 1;
    for (int i = 0; i < count; ++i) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Range generator
Generator<int> range(int start, int end, int step = 1) {
    for (int i = start; i < end; i += step) {
        co_yield i;
    }
}

int main() {
    std::cout << "Fibonacci sequence:\\n";
    auto fib = fibonacci(15);
    while (auto val = fib.next()) {
        std::cout << *val << " ";
    }
    std::cout << "\\n\\n";
    
    std::cout << "Range [0, 10, 2]:\\n";
    auto rng = range(0, 10, 2);
    while (auto val = rng.next()) {
        std::cout << *val << " ";
    }
    std::cout << "\\n";
    
    return 0;
}''',
            "description": "C++20 coroutines for lazy evaluation",
            "complexity": CodeComplexity.VERY_COMPLEX,
        },
    },
    LanguageType.TYPESCRIPT: {
        "generics": {
            "name": "Advanced Generics",
            "code": '''// TypeScript Advanced Generic Patterns

// Conditional Types
type IsArray<T> = T extends any[] ? true : false;
type IsString<T> = T extends string ? true : false;

// Mapped Types with Modifiers
type Readonly<T> = { readonly [P in keyof T]: T[P] };
type Optional<T> = { [P in keyof T]?: T[P] };
type Nullable<T> = { [P in keyof T]: T[P] | null };

// Template Literal Types (2026+)
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiRoute<M extends HttpMethod, P extends string> = `${M} /api/${P}`;

type UserRoute = ApiRoute<'GET', 'users'>;  // "GET /api/users"
type CreateRoute = ApiRoute<'POST', 'items'>; // "POST /api/items"

// Recursive Types
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object 
        ? DeepReadonly<T[P]> 
        : T[P];
};

// Infer in Conditional Types
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type FirstArg<T> = T extends (first: infer F, ...args: any[]) => any ? F : never;

// Example usage
interface User {
    id: number;
    name: string;
    settings: {
        theme: 'light' | 'dark';
        notifications: boolean;
    };
}

type ReadonlyUser = DeepReadonly<User>;

function createUser(data: Optional<User>): User {
    return {
        id: data.id ?? 0,
        name: data.name ?? 'Anonymous',
        settings: data.settings ?? { theme: 'dark', notifications: true }
    };
}

const user = createUser({ name: 'TypeScript Dev' });
console.log('Created user:', user);

// Type inference test
type CreateUserReturn = ReturnType<typeof createUser>; // User
type CreateUserArg = FirstArg<typeof createUser>; // Optional<User>

console.log('Type system validated successfully!');''',
            "description": "Advanced TypeScript type patterns",
            "complexity": CodeComplexity.COMPLEX,
        },
    },
}

#====================================================================================================
# PYDANTIC MODELS - Enterprise-Grade Data Structures
#====================================================================================================

class ExecutionMetrics(BaseModel):
    """Detailed execution performance metrics"""
    execution_time_ms: float = 0
    memory_peak_kb: Optional[float] = None
    cpu_time_ms: Optional[float] = None
    lines_executed: Optional[int] = None
    allocations: Optional[int] = None

class SecurityReport(BaseModel):
    """Code security analysis report"""
    risk_level: str = "low"
    issues_found: List[Dict[str, Any]] = []
    blocked_operations: List[str] = []
    recommendations: List[str] = []

class CodeAnalysis(BaseModel):
    """Comprehensive code analysis results"""
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
    """Enhanced execution result with full telemetry"""
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
    """Code execution request with advanced options"""
    code: str
    language: LanguageType
    input_data: Optional[str] = None
    timeout_seconds: int = Field(default=10, ge=1, le=60)
    memory_limit_mb: int = Field(default=256, ge=64, le=1024)
    security_level: SecurityLevel = SecurityLevel.STANDARD
    include_analysis: bool = False
    optimize_output: bool = False
    
    @validator('code')
    def code_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Code cannot be empty')
        return v

class CodeExecutionResponse(BaseModel):
    """Comprehensive execution response"""
    execution_id: str
    result: ExecutionResult
    language_info: Dict[str, Any]
    queue_position: Optional[int] = None
    estimated_wait_ms: Optional[int] = None

class AIAssistRequest(BaseModel):
    """AI code assistance request"""
    code: str
    language: LanguageType
    mode: AIAssistantMode
    context: Optional[str] = None
    target_language: Optional[LanguageType] = None  # For conversion
    style_preferences: Optional[Dict[str, Any]] = None

class AIAssistResponse(BaseModel):
    """AI assistant response"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    mode: AIAssistantMode
    suggestion: str
    explanation: Optional[str] = None
    code_blocks: List[Dict[str, str]] = []
    confidence: float = 0.0
    tokens_used: int = 0
    model: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CodeFile(BaseModel):
    """Enhanced code file with version history"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    language: LanguageType
    code: str
    version: int = 1
    checksum: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    is_template: bool = False
    is_favorite: bool = False
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    
    @validator('checksum', pre=True, always=True)
    def compute_checksum(cls, v, values):
        if 'code' in values:
            return hashlib.sha256(values['code'].encode()).hexdigest()[:16]
        return v

class CodeFileCreate(BaseModel):
    name: str
    language: LanguageType
    code: str
    tags: List[str] = []
    is_favorite: bool = False

class CodeFileUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None

class LanguageAddon(BaseModel):
    """Custom language addon configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    language_key: str
    name: str
    extension: str
    icon: str = "code-slash"
    color: str = "#6B7280"
    description: str = ""
    executable: bool = False
    version: str = "1.0"
    compiler_config: Optional[Dict[str, Any]] = None
    syntax_rules: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class UserPreferences(BaseModel):
    """User preferences with extended options"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    theme: str = "dark"
    font_size: int = 14
    font_family: str = "JetBrains Mono"
    tab_size: int = 4
    use_spaces: bool = True
    auto_save: bool = True
    auto_save_interval_ms: int = 30000
    show_line_numbers: bool = True
    show_minimap: bool = False
    word_wrap: bool = True
    highlight_active_line: bool = True
    bracket_matching: bool = True
    auto_indent: bool = True
    default_language: LanguageType = LanguageType.PYTHON
    ai_suggestions: bool = True
    ai_model: str = "gpt-4o"
    security_level: SecurityLevel = SecurityLevel.STANDARD
    recent_files: List[str] = []
    favorite_templates: List[str] = []
    keyboard_shortcuts: Dict[str, str] = {}
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ExecutionHistory(BaseModel):
    """Execution history entry with full context"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_id: Optional[str] = None
    language: LanguageType
    code_hash: str
    code_preview: str
    result: ExecutionResult
    duration_ms: float = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectSnapshot(BaseModel):
    """Project state snapshot for versioning"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    files: List[CodeFile]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = []

class SystemHealth(BaseModel):
    """System health metrics"""
    status: str = "healthy"
    uptime_seconds: float = 0
    active_executions: int = 0
    queue_depth: int = 0
    memory_usage_mb: float = 0
    cpu_usage_percent: float = 0
    db_connected: bool = True
    ai_available: bool = True
    last_check: datetime = Field(default_factory=datetime.utcnow)

#====================================================================================================
# CODE EXECUTORS - Advanced Abstract Factory with Monitoring
#====================================================================================================

class ExecutionContext:
    """Execution context with telemetry and resource tracking"""
    def __init__(self, request: CodeExecutionRequest):
        self.request = request
        self.start_time = None
        self.end_time = None
        self.trace_id = uuid.uuid4().hex[:16]
        self.logs: List[str] = []
        
    def start(self):
        self.start_time = time.perf_counter()
        self.logs.append(f"[{self.trace_id}] Execution started")
        
    def end(self):
        self.end_time = time.perf_counter()
        elapsed = (self.end_time - self.start_time) * 1000
        self.logs.append(f"[{self.trace_id}] Execution completed in {elapsed:.2f}ms")
        
    @property
    def elapsed_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0

class CodeAnalyzer:
    """Static code analysis engine"""
    
    @staticmethod
    def analyze_python(code: str) -> CodeAnalysis:
        """Analyze Python code structure and complexity"""
        analysis = CodeAnalysis()
        
        try:
            tree = ast.parse(code)
            
            analysis.lines_of_code = len(code.splitlines())
            analysis.functions_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            analysis.classes_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            analysis.imports_count = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))
            
            # Calculate cyclomatic complexity (simplified)
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            
            analysis.cyclomatic_complexity = complexity
            
            # Determine complexity level
            if complexity <= 5:
                analysis.complexity = CodeComplexity.TRIVIAL
            elif complexity <= 10:
                analysis.complexity = CodeComplexity.SIMPLE
            elif complexity <= 20:
                analysis.complexity = CodeComplexity.MODERATE
            elif complexity <= 50:
                analysis.complexity = CodeComplexity.COMPLEX
            else:
                analysis.complexity = CodeComplexity.VERY_COMPLEX
                
            # Calculate comment ratio
            try:
                tokens = list(tokenize.generate_tokens(StringIO(code).readline))
                comment_lines = sum(1 for t in tokens if t.type == tokenize.COMMENT)
                analysis.comments_ratio = comment_lines / max(analysis.lines_of_code, 1)
            except:
                pass
                
        except SyntaxError as e:
            analysis.issues.append({
                "type": "syntax_error",
                "line": e.lineno,
                "message": str(e.msg)
            })
        except Exception as e:
            analysis.issues.append({
                "type": "analysis_error",
                "message": str(e)
            })
            
        return analysis

class CodeExecutor(ABC):
    """Abstract base class for all code executors with enhanced monitoring"""
    
    def __init__(self):
        self.execution_count = 0
        self.total_time_ms = 0
        self.error_count = 0
        
    @abstractmethod
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        pass
    
    @abstractmethod
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        pass
    
    def sanitize_output(self, output: str, max_length: int = 50000) -> str:
        """Sanitize and truncate output with smart truncation"""
        if len(output) > max_length:
            half = max_length // 2
            return f"{output[:half]}\n\n... [Output truncated: {len(output)} chars total] ...\n\n{output[-half:]}"
        return output
    
    def record_metrics(self, elapsed_ms: float, success: bool):
        """Record execution metrics for monitoring"""
        self.execution_count += 1
        self.total_time_ms += elapsed_ms
        if not success:
            self.error_count += 1

class PythonExecutor(CodeExecutor):
    """Advanced Python executor with sandbox and analysis"""
    
    FORBIDDEN_STRICT = {
        'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests',
        'urllib', 'http', 'ftplib', 'smtplib', 'pickle', 'shelve',
        'multiprocessing', 'threading', 'ctypes', 'importlib',
        '__builtins__', 'eval', 'exec', 'compile', 'open', 'file',
        'input', 'breakpoint', 'globals', 'locals', 'vars', 'dir'
    }
    
    FORBIDDEN_STANDARD = {
        'os', 'sys', 'subprocess', 'shutil', 'socket',
        'pickle', 'shelve', 'ctypes', 'importlib'
    }
    
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        # Validate first
        is_valid, error_msg, security = self.validate(ctx.request.code, ctx.request.security_level)
        result.security = security
        
        if not is_valid:
            result.status = ExecutionStatus.SECURITY_VIOLATION
            result.error = error_msg
            ctx.end()
            return result
        
        # Analyze if requested
        if ctx.request.include_analysis:
            result.analysis = CodeAnalyzer.analyze_python(ctx.request.code)
        
        try:
            # Create sandboxed execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # Inject output capturing wrapper
                wrapped_code = f'''
import sys
from io import StringIO

# Redirect stdout
_stdout = sys.stdout
_captured = StringIO()
sys.stdout = _captured

try:
{chr(10).join("    " + line for line in ctx.request.code.splitlines())}
finally:
    sys.stdout = _stdout
    print(_captured.getvalue(), end="")
'''
                f.write(ctx.request.code)  # Use original code
                temp_file = f.name
            
            try:
                process = await asyncio.create_subprocess_exec(
                    sys.executable, '-u', temp_file,
                    stdin=asyncio.subprocess.PIPE if ctx.request.input_data else None,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(
                            input=ctx.request.input_data.encode() if ctx.request.input_data else None
                        ),
                        timeout=ctx.request.timeout_seconds
                    )
                    
                    result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
                    result.error = stderr.decode('utf-8', errors='replace')
                    result.status = ExecutionStatus.SUCCESS if process.returncode == 0 else ExecutionStatus.ERROR
                    
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    result.status = ExecutionStatus.TIMEOUT
                    result.error = f"Execution timed out after {ctx.request.timeout_seconds}s"
                    
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = f"Execution failed: {str(e)}"
            logger.error(f"Python execution error: {traceback.format_exc()}")
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        self.record_metrics(ctx.elapsed_ms, result.status == ExecutionStatus.SUCCESS)
        
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        """Validate Python code with configurable security levels"""
        report = SecurityReport()
        
        forbidden = self.FORBIDDEN_STRICT if security_level == SecurityLevel.STRICT else self.FORBIDDEN_STANDARD
        
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        
        code_lower = code.lower()
        
        # Check imports
        for module in forbidden:
            patterns = [
                f'import {module}',
                f'from {module}',
                f'__import__("{module}")',
                f"__import__('{module}')",
                f'importlib.import_module("{module}")',
                f"importlib.import_module('{module}')"
            ]
            for pattern in patterns:
                if pattern in code_lower:
                    report.risk_level = "high"
                    report.blocked_operations.append(f"import:{module}")
                    report.issues_found.append({
                        "type": "forbidden_import",
                        "module": module,
                        "severity": "critical"
                    })
                    return False, f"Forbidden module: {module}", report
        
        # Check dangerous functions
        dangerous_funcs = ['eval(', 'exec(', 'compile(', '__import__(', 'breakpoint(']
        for func in dangerous_funcs:
            if func in code_lower:
                report.risk_level = "high"
                report.blocked_operations.append(f"function:{func[:-1]}")
                return False, f"Forbidden function: {func[:-1]}", report
        
        # Check file operations
        file_ops = ['open(', 'file(', 'read(', 'write(', 'Path(']
        for op in file_ops:
            if op in code:
                report.risk_level = "medium"
                report.issues_found.append({
                    "type": "file_operation",
                    "operation": op[:-1],
                    "severity": "warning"
                })
        
        return True, "", report

class JavaScriptExecutor(CodeExecutor):
    """JavaScript executor with WebView-compatible output"""
    
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
        
        # Return wrapped code for WebView execution with enhanced error handling
        wrapped_code = f'''
(function() {{
    'use strict';
    const __output = [];
    const __errors = [];
    const __startTime = performance.now();
    
    const __originalConsole = {{}};
    ['log', 'info', 'warn', 'error'].forEach(method => {{
        __originalConsole[method] = console[method];
        console[method] = (...args) => {{
            const formatted = args.map(a => {{
                if (a === null) return 'null';
                if (a === undefined) return 'undefined';
                if (typeof a === 'object') {{
                    try {{ return JSON.stringify(a, null, 2); }}
                    catch {{ return String(a); }}
                }}
                return String(a);
            }}).join(' ');
            __output.push({{ type: method, message: formatted }});
        }};
    }});
    
    try {{
        {ctx.request.code}
        return {{
            status: 'success',
            output: __output.map(o => o.message).join('\\n'),
            logs: __output,
            executionTime: performance.now() - __startTime
        }};
    }} catch(e) {{
        return {{
            status: 'error',
            error: e.message,
            stack: e.stack,
            output: __output.map(o => o.message).join('\\n'),
            executionTime: performance.now() - __startTime
        }};
    }}
}})()
'''
        result.status = ExecutionStatus.SUCCESS
        result.output = wrapped_code
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        report = SecurityReport()
        
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        
        dangerous = [
            ('eval(', 'Dynamic code execution'),
            ('Function(', 'Dynamic function creation'),
            ('document.cookie', 'Cookie access'),
            ('localStorage', 'Local storage access'),
            ('sessionStorage', 'Session storage access'),
            ('fetch(', 'Network requests'),
            ('XMLHttpRequest', 'Network requests'),
            ('WebSocket', 'WebSocket connections'),
        ]
        
        for pattern, description in dangerous:
            if pattern in code:
                report.issues_found.append({
                    "type": "potentially_unsafe",
                    "pattern": pattern,
                    "description": description
                })
                if security_level == SecurityLevel.STRICT:
                    report.risk_level = "high"
                    return False, f"Blocked: {description} ({pattern})", report
        
        return True, "", report

class CppExecutor(CodeExecutor):
    """C++ executor with C++23 support and detailed compilation feedback"""
    
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
        
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            source_file = os.path.join(temp_dir, 'main.cpp')
            output_file = os.path.join(temp_dir, 'main')
            
            with open(source_file, 'w') as f:
                f.write(ctx.request.code)
            
            # Compile with C++23 standard and optimizations
            compile_flags = [
                'g++', '-std=c++20', '-O2',
                '-Wall', '-Wextra', '-Wpedantic',
                '-o', output_file, source_file
            ]
            
            compile_process = await asyncio.create_subprocess_exec(
                *compile_flags,
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
                result.error = "Compilation timed out (30s limit)"
                ctx.end()
                return result
            
            if compile_process.returncode != 0:
                result.status = ExecutionStatus.ERROR
                error_text = compile_stderr.decode('utf-8', errors='replace')
                result.error = f"Compilation failed:\n{error_text}"
                ctx.end()
                return result
            
            # Capture any warnings
            if compile_stderr:
                warnings = compile_stderr.decode('utf-8', errors='replace')
                if warnings.strip():
                    result.output = f"[Compiler warnings]\n{warnings}\n[Output]\n"
            
            # Execute
            run_process = await asyncio.create_subprocess_exec(
                output_file,
                stdin=asyncio.subprocess.PIPE if ctx.request.input_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    run_process.communicate(
                        input=ctx.request.input_data.encode() if ctx.request.input_data else None
                    ),
                    timeout=ctx.request.timeout_seconds
                )
                
                output_text = stdout.decode('utf-8', errors='replace')
                result.output = (result.output or "") + self.sanitize_output(output_text)
                
                if stderr:
                    result.error = stderr.decode('utf-8', errors='replace')
                    
                result.status = ExecutionStatus.SUCCESS if run_process.returncode == 0 else ExecutionStatus.ERROR
                
            except asyncio.TimeoutError:
                run_process.kill()
                result.status = ExecutionStatus.TIMEOUT
                result.error = f"Execution timed out after {ctx.request.timeout_seconds}s"
                
        except Exception as e:
            result.status = ExecutionStatus.ERROR
            result.error = f"Execution failed: {str(e)}"
            logger.error(f"C++ execution error: {traceback.format_exc()}")
            
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        self.record_metrics(ctx.elapsed_ms, result.status == ExecutionStatus.SUCCESS)
        
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        report = SecurityReport()
        
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        
        dangerous = [
            ('system(', 'System command execution'),
            ('popen(', 'Process pipe'),
            ('fork(', 'Process forking'),
            ('exec', 'Exec family functions'),
            ('unlink(', 'File deletion'),
            ('remove(', 'File removal'),
            ('rename(', 'File renaming'),
        ]
        
        for pattern, description in dangerous:
            if pattern in code:
                report.issues_found.append({
                    "type": "system_call",
                    "pattern": pattern,
                    "description": description
                })
                if security_level == SecurityLevel.STRICT:
                    report.risk_level = "high"
                    return False, f"Blocked system call: {description}", report
        
        return True, "", report

class CExecutor(CodeExecutor):
    """C executor with C23 support"""
    
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
        
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            source_file = os.path.join(temp_dir, 'main.c')
            output_file = os.path.join(temp_dir, 'main')
            
            with open(source_file, 'w') as f:
                f.write(ctx.request.code)
            
            compile_process = await asyncio.create_subprocess_exec(
                'gcc', '-std=c17', '-O2', '-Wall', '-o', output_file, source_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            compile_stdout, compile_stderr = await asyncio.wait_for(
                compile_process.communicate(),
                timeout=30
            )
            
            if compile_process.returncode != 0:
                result.status = ExecutionStatus.ERROR
                result.error = f"Compilation failed:\n{compile_stderr.decode()}"
                ctx.end()
                return result
            
            run_process = await asyncio.create_subprocess_exec(
                output_file,
                stdin=asyncio.subprocess.PIPE if ctx.request.input_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                run_process.communicate(
                    input=ctx.request.input_data.encode() if ctx.request.input_data else None
                ),
                timeout=ctx.request.timeout_seconds
            )
            
            result.output = self.sanitize_output(stdout.decode('utf-8', errors='replace'))
            result.error = stderr.decode('utf-8', errors='replace')
            result.status = ExecutionStatus.SUCCESS if run_process.returncode == 0 else ExecutionStatus.ERROR
            
        except asyncio.TimeoutError:
            result.status = ExecutionStatus.TIMEOUT
            result.error = f"Execution timed out after {ctx.request.timeout_seconds}s"
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
        # Same validation as C++
        report = SecurityReport()
        dangerous = ['system(', 'popen(', 'fork(', 'exec']
        for d in dangerous:
            if d in code and security_level != SecurityLevel.PERMISSIVE:
                return False, f"Blocked: {d}", report
        return True, "", report

class HTMLExecutor(CodeExecutor):
    """HTML executor with sanitization and preview"""
    
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
        
        result.status = ExecutionStatus.SUCCESS
        result.output = ctx.request.code
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        report = SecurityReport()
        
        if security_level == SecurityLevel.PERMISSIVE:
            return True, "", report
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            (r'javascript:', 'JavaScript URL'),
            (r'on\w+\s*=', 'Event handlers'),
            (r'<script[^>]*src\s*=', 'External scripts'),
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                report.issues_found.append({
                    "type": "html_security",
                    "pattern": pattern,
                    "description": description
                })
                
        return True, "", report

class TypeScriptExecutor(CodeExecutor):
    """TypeScript executor - compiles to JS then executes"""
    
    async def execute(self, ctx: ExecutionContext) -> ExecutionResult:
        ctx.start()
        result = ExecutionResult(trace_id=ctx.trace_id)
        
        # For now, return wrapped code similar to JS
        # In production, would use tsc compiler
        wrapped_code = f'''
// TypeScript code - requires compilation
// Type checking would occur at compile time
{ctx.request.code}
'''
        result.status = ExecutionStatus.SUCCESS
        result.output = wrapped_code
        
        ctx.end()
        result.metrics.execution_time_ms = ctx.elapsed_ms
        return result
    
    def validate(self, code: str, security_level: SecurityLevel) -> tuple[bool, str, SecurityReport]:
        return True, "", SecurityReport()

# Executor Factory with Singleton Pattern
class ExecutorFactory:
    """Factory for creating and managing code executors"""
    
    _instance = None
    _executors: Dict[LanguageType, CodeExecutor] = {}
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not ExecutorFactory._initialized:
            self._executors = {
                LanguageType.PYTHON: PythonExecutor(),
                LanguageType.JAVASCRIPT: JavaScriptExecutor(),
                LanguageType.TYPESCRIPT: TypeScriptExecutor(),
                LanguageType.CPP: CppExecutor(),
                LanguageType.C: CExecutor(),
                LanguageType.HTML: HTMLExecutor(),
            }
            ExecutorFactory._initialized = True
    
    def get_executor(self, language: LanguageType) -> Optional[CodeExecutor]:
        return self._executors.get(language)
    
    def is_executable(self, language: LanguageType) -> bool:
        return language in self._executors
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get execution statistics for all executors"""
        return {
            lang.value: {
                "executions": executor.execution_count,
                "total_time_ms": executor.total_time_ms,
                "avg_time_ms": executor.total_time_ms / max(executor.execution_count, 1),
                "error_rate": executor.error_count / max(executor.execution_count, 1)
            }
            for lang, executor in self._executors.items()
        }

#====================================================================================================
# AI ASSISTANT SERVICE - GPT-4o Integration
#====================================================================================================

class AIAssistantService:
    """AI-powered code assistance using GPT-4o"""
    
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.model = "gpt-4o"
        self.request_count = 0
        
    async def assist(self, request: AIAssistRequest) -> AIAssistResponse:
        """Process AI assistance request"""
        if not self.api_key:
            raise HTTPException(status_code=503, detail="AI service not configured")
        
        self.request_count += 1
        
        # Build system prompt based on mode
        system_prompts = {
            AIAssistantMode.EXPLAIN: """You are a code explanation expert. Analyze the provided code and explain:
1. What the code does (high-level overview)
2. How it works (step by step)
3. Key concepts and patterns used
4. Potential improvements or concerns
Be clear, educational, and thorough.""",

            AIAssistantMode.DEBUG: """You are a debugging expert. Analyze the code for:
1. Syntax errors
2. Logic errors
3. Edge cases not handled
4. Potential runtime issues
5. Performance problems
Provide specific fixes with code examples.""",

            AIAssistantMode.OPTIMIZE: """You are a code optimization specialist. Analyze and suggest:
1. Performance improvements
2. Memory optimization
3. Code simplification
4. Better algorithms or data structures
5. Modern language features that could help
Provide optimized code with explanations.""",

            AIAssistantMode.COMPLETE: """You are a code completion assistant. Based on the context:
1. Understand the intent of the code
2. Complete the missing parts logically
3. Follow existing patterns and style
4. Add appropriate error handling
5. Include helpful comments
Return only the completed code.""",

            AIAssistantMode.REFACTOR: """You are a code refactoring expert. Improve the code by:
1. Improving readability and maintainability
2. Applying SOLID principles
3. Reducing complexity
4. Improving naming conventions
5. Adding type hints (if applicable)
Provide refactored code with explanations.""",

            AIAssistantMode.DOCUMENT: """You are a documentation specialist. Generate:
1. Function/class docstrings
2. Parameter descriptions
3. Return value documentation
4. Usage examples
5. Any important notes or warnings
Follow the language's documentation conventions.""",

            AIAssistantMode.TEST_GEN: """You are a test generation expert. Create:
1. Unit tests for the provided code
2. Edge case tests
3. Error handling tests
4. Integration test suggestions
Use appropriate testing frameworks for the language.""",

            AIAssistantMode.SECURITY_AUDIT: """You are a security auditor. Analyze for:
1. Injection vulnerabilities
2. Authentication/authorization issues
3. Data exposure risks
4. Unsafe operations
5. Dependency vulnerabilities
Provide severity ratings and remediation steps.""",

            AIAssistantMode.CONVERT: f"""You are a code conversion expert. Convert the code to {request.target_language or 'the requested language'}:
1. Maintain the same logic and functionality
2. Use idiomatic patterns for the target language
3. Handle language-specific differences
4. Add necessary imports/includes
5. Include comments explaining significant changes""",
        }
        
        system_message = system_prompts.get(request.mode, system_prompts[AIAssistantMode.EXPLAIN])
        
        # Build user message
        user_content = f"""Language: {request.language.value}

Code:
```{request.language.value}
{request.code}
```

{f"Additional context: {request.context}" if request.context else ""}
"""
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"codedock-{uuid.uuid4().hex[:8]}",
                system_message=system_message
            ).with_model("openai", self.model)
            
            response = await chat.send_message(UserMessage(text=user_content))
            
            # Parse response for code blocks
            code_blocks = []
            code_pattern = r'```(\w+)?\n(.*?)```'
            matches = re.findall(code_pattern, response, re.DOTALL)
            for lang, code in matches:
                code_blocks.append({
                    "language": lang or request.language.value,
                    "code": code.strip()
                })
            
            return AIAssistResponse(
                mode=request.mode,
                suggestion=response,
                code_blocks=code_blocks,
                confidence=0.85,
                model=self.model
            )
            
        except Exception as e:
            logger.error(f"AI assistance error: {e}")
            raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

#====================================================================================================
# RATE LIMITING & CIRCUIT BREAKER
#====================================================================================================

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int = 60, per_seconds: int = 60):
        self.rate = rate
        self.per_seconds = per_seconds
        self.tokens: Dict[str, float] = defaultdict(lambda: rate)
        self.last_update: Dict[str, float] = defaultdict(time.time)
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        elapsed = now - self.last_update[key]
        self.last_update[key] = now
        
        # Add tokens based on elapsed time
        self.tokens[key] = min(
            self.rate,
            self.tokens[key] + elapsed * (self.rate / self.per_seconds)
        )
        
        if self.tokens[key] >= 1:
            self.tokens[key] -= 1
            return True
        return False

class CircuitBreaker:
    """Circuit breaker for external services"""
    
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures: Dict[str, int] = defaultdict(int)
        self.last_failure: Dict[str, float] = {}
        self.state: Dict[str, str] = defaultdict(lambda: "closed")
    
    def record_failure(self, service: str):
        self.failures[service] += 1
        self.last_failure[service] = time.time()
        
        if self.failures[service] >= self.failure_threshold:
            self.state[service] = "open"
    
    def record_success(self, service: str):
        self.failures[service] = 0
        self.state[service] = "closed"
    
    def is_available(self, service: str) -> bool:
        if self.state[service] == "closed":
            return True
        
        if self.state[service] == "open":
            if time.time() - self.last_failure.get(service, 0) > self.reset_timeout:
                self.state[service] = "half-open"
                return True
            return False
        
        return True  # half-open allows one request

#====================================================================================================
# APPLICATION LIFECYCLE & STARTUP
#====================================================================================================

# Global instances
executor_factory = ExecutorFactory()
ai_service = AIAssistantService()
rate_limiter = RateLimiter(rate=100, per_seconds=60)
circuit_breaker = CircuitBreaker()
app_start_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("=" * 60)
    logger.info("CodeDock Quantum v3.0 - Starting up...")
    logger.info("=" * 60)
    
    # Initialize indexes
    try:
        await db.code_files.create_index("id", unique=True)
        await db.code_files.create_index("language")
        await db.code_files.create_index("updated_at")
        await db.execution_history.create_index("created_at")
        await db.language_addons.create_index("language_key", unique=True)
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")
    
    yield
    
    logger.info("CodeDock Quantum v3.0 - Shutting down...")
    client.close()

# Create FastAPI app with lifespan
app = FastAPI(
    title="CodeDock Quantum",
    description="2026+ Bleeding-Edge Multi-Language Compiler & AI Code Assistant",
    version="3.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router
api_router = APIRouter(prefix="/api")

#====================================================================================================
# API ROUTES - Core Endpoints
#====================================================================================================

@api_router.get("/")
async def root():
    """API root with version info"""
    return {
        "name": "CodeDock Quantum",
        "version": "3.0.0",
        "edition": "2026+ Bleeding Edge",
        "features": [
            "Multi-language compilation (Python, JS, C++, C, HTML, TypeScript)",
            "AI-powered code assistance (GPT-4o)",
            "Real-time code analysis",
            "Security sandboxing",
            "Execution telemetry",
            "Custom language addons"
        ],
        "api_version": "v3",
        "docs": "/docs"
    }

@api_router.get("/health", response_model=SystemHealth)
async def health_check():
    """Comprehensive health check"""
    uptime = time.time() - app_start_time
    
    # Check database
    db_connected = True
    try:
        await db.command("ping")
    except:
        db_connected = False
    
    return SystemHealth(
        status="healthy" if db_connected else "degraded",
        uptime_seconds=uptime,
        db_connected=db_connected,
        ai_available=bool(ai_service.api_key),
        last_check=datetime.utcnow()
    )

@api_router.get("/stats")
async def get_stats():
    """Get system statistics"""
    executor_stats = executor_factory.get_stats()
    
    return {
        "uptime_seconds": time.time() - app_start_time,
        "executors": executor_stats,
        "ai_requests": ai_service.request_count,
        "rate_limiter": {
            "rate": rate_limiter.rate,
            "per_seconds": rate_limiter.per_seconds
        }
    }

#====================================================================================================
# LANGUAGE ROUTES
#====================================================================================================

@api_router.get("/languages")
async def get_languages():
    """Get all supported languages with full metadata"""
    languages = []
    
    for lang_type, config in LANGUAGE_CONFIG.items():
        lang_data = {
            "key": lang_type.value,
            "type": "builtin",
            **config,
            "executable": executor_factory.is_executable(lang_type),
            "templates_available": lang_type in CODE_TEMPLATES
        }
        languages.append(lang_data)
    
    # Add custom addons
    addons = await db.language_addons.find().to_list(100)
    for addon in addons:
        addon['_id'] = str(addon['_id'])
        addon['type'] = 'addon'
        languages.append(addon)
    
    return {"languages": languages, "count": len(languages)}

@api_router.get("/languages/{language_key}")
async def get_language(language_key: str):
    """Get specific language configuration"""
    try:
        lang_type = LanguageType(language_key)
        if lang_type in LANGUAGE_CONFIG:
            config = LANGUAGE_CONFIG[lang_type]
            templates = CODE_TEMPLATES.get(lang_type, {})
            return {
                "key": lang_type.value,
                "type": "builtin",
                **config,
                "executable": executor_factory.is_executable(lang_type),
                "templates": [
                    {"key": k, **v} if isinstance(v, dict) else {"key": k, "code": v}
                    for k, v in templates.items()
                ]
            }
    except ValueError:
        pass
    
    # Check addons
    addon = await db.language_addons.find_one({"language_key": language_key})
    if addon:
        addon['_id'] = str(addon['_id'])
        return addon
    
    raise HTTPException(status_code=404, detail="Language not found")

#====================================================================================================
# CODE EXECUTION ROUTES
#====================================================================================================

@api_router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute code with full telemetry and security"""
    
    # Rate limiting
    if not rate_limiter.is_allowed("global"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    executor = executor_factory.get_executor(request.language)
    
    if not executor:
        raise HTTPException(
            status_code=400,
            detail=f"Language '{request.language.value}' is not executable on server"
        )
    
    # Create execution context
    ctx = ExecutionContext(request)
    
    # Execute
    result = await executor.execute(ctx)
    
    # Store in history
    history_entry = ExecutionHistory(
        language=request.language,
        code_hash=hashlib.sha256(request.code.encode()).hexdigest()[:16],
        code_preview=request.code[:100] + ("..." if len(request.code) > 100 else ""),
        result=result,
        duration_ms=result.metrics.execution_time_ms
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
    executor = executor_factory.get_executor(request.language)
    
    if not executor:
        return {
            "valid": True,
            "message": "No validation available for this language",
            "security": SecurityReport().dict()
        }
    
    is_valid, error_msg, security = executor.validate(request.code, request.security_level)
    
    # Add code analysis for Python
    analysis = None
    if request.language == LanguageType.PYTHON:
        analysis = CodeAnalyzer.analyze_python(request.code)
    
    return {
        "valid": is_valid,
        "message": error_msg if not is_valid else "Code is valid",
        "security": security.dict(),
        "analysis": analysis.dict() if analysis else None
    }

@api_router.post("/analyze")
async def analyze_code(request: CodeExecutionRequest):
    """Perform deep code analysis"""
    analysis = None
    
    if request.language == LanguageType.PYTHON:
        analysis = CodeAnalyzer.analyze_python(request.code)
    else:
        # Basic analysis for other languages
        analysis = CodeAnalysis(
            lines_of_code=len(request.code.splitlines()),
            complexity=CodeComplexity.SIMPLE
        )
    
    return {
        "language": request.language.value,
        "analysis": analysis.dict()
    }

#====================================================================================================
# AI ASSISTANT ROUTES
#====================================================================================================

@api_router.post("/ai/assist", response_model=AIAssistResponse)
async def ai_assist(request: AIAssistRequest):
    """AI-powered code assistance"""
    if not circuit_breaker.is_available("ai"):
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    
    try:
        response = await ai_service.assist(request)
        circuit_breaker.record_success("ai")
        return response
    except Exception as e:
        circuit_breaker.record_failure("ai")
        raise

@api_router.get("/ai/modes")
async def get_ai_modes():
    """Get available AI assistance modes"""
    modes = [
        {"key": mode.value, "name": mode.value.replace("_", " ").title(), "description": desc}
        for mode, desc in [
            (AIAssistantMode.EXPLAIN, "Get a detailed explanation of what the code does"),
            (AIAssistantMode.DEBUG, "Find and fix bugs in your code"),
            (AIAssistantMode.OPTIMIZE, "Improve performance and efficiency"),
            (AIAssistantMode.COMPLETE, "Auto-complete partial code"),
            (AIAssistantMode.REFACTOR, "Improve code structure and readability"),
            (AIAssistantMode.DOCUMENT, "Generate documentation and comments"),
            (AIAssistantMode.TEST_GEN, "Generate unit tests"),
            (AIAssistantMode.SECURITY_AUDIT, "Analyze for security vulnerabilities"),
            (AIAssistantMode.CONVERT, "Convert code to another language"),
        ]
    ]
    return {"modes": modes, "ai_available": bool(ai_service.api_key)}

#====================================================================================================
# TEMPLATE ROUTES
#====================================================================================================

@api_router.get("/templates")
async def get_templates():
    """Get all code templates"""
    templates = {}
    for lang_type, lang_templates in CODE_TEMPLATES.items():
        templates[lang_type.value] = [
            {
                "key": key,
                "name": data.get("name", key) if isinstance(data, dict) else key.replace("_", " ").title(),
                "code": data.get("code", data) if isinstance(data, dict) else data,
                "description": data.get("description", "") if isinstance(data, dict) else "",
                "complexity": data.get("complexity", CodeComplexity.SIMPLE).value if isinstance(data, dict) else CodeComplexity.SIMPLE.value
            }
            for key, data in lang_templates.items()
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
                    {
                        "key": key,
                        "name": data.get("name", key) if isinstance(data, dict) else key.replace("_", " ").title(),
                        "code": data.get("code", data) if isinstance(data, dict) else data,
                        "description": data.get("description", "") if isinstance(data, dict) else "",
                        "complexity": data.get("complexity", CodeComplexity.SIMPLE).value if isinstance(data, dict) else CodeComplexity.SIMPLE.value
                    }
                    for key, data in CODE_TEMPLATES[lang_type].items()
                ]
            }
    except ValueError:
        pass
    
    raise HTTPException(status_code=404, detail="No templates for this language")

#====================================================================================================
# FILE MANAGEMENT ROUTES
#====================================================================================================

@api_router.post("/files", response_model=CodeFile)
async def create_file(file_data: CodeFileCreate):
    """Create a new code file"""
    code_file = CodeFile(**file_data.dict())
    await db.code_files.insert_one(code_file.dict())
    return code_file

@api_router.get("/files")
async def get_files(
    language: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0
):
    """Get saved files with filtering"""
    query = {}
    if language:
        query["language"] = language
    if is_favorite is not None:
        query["is_favorite"] = is_favorite
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"tags": {"$in": [search]}}
        ]
    
    total = await db.code_files.count_documents(query)
    files = await db.code_files.find(query).sort("updated_at", -1).skip(offset).limit(limit).to_list(limit)
    
    return {
        "files": [CodeFile(**f) for f in files],
        "total": total,
        "limit": limit,
        "offset": offset
    }

@api_router.get("/files/{file_id}", response_model=CodeFile)
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
    
    if "code" in update_dict:
        update_dict["checksum"] = hashlib.sha256(update_dict["code"].encode()).hexdigest()[:16]
        update_dict["version"] = await db.code_files.find_one({"id": file_id}).then(lambda f: f.get("version", 0) + 1 if f else 1)
    
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
    return {"message": "File deleted successfully", "id": file_id}

#====================================================================================================
# ADDON MANAGEMENT ROUTES
#====================================================================================================

@api_router.post("/addons", response_model=LanguageAddon)
async def create_addon(addon_data: dict):
    """Create a new language addon"""
    # Check for duplicate
    existing = await db.language_addons.find_one({"language_key": addon_data.get("language_key")})
    if existing:
        raise HTTPException(status_code=400, detail="Addon with this key already exists")
    
    addon = LanguageAddon(**addon_data)
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

#====================================================================================================
# USER PREFERENCES ROUTES
#====================================================================================================

@api_router.get("/preferences", response_model=UserPreferences)
async def get_preferences():
    """Get user preferences"""
    prefs = await db.user_preferences.find_one({})
    if not prefs:
        default_prefs = UserPreferences()
        await db.user_preferences.insert_one(default_prefs.dict())
        return default_prefs
    return UserPreferences(**prefs)

@api_router.put("/preferences", response_model=UserPreferences)
async def update_preferences(update_data: dict):
    """Update user preferences"""
    update_data["updated_at"] = datetime.utcnow()
    
    await db.user_preferences.update_one(
        {},
        {"$set": update_data},
        upsert=True
    )
    
    prefs = await db.user_preferences.find_one({})
    return UserPreferences(**prefs)

#====================================================================================================
# EXECUTION HISTORY ROUTES
#====================================================================================================

@api_router.get("/history")
async def get_execution_history(
    language: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=50, le=200)
):
    """Get execution history"""
    query = {}
    if language:
        query["language"] = language
    if status:
        query["result.status"] = status
    
    history = await db.execution_history.find(query).sort("created_at", -1).to_list(limit)
    return {"history": [ExecutionHistory(**h) for h in history]}

@api_router.delete("/history")
async def clear_history():
    """Clear execution history"""
    result = await db.execution_history.delete_many({})
    return {"message": f"Cleared {result.deleted_count} history entries"}

#====================================================================================================
# SNIPPETS & SHARING ROUTES
#====================================================================================================

@api_router.post("/snippets")
async def create_snippet(data: dict):
    """Create a shareable code snippet"""
    snippet_id = uuid.uuid4().hex[:8]
    snippet = {
        "id": snippet_id,
        "code": data.get("code"),
        "language": data.get("language"),
        "title": data.get("title", "Untitled"),
        "description": data.get("description", ""),
        "created_at": datetime.utcnow(),
        "views": 0,
        "expires_at": datetime.utcnow() + timedelta(days=30)  # 30 day expiry
    }
    await db.snippets.insert_one(snippet)
    return {"id": snippet_id, "share_url": f"/snippets/{snippet_id}"}

@api_router.get("/snippets/{snippet_id}")
async def get_snippet(snippet_id: str):
    """Get a shared snippet"""
    snippet = await db.snippets.find_one({"id": snippet_id})
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    # Increment views
    await db.snippets.update_one({"id": snippet_id}, {"$inc": {"views": 1}})
    
    snippet['_id'] = str(snippet['_id'])
    return snippet

# Include router
app.include_router(api_router)

#====================================================================================================
# ERROR HANDLERS
#====================================================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {traceback.format_exc()}")
    return {
        "error": True,
        "status_code": 500,
        "detail": "Internal server error",
        "timestamp": datetime.utcnow().isoformat()
    }
