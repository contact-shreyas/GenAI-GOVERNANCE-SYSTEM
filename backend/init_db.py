"""
Initialize SQLite database for local development.
Creates tables if they don't exist.
"""

from models import Base
from db import engine

if __name__ == "__main__":
    print("Initializing SQLite database...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully!")
    print("  Database: genai_governance.db")
    print("  Tables: policies, ai_use_logs")
