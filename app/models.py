from typing import Optional
from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.routing import Mount

from app.ws import WebSocketManagerBase
from app.ws import StreamingWebSocketManager
from app.ws import SignalWebSocketManager
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
        self.__model = model
        self.__status: bool = False
        self.__ssr_manager: WebSocketManagerBase = StreamingWebSocketManager()
        self.__signal_manager: WebSocketManagerBase = SignalWebSocketManager()
        self.__process: Popen = None
        
    @property
    def model(self) -> SSRModel:
        return self.__model
    
    @property
    def ssr_manager(self) -> WebSocketManagerBase:
        return self.__ssr_manager
    
    @property
    def signal_manager(self) -> WebSocketManagerBase:
        return self.__signal_manager
    
    @property
    def status(self) -> bool: 
        return self.__status
    
    @status.setter
    def status(self, sta: bool):
        self.__status = sta
        return self
    
    def run(self, app: FastAPI) -> bool:
        ue_result: bool = False
        front_result: bool = False
        
        if self.model.uepath != '' and Path(self.model.uepath).exists() and not self.__process:
            cmds = [self.model.uepath,
                    "-AudioMixer", 
                    "-NoTextureStreaming", 
                    "-binnedmalloc3", 
                    "-AllowPixelStreamingCommands", 
                    f"-PixelStreamingURL=ws://127.0.0.1:{settings.PROJECT_PORT}/ws/streaming/server/{self.model.uid}", 
                    f"-ws=ws://127.0.0.1:{settings.PROJECT_PORT}/ws/streaming/signal/{self.model.uid}"]
            
            if self.model.background:
                cmds = cmds + ["-RenderOffScreen", "-ForceRes"]
            
            cmds = cmds + [f"-ResX={self.model.xresolution}", f"-Resy={self.model.xresolution}"]
            cmds = cmds + ["-NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52"]
            self.__process = Popen(cmds)
            
            logger.info("[Render] Render Start: %s", ' '.join(cmds))
            
            ue_result = True

        if self.model.frontpath != '' and Path(self.model.frontpath).exists():
            app.mount(f"/static/{self.model.uid}", StaticFiles(directory=self.model.frontpath), str(self.model.uid))
            
            front_result =True
            
        self.status = ue_result or front_result
        return self.status

    def stop(self, app:FastAPI) -> bool:
        # umount self static mount
        for index, route in enumerate(app.routes):
            if isinstance(route, Mount) and route.name == str(self.model.uid):
                del app.routes[index]
                break
            
        if self.__process != None:
            self.__process.kill()
            self.__process.wait()
            self.__process = None
        
        self.status = False
        return True