from enum import Enum
from enum import unique

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.ws import WebSocketManager
from app.crud import Caches
from app.response import ResponseModel
from app.models import SSRModel

router = APIRouter()

@router.post("/ssr/add", response_model=ResponseModel[SSRModel])
async def add(ssr_model: SSRModel) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.add(ssr_model).model
    r.status = 200
    r.msg = "create ssr success"
    return r
    
@router.get("/ssr/list", response_model=ResponseModel[list[SSRModel]])
async def list() -> ResponseModel[list[SSRModel]]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.values()
    r.status = 200
    r.msg = "list ssr success"
    return r

@router.get("/ssr/get/{uid}", response_model=ResponseModel[SSRModel])
async def get(uid: str) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    ssr_instance = Caches.get(uid)
    r.data = ssr_instance.model if ssr_instance else None
    r.status = 200
    r.msg = "get ssr success"
    return r

@router.post("/ssr/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str) -> ResponseModel[str]:
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
        ssr_instance.run()
        r.msg = "ssr start succeess"
        r.status = 200
        return r

@router.post("/ssr/stop/{uid}", response_model=ResponseModel[str])
async def stop(uid: str) -> ResponseModel[str]:
    ssr_instance = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_instance is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_instance.status == True:
        ssr_instance.stop()
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
        
@router.websocket("/streaming/{origin}/{uid}")
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