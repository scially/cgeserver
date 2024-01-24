from typing import Generic, Optional, Type, TypeVar, Union
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import engine
from app.db import create_table

create_table()

ModelType = TypeVar("ModelType", bound=BaseModel)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self._model = model

    def get(self, uid: str) -> Optional[ModelType]:
        with Session(engine) as session:
            stmt = select(self._model).where(self._model.uid == uid)
            return session.execute(stmt).first()
        
    def create(self, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, uid: str) -> ModelType:
        obj = db.query(self._model).filter(self._model.uid == uid).first()
        db.delete(obj)
        db.commit()
        return obj