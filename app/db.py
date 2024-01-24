from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from app.config import settings

def init_engine() -> Engine:
    engine = create_engine(settings.DATABASE_URL, echo=settings.PRODUCTION)
    return engine

engine = init_engine()

def create_table():
    from app import models
    # muset be called after import all Base class
    models.Base.metadata.create_all(engine)