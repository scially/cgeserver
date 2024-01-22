from typing import Optional, Dict, List
import uuid
import subprocess
import logging
from pathlib import Path
from sqlmodel import SQLModel, Session, Field, select, delete, update
from pydantic.fields import PrivateAttr
import main
from . import database

logger = logging.getLogger(__name__)

class SSRModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    name: str
    background: Optional[bool] = True
    uepath: Optional[str] = None
    frontpath: Optional[str] = None
    status: bool = False
    xresolution: int = 1920
    yresolution: int = 1080
    
    _process: subprocess.Popen = PrivateAttr(None)
    
    def run(self) -> bool:
        if Path(self.uepath).exists() and not self.status:
            cmds = [self.uepath,
                    "-AudioMixer", 
                    "-NoTextureStreaming", 
                    "-binnedmalloc3", 
                    "-AllowPixelStreamingCommands", 
                    f"-PixelStreamingURL=ws://127.0.0.1:{PORT}/client/{self.uid}", 
                    f"-ws=ws://127.0.0.1:{PORT}/message/{self.uid}"]
            if self.background:
                cmds = cmds + ["-RenderOffScreen", "-ForceRes"]
            
            cmds = cmds + [f"-ResX={self.xresolution}", f"-Resy={self.xresolution}"]
            cmds = cmds + ["-NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52"]
            self._process = subprocess.Popen(cmds)
            logger.info("[Render] Render Start: %s", ' '.join(cmds))
            return True
        
        return False

    def stop(self) -> None:
        if self._process is not None:
            self._process.kill()

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
    
def update_ssr(model: SSRModel) -> SSRModel:
    with Session(database.DATABASE_ENGINE) as session:
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
    def __init__(self):
        self._cache:Dict[str, SSRModel] = dict()
        for v in list_ssr():
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