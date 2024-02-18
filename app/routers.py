from enum import Enum
from enum import unique
from typing import Annotated

from datetime import datetime
from datetime import timedelta
from fastapi import APIRouter
from fastapi import Body
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import Request
from app.crud import Caches

from app.response import ResponseModel
from app.models import SSRModel

api_router = APIRouter(prefix="/api")
ws_router  = APIRouter(prefix="/ws")

router = (api_router, ws_router)

@api_router.post("/ssr/add", response_model=ResponseModel[SSRModel])
async def add(ssr_model: SSRModel) -> ResponseModel[SSRModel]:
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

@api_router.get("/ssr/status", response_model=ResponseModel[bool])
async def status(uid: str) -> ResponseModel[bool]:
    r: ResponseModel[bool] = ResponseModel()
    ssr_instance = Caches.get(uid)
    r.data = ssr_instance.status
    r.status = 200
    r.msg = "get ssr status success"
    return r

@api_router.get("/ssr/get", response_model=ResponseModel[SSRModel])
async def get(uid: str) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    ssr_instance = Caches.get(uid)
    r.data = ssr_instance.model if ssr_instance else None
    r.status = 200
    r.msg = "get ssr success"
    return r

@api_router.post('/ssr/delete', response_model=ResponseModel[str])
async def delete(uid: Annotated[str, Body(embed=True)], req: Request):
    ssr_instance = Caches.get(uid)
    ssr_instance.stop(req.app)
    
    Caches.delete(uid)
    r: ResponseModel[str] = ResponseModel()
    ssr_instance = Caches.get(uid)
    r.data = None
    r.status = 200
    r.msg = "delete ssr success"
    return r

@api_router.post("/ssr/start", response_model=ResponseModel[str])
async def start(uid: Annotated[str, Body(embed=True)], req: Request) -> ResponseModel[str]:
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

@api_router.post("ssr/stop", response_model=ResponseModel[str])
async def stop(uid: Annotated[str, Body(embed=True)], req: Request) -> ResponseModel[str]:
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