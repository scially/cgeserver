from typing import TypeVar, Generic
from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass(init=False)
class ResponseModel(BaseModel, Generic[T]):
    msg: str = ""
    data: Optional[T] = None
    status: int = 200