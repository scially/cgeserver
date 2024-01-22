from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine
from app.model import *

global DATABASE_NAME
global DATABASE_URL
global DATABASE_ENGINE

DATABASE_NAME: str      = "cgeserver.db"
DATABASE_URL: str       = f"sqlite:///{DATABASE_NAME}"
DATABASE_ENGINE: Engine  = None

def init_database(product:bool = False):
    from ..model import ssr
    global DATABASE_ENGINE
    DATABASE_ENGINE = create_engine(DATABASE_URL, echo=product)
    SQLModel.metadata.create_all(DATABASE_ENGINE)

init_database(True)
from . import ssr as ssr