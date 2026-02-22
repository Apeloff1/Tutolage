"""
Database connection and utilities for CodeDock
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_URL, DB_NAME, MONGO_POOL_CONFIG

# MongoDB Client with production-optimized pooling
client = AsyncIOMotorClient(MONGO_URL, **MONGO_POOL_CONFIG)
db = client[DB_NAME]

# Collection references
files_collection = db.files
addons_collection = db.addons
preferences_collection = db.preferences
history_collection = db.history
snippets_collection = db.snippets
sessions_collection = db.sessions

async def health_check() -> bool:
    """Check database connectivity"""
    try:
        await client.admin.command('ping')
        return True
    except Exception:
        return False

async def get_collection_stats() -> dict:
    """Get statistics about collections"""
    return {
        "files": await files_collection.count_documents({}),
        "addons": await addons_collection.count_documents({}),
        "snippets": await snippets_collection.count_documents({}),
        "sessions": await sessions_collection.count_documents({})
    }
