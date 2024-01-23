from sqlmodel import create_engine
from sqlalchemy import Engine
from app.config import settings
from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session

def init_engine() -> Engine:
    engine = create_engine(settings.DATABASE_URL, echo=settings.PRODUCTION)
    return engine

engine = init_engine()

def create_table():
    from app import model
    from sqlmodel import SQLModel
    # muset be called after import all SQLModel class
    SQLModel.metadata.create_all(engine)

create_table()

def get_db() -> Generator:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]