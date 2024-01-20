from typing import Optional
from . import database
from sqlmodel import SQLModel, Session, Field, select, delete
import uuid

class SSRModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    name: str
    background: Optional[bool] = True
    uepath: Optional[str] = None
    frontpath: Optional[str] = None
    status: bool = False

def create_ssr(model: SSRModel) -> SSRModel:
    with Session() as session:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

def get_ssr(uid: str) -> SSRModel:
    with Session(database.DATABASE_ENGINE) as session:
        statement = select(SSRModel).where(SSRModel.uid == uid)
        results = session.exec(statement)
        return results.first()

def delete_ssr(uid: str) -> SSRModel:
    with Session(database.DATABASE_ENGINE) as session:
        statement = delete(SSRModel).where(SSRModel.uid == uid)
        results = session.exec(statement)
        return results.first()

def list_ssr() -> list[SSRModel]:
    with Session(database.DATABASE_ENGINE) as session:
        statement = select(SSRModel)
        results = session.exec(statement)
        return results.all()