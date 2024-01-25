from typing import Generic, Optional, Type, TypeVar
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import select

from app.db import engine
from app.models import SSRModel

ModelType = TypeVar("ModelType", bound=SQLModel)

class SQLModelPlus(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLModel model class
        """
        self._model = model

    def get(self, uid: str) -> Optional[ModelType]:
        with Session(engine) as session:
            obj = session.get(self._model, uid)
            return obj
        
    def create(self, obj: ModelType) -> ModelType:
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def update(self, obj: ModelType) -> ModelType:
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, uid: str) -> ModelType:
        with Session(engine) as session:
            obj = session.get(self._model, uid)
            session.delete(obj)
            session.commit()
            return obj


class SSRCRUD(SQLModelPlus[SSRModel]):
    def __init__(self):
        super().__init__(SSRModel)

    def list(self) -> list[SSRModel]:
        with Session(engine) as session:
            statement = select(SSRModel)
            results = session.exec(statement=statement)
            return results.all()

class SSRModelCache:
    def __init__(self):
        self._ssr_crud = SSRCRUD()
        self._cache: dict[str, SSRModel] = dict()
        for v in self._ssr_crud.list():
            self._cache[v.uid] = v
            
    def get(self, uid: str) -> Optional[SSRModel]:
        hit_value = self._cache.get(uid)
        return hit_value
    
    def delete(self, uid: str) -> None:
        hit_value = self._cache.get(uid)
        self._ssr_crud.delete(uid)
        del self._cache[uid]
    
    def add(self, model: SSRModel) -> SSRModel:
        model = self._ssr_crud.create(model)
        self._cache[model.uid] = model
        return model
    
    def update(self, model: SSRModel) -> None:
        self._cache[model.uid] = model
        self._ssr_crud.update(model)

    def values(self)-> list[SSRModel]:
        return self._cache.values()

Caches = SSRModelCache(Session(engine))
