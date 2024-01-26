from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from app.ws import WebSocketManager

import uuid 

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
        pass
    
    def stop(self) -> None:
        pass