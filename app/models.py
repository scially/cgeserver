from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

import uuid 

class Base(DeclarativeBase):
    pass

class SSR(Base):
    _tablename__ = "ssr"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(unique=True, index=True, default_factory=uuid.uuid4)
    name: Mapped[str]
    background: Mapped[bool] = mapped_column(default=True)
    uepath: Mapped[str] = mapped_column(default="")
    frontpath: Mapped[str] = mapped_column(default="")
    xresolution: Mapped[int] = mapped_column(default=1920)
    yresolution: Mapped[int] = mapped_column(default=1080)