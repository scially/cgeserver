from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

import uuid 

class SSRModel(SQLModel, table=True):
    uid: Optional[int] = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str
    background: bool = Field(default=True)
    uepath: Optional[str] = Field(default="")
    frontpath: Optional[str] = Field(default="")
    xresolution: int = Field(default=1920)
    yresolution: int = Field(default=1080)