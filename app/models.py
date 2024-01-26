from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from app.ws import WebSocketManager
from app.config import settings

from pathlib import Path
import logging
import uuid
from subprocess import Popen

logger = logging.Logger(__name__)

class SSRModel(SQLModel, table=True):
    uid: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    background: bool = True
    uepath: str = ""
    frontpath: str = ""
    xresolution: int = Field(default=1920)
    yresolution: int = Field(default=1080)

class SSRModelInstance:
    def __init__(self, model: SSRModel):
        self._model = model
        self._status: bool = False
        self._client_manager: WebSocketManager = WebSocketManager()
        self._server_manager: WebSocketManager = WebSocketManager()

        self._process: Popen = None
        
    @property
    def model(self) -> SSRModel:
        return self._model
    
    @property
    def client_manager(self) -> WebSocketManager:
        return self._client_manager
    
    @property
    def server_manager(self) -> WebSocketManager:
        return self._server_manager
    
    @property
    def status(self) -> bool: 
        return self._status
    
    @status.setter
    def status(self, sta: bool):
        self._status = sta
        return self
    
    def run(self) -> bool:
        if self.model.uepath != '' and Path(self.model.uepath).exists() and not self.status:
            cmds = [self.model.uepath,
                    "-AudioMixer", 
                    "-NoTextureStreaming", 
                    "-binnedmalloc3", 
                    "-AllowPixelStreamingCommands", 
                    f"-PixelStreamingURL=ws://127.0.0.1:{settings.PORT}/client/{self.model.uid}", 
                    f"-ws=ws://127.0.0.1:{settings.PORT}/message/{self.model.uid}"]
            
            if self.model.background:
                cmds = cmds + ["-RenderOffScreen", "-ForceRes"]
            
            cmds = cmds + [f"-ResX={self.model.xresolution}", f"-Resy={self.model.xresolution}"]
            cmds = cmds + ["-NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52"]
            self._process = Popen(cmds)
            
            logger.info("[Render] Render Start: %s", ' '.join(cmds))
            return True
        
        return False

    def stop(self) -> None:
        if self._process != None:
            self._process.kill()