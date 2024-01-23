from typing import Generic, Optional, Type, TypeVar, Union
from sqlmodel import SQLModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=SQLModel)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self._model = model

    def get(self, db: Session, uid: str) -> Optional[ModelType]:
        return db.query(self._model).filter(self._model.uid == uid).first()

    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, uid: str) -> ModelType:
        obj = db.query(self._model).filter(self._model.uid == uid).first()
        db.delete(obj)
        db.commit()
        return obj