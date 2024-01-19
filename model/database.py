from pathlib import Path
from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine
from .ssr import SSRModel as SSRModel

DATABASE_NAME = "cgeserver.db"
__need_create_table: bool = not Path(DATABASE_NAME).exists()
__sqlite_url = f"sqlite:///{DATABASE_NAME}"
    
DATABASE_ENGINE: Engine = create_engine(__sqlite_url)

if __need_create_table:
    SQLModel.metadata.create_all(DATABASE_ENGINE)