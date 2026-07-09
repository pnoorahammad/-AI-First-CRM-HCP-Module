"""
Database session — uses Supabase HTTPS API (via supabase-py SDK) as the
primary data layer since the direct PostgreSQL host is IPv6-only on this
network. SQLAlchemy engine is kept for Alembic compatibility only.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

from app.core.config import settings


def _build_engine():
    """Build SQLAlchemy engine — uses SQLite locally, Supabase otherwise."""
    if settings.is_sqlite or not settings.DB_PASSWORD:
        engine = create_engine(
            "sqlite:///./crm_local.db",
            connect_args={"check_same_thread": False},
            pool_pre_ping=True,
        )

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()

        return engine

    # Use SQLite as local ORM layer; real data ops go through Supabase SDK
    engine = create_engine(
        "sqlite:///./crm_local.db",
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
    return engine


engine = _build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — provides a local ORM session (schema reference)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_supabase():
    """Return an authenticated Supabase client (service role) for data ops."""
    from supabase import create_client

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def create_tables() -> None:
    """Create local SQLite schema at startup (for ORM type-checking)."""
    from app.models import (
        user,
        hcp,
        interaction,
        interaction_history,
        followup,
        ai_log,
    )  # noqa: F401

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[INFO] create_tables: {e}")
