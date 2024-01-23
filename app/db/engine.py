from sqlmodel import create_engine
from sqlalchemy import Engine
from app.config import settings

def create_engine() -> Engine:
    engine = create_engine(settings.DATABASE_URL, echo=settings.PRODUCTION)
    return engine

engine = create_engine()
