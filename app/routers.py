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
    r.data = Caches.add(ssr_model)
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
    r.data = Caches.get(uid)
    r.status = 200
    r.msg = "get ssr success"
    return r

@router.post("/ssr/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str) -> ResponseModel[str]:
    ssr_model = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_model is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_model.status is True:
        r.msg = 'ssr is running'
        r.status = 200
        return r

@router.post("/ssr/stop/{uid}", response_model=ResponseModel[str])
async def run(uid: str) -> ResponseModel[str]:
    ssr_model = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_model is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_model.status is True:
        r.msg = 'ssr is running'
        r.status = 200
        return r
    
@router.websocket("/streamingserver/{uid}")
async def server_websocket_endpoint(websocket: WebSocket, uid: str):
    manager = server_manager[uid]
    if manager is None:
        server_manager[uid] = WebSocketManager()
    manager = server_manager[uid]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/streamingclient/{uid}")
async def client_websocket_endpoint(websocket: WebSocket, uid: str):
    manager = client_manager[uid]
    if manager is None:
        client_manager[uid] = WebSocketManager()
    manager = client_manager[uid]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)