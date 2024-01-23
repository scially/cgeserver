from sqlmodel import Session, select, delete, update
from app.model import SSRModel
from typing import Optional, Dict, List
from fastapi import Depends

def create_ssr(session: Session, model: SSRModel) -> SSRModel:
    session.add(model)
    session.commit()
    session.refresh(model)
    return model
        

def get_ssr(session: Session, uid: str) -> SSRModel:
    statement = select(SSRModel).where(SSRModel.uid == uid)
    results = session.exec(statement)
    return results.first()
        

def delete_ssr(session: Session, uid: str) -> SSRModel:
    statement = delete(SSRModel).where(SSRModel.uid == uid)
    results = session.exec(statement)
    return results.first()
       

def list_ssr(session: Session) -> list[SSRModel]:
    statement = select(SSRModel)
    results = session.exec(statement)
    return results.all()
        
    
def update_ssr(session: Session, model: SSRModel) -> SSRModel:
    statement = (
            update(SSRModel)
           .where(SSRModel.uid == model.uid)
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
    def __init__(self, session: Session = Depends(Session)):
        self._cache: Dict[str, SSRModel] = dict()
        for v in list_ssr(session):
            self._cache[v.uid] = v
            
    def get(self, uid: str) -> Optional[SSRModel]:
        hit_value = self._cache.get(uid)
        return hit_value
    
    def delete(self, uid: str, db_operate: bool = True) -> None:
        hit_value = self._cache.get(uid)
        if hit_value is not None and db_operate:
            delete_ssr(uid)
        del self._cache[uid]
    
    def add(self, model: SSRModel) -> SSRModel:
        model = create_ssr(model)
        self._cache[model.uid] = model
        return model
    
    def update(self, model: SSRModel, db_operate: bool = True) -> None:
        self._cache[model.uid] = model
        if db_operate:
            update_ssr(model)
            
    def values(self)-> List[SSRModel]:
        return self._cache.values()
    

Caches = SSRModelCache()
