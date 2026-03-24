"""
Pytest Configuration and Fixtures for CodeDock Backend Tests
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Import the FastAPI app
import sys
sys.path.insert(0, '/app/backend')
from server import app


# ============================================================================
# Pytest Configuration
# ============================================================================

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Client Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Create a synchronous test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an asynchronous test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_npc_request() -> dict:
    """Sample NPC generation request."""
    return {
        "description": "A wise old wizard with a mysterious past",
        "include_dialogue": True,
        "include_quests": True,
        "complexity_level": "moderate"
    }


@pytest.fixture
def sample_combat_request() -> dict:
    """Sample combat system generation request."""
    return {
        "style": "turn_based",
        "include_magic": True,
        "include_status_effects": True,
        "party_based": True,
        "enemy_ai_complexity": "moderate"
    }


@pytest.fixture
def sample_animation_request() -> dict:
    """Sample animation generation request."""
    return {
        "description": "humanoid character walking",
        "looping": True,
        "include_root_motion": True
    }


@pytest.fixture
def sample_cocoding_request() -> dict:
    """Sample co-coding session request."""
    return {
        "user_id": "test_user_123",
        "pipeline": "npc",
        "initial_prompt": "Create a friendly merchant NPC",
        "skill_level": "intermediate"
    }


@pytest.fixture
def sample_user_state() -> dict:
    """Sample learner state for matrix application."""
    return {
        "retention_rate": 0.65,
        "cognitive_load": 0.72,
        "time_since_review_hours": 48,
        "skill_level": "intermediate"
    }


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def api_base_url() -> str:
    """Base URL for API endpoints."""
    return "/api"
