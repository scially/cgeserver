from sqlmodel import Session, select, delete, update
from app.model import ssr
from typing import Optional, Dict, List
from . import DATABASE_ENGINE

def create_ssr(model: ssr.SSRModel) -> ssr.SSRModel:
    with Session() as session:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

def get_ssr(uid: str) -> ssr.SSRModel:
    with Session(DATABASE_ENGINE) as session:
        statement = select(ssr.SSRModel).where(ssr.SSRModel.uid == uid)
        results = session.exec(statement)
        return results.first()

def delete_ssr(uid: str) -> ssr.SSRModel:
    with Session(DATABASE_ENGINE) as session:
        statement = delete(ssr.SSRModel).where(ssr.SSRModel.uid == uid)
        results = session.exec(statement)
        return results.first()

def list_ssr() -> list[ssr.SSRModel]:
    with Session(DATABASE_ENGINE) as session:
        statement = select(ssr.SSRModel)
        results = session.exec(statement)
        return results.all()
    
def update_ssr(model: ssr.SSRModel) -> ssr.SSRModel:
    with Session(DATABASE_ENGINE) as session:
        statement = (
            update(ssr.SSRModel)
           .where(ssr.SSRModel.uid == model.uid)
           .values(
                name=model.name,
                background=model.background,
                uepath=model.uepath,
                frontpath=model.frontpath,
                status=model.status
            )
        )
        results = session.exec(statement)
        return results.first()
 
   
class SSRModelCache:
    def __init__(self):
        self._cache: dict[str, ssr.SSRModel] = dict()
        for v in list_ssr():
            self._cache[v.uid] = v
            
    def get(self, uid: str) -> Optional[ssr.SSRModel]:
        hit_value = self._cache.get(uid)
        return hit_value
    
    def delete(self, uid: str, db_operate: bool = True) -> None:
        hit_value = self._cache.get(uid)
        if hit_value is not None and db_operate:
            delete_ssr(uid)
        del self._cache[uid]
    
    def add(self, model: ssr.SSRModel) -> ssr.SSRModel:
        model = create_ssr(model)
        self._cache[model.uid] = model
        return model
    
    def update(self, model: ssr.SSRModel, db_operate: bool = True) -> None:
        self._cache[model.uid] = model
        if db_operate:
            update_ssr(model)
            
    def values(self)-> List[ssr.SSRModel]:
        return self._cache.values()
    
Caches = SSRModelCache()