from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from app.ws import WebSocketManager

import uuid 

class SSRModel(SQLModel, table=True):
    uid: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    background: bool = Field(default=True)
    uepath: Optional[str] = Field(default="")
    frontpath: Optional[str] = Field(default="")
    xresolution: int = Field(default=1920)
    yresolution: int = Field(default=1080)
    
    client_manager: WebSocketManager = Field(default_factory=WebSocketManager)
    server_manager: WebSocketManager = Field(default_factory=WebSocketManager)