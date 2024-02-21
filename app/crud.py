from typing import Generic, Optional, Type, TypeVar
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import select

from app.db import engine
from app.db import create_table
from app.models import SSRModel
from app.models import SSRModelInstance
from uuid import UUID

create_table()

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
            obj = session.get(self._model, UUID(uid))
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
            obj = session.get(self._model, UUID(uid))
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
        self._cache: dict[str, SSRModelInstance] = dict()

    def get(self, uid: str) -> Optional[SSRModelInstance]:
        hit_value = self._cache.get(uid)
        if hit_value == None:
            hit_value = self._ssr_crud.get(uid)
            if hit_value == None:
                return None
            else:
                self._cache[uid] = SSRModelInstance(hit_value)
        return self._cache[uid]
    
    def delete(self, uid: str) -> None:
        hit_value = self._cache.get(uid)
        if hit_value:
            self._ssr_crud.delete(uid)
            del self._cache[uid]
    
    def add(self, model: SSRModel) -> SSRModelInstance:
        model = self._ssr_crud.create(model)
        self._cache[str(model.uid)] = SSRModelInstance(model)
        return self._cache[str(model.uid)]
    
    def update(self, model: SSRModel) -> SSRModelInstance:
        old = self._ssr_crud.get(str(model.uid))
        
        old.name = model.name
        old.background = model.background
        old.frontpath = model.frontpath
        old.uepath = model.uepath
        old.xresolution = model.xresolution
        old.yresolution = model.yresolution
        model = self._ssr_crud.update(old)
        self._cache[str(model.uid)] = SSRModelInstance(model)
        return self._cache[str(model.uid)]
    
    def values(self)-> list[SSRModel]:
        return self._ssr_crud.list()

Caches = SSRModelCache()