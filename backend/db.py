"""
Database setup: SQLAlchemy engine and session management.
Supports both SQLite (local development) and PostgreSQL (production).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

# Auto-detect SQLite vs PostgreSQL and set appropriate options
engine_kwargs = {}
if "sqlite" in settings.database_url.lower():
    # SQLite: no connection pooling needed
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": None,
    }
else:
    # PostgreSQL: use connection pooling
    engine_kwargs = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
    }

engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency yielding a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
