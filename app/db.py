from sqlmodel import create_engine
from sqlmodel import SQLModel
from app.config import settings

def init_engine():
    engine = create_engine(settings.DATABASE_URL, echo=settings.PRODUCTION != 'production')
    return engine

engine = init_engine()

def create_table():
    from app import models
    # muset be called after import all Base class
    SQLModel.metadata.create_all(engine)