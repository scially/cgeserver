from .base import CRUDBase
from typing import Optional
from app.model import SSRModel
from sqlmodel import Session
from sqlmodel import select
from app.db.engine import engine

class SSRCRUD(CRUDBase[SSRModel]):
    def __init__(self):
        super().__init__(SSRModel)

    def list(self, db: Session) -> list[SSRModel]:
        statement = select(SSRModel)
        results = db.exec(statement=statement)
        return results.all()

class SSRModelCache:
    def __init__(self, session: Session):
        self._ssr_crud = SSRCRUD()
        self._session = session
        self._cache: dict[str, SSRModel] = dict()
        for v in self._ssr_crud.list(self._session):
            self._cache[v.uid] = v
            
    def get(self, uid: str) -> Optional[SSRModel]:
        hit_value = self._cache.get(uid)
        return hit_value
    
    def delete(self, uid: str) -> None:
        hit_value = self._cache.get(uid)
        self._ssr_crud.delete(self._session, uid)
        del self._cache[uid]
    
    def add(self, model: SSRModel) -> SSRModel:
        model = self._ssr_crud.create(self._session, model)
        self._cache[model.uid] = model
        return model
    
    def update(self, model: SSRModel) -> None:
        self._cache[model.uid] = model
        self._ssr_crud.update(self._session, model)

    def values(self)-> list[SSRModel]:
        return self._cache.values()

Caches = SSRModelCache(Session(engine))
