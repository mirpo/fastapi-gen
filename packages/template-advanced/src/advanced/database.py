from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from advanced.config import settings

# Database setup - SQLite for simplicity, see Settings.database_url
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
