# app/core/database.py
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Use the clean property from config
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Dependency-injected DB session
def get_session() -> Session:
    with Session(engine) as session:
        yield session

# Initialize tables (called at app startup)
def init_db() -> None:
    from app.models import user # ensures all models are loaded for metadata
    SQLModel.metadata.create_all(bind=engine)