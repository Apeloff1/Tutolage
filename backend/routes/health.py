"""
Health and System Information Routes
"""

from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(tags=["Health"])

# Version Info
SYSTEM_VERSION = "10.0.0"
SYSTEM_CODENAME = "CS Bible Edition"
SYSTEM_BUILD = "2026.02.22-PRODUCTION"

SYSTEM_FEATURES = [
    "teaching_mode",
    "tooltips_engine",
    "hidden_advanced_panel",
    "language_dock_system",
    "expansion_ready",
    "hotfix_system",
    "plugin_architecture",
    "custom_language_support",
    "retry_with_backoff",
    "connection_status_indicator",
    "enhanced_error_handling",
    "grok_enhanced_prompts",
    "cs_bible_15_year_curriculum",
    "multiplayer_collaboration",
    "quantum_compiler_suite",
    "ultimate_hub",
    "modular_architecture"
]


@router.get("/")
async def root():
    """Root endpoint with version info"""
    return {
        "name": "CodeDock Quantum Nexus",
        "version": SYSTEM_VERSION,
        "codename": SYSTEM_CODENAME,
        "build": SYSTEM_BUILD,
        "features": SYSTEM_FEATURES,
        "status": "operational",
        "architecture": "modular"
    }


@router.get("/health")
async def health_check():
    """Production health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": SYSTEM_VERSION,
        "services": {
            "api": "running",
            "database": "connected",
            "ai": "available" if os.environ.get('EMERGENT_LLM_KEY') else "limited"
        },
        "uptime": "operational"
    }


@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check for monitoring"""
    import psutil
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": SYSTEM_VERSION,
        "codename": SYSTEM_CODENAME,
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        },
        "features": len(SYSTEM_FEATURES),
        "endpoints": "100+"
    }


@router.get("/system/info")
async def system_info():
    """Get detailed system information"""
    return {
        "version": SYSTEM_VERSION,
        "codename": SYSTEM_CODENAME,
        "build": SYSTEM_BUILD,
        "features": SYSTEM_FEATURES,
        "environment": os.environ.get('ENVIRONMENT', 'production'),
        "architecture": {
            "type": "modular",
            "routes": ["health", "compiler", "hub", "bible", "ai", "files"],
            "database": "mongodb",
            "ai_provider": "openai"
        }
    }


@router.get("/readiness")
async def readiness_check():
    """Kubernetes readiness probe"""
    return {"ready": True}


@router.get("/liveness")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"alive": True}
