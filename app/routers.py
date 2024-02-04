from enum import Enum
from enum import unique
from datetime import datetime
from datetime import timedelta

from fastapi import status
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel

from jose import JWTError, jwt

from app.crud import Caches
from app.crud import UserCRUD
from app.response import ResponseModel
from app.models import SSRModel
from app.models import UserModel
from app.models import UserRole
from app.schmeas import UserInfoSchema
from app.schmeas import UserBaseSchema
from app.config import settings

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/token")
api_router = APIRouter(prefix="/api")
ws_router  = APIRouter(prefix="/ws")

router = (api_router, ws_router)

class Token(BaseModel):
    access_token: str
    token_type: str
    
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2)) -> UserInfoSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserCRUD().get_by_name(username)
    if user is None:
        raise credentials_exception
    return UserInfoSchema(
        name=user.name,
        username=user.username,
        role=user.role
        created_at=user.created_at
    )
    
@api_router.post("/ssr/add", response_model=ResponseModel[SSRModel])
async def add(ssr_model: SSRModel, user: UserInfoSchema = Depends(get_current_user)) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.add(ssr_model).model
    r.status = 200
    r.msg = "create ssr success"
    return r

@api_router.get("/ssr/list", response_model=ResponseModel[list[SSRModel]])
async def list() -> ResponseModel[list[SSRModel]]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.values()
    r.status = 200
    r.msg = "list ssr success"
    return r

@api_router.get("/ssr/get/{uid}", response_model=ResponseModel[SSRModel])
async def get(uid: str) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    ssr_instance = Caches.get(uid)
    r.data = ssr_instance.model if ssr_instance else None
    r.status = 200
    r.msg = "get ssr success"
    return r

@api_router.post("/ssr/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str, req: Request) -> ResponseModel[str]:
    ssr_instance = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_instance is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_instance.status is True:
        r.msg = 'ssr is running'
        r.status = 200
        return r
    else:
        ssr_instance.run(req.app)
        r.msg = "ssr start succeess"
        r.status = 200
        return r

@api_router.post("ssr/stop/{uid}", response_model=ResponseModel[str])
async def stop(uid: str, req: Request) -> ResponseModel[str]:
    ssr_instance = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_instance is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_instance.status == True:
        ssr_instance.stop(req.app)
        r.msg = 'ssr stop successed'
        r.status = 200
        return r
    else:
        r.msg = "ssr has stoped"
        r.status = 200
        return r

@unique
class StreamingServerOrigin(str, Enum):
    client = 'client'
    server = 'server'
        
@ws_router.websocket("/streaming/{origin}/{uid}")
async def server_websocket_endpoint(websocket: WebSocket, origin: StreamingServerOrigin,uid: str):
    ssr_instance = Caches.get(uid)
    if ssr_instance == None or ssr_instance.status == False:
        return
    
    manager = ssr_instance.server_manager[uid] if origin == StreamingServerOrigin.server else ssr_instance.client_manager
    
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
@api_router.post('/token')
async def user_login(form_data: OAuth2PasswordRequestForm=Depends()):
    user = UserCRUD().get_by_name(form_data.username)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="invalid username or password")
    else:
        access_token = create_access_token(
            data={"username": user.username}
            )

        return {"access_token": access_token, "token_type": "bearer"}