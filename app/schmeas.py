from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from app.models import UserRole

class UserBaseSchema(BaseModel):
    username: str
    password: str
    
class UserInfoSchema(BaseModel):
    name: str = Field(default='')
    username: str
    role: UserRole
    created_at: datetime