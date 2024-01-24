from pydantic import BaseModel
from pydantic.fields import PrivateAttr

class SSRBase(BaseModel):
    name: str
    background: bool = True
    uepath: str = ""
    frontpath: str = ""
    xresolution: int = 1920
    yresolution: int = 1080

class SSRCreate(SSRBase):
    pass


class SSR(SSRBase):
    id: int 
    uid: str
    
    class Config:
        orm_mode = True