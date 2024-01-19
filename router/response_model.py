from typing import TypeVar, Generic
from pydantic import BaseModel
from typing import Optional

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    msg: str = ""
    data: Optional[T] = None
    status: int = 200