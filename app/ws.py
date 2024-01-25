from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws/signalstreaming")

class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
            
client_manager: dict[str, WebSocketManager] = {}
server_manager: dict[str, WebSocketManager] = {}

@router.websocket("/server/{ssr_id}")
async def server_websocket_endpoint(websocket: WebSocket, ssr_id: str):
    if server_manager.get(ssr_id) is None:
        server_manager[ssr_id] = WebSocketManager()
    manager = server_manager[ssr_id]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
@router.websocket("/client/{ssr_id}")
async def client_websocket_endpoint(websocket: WebSocket, ssr_id: str):
    if client_manager.get(ssr_id) is None:
        client_manager[ssr_id] = WebSocketManager()
    manager = client_manager[ssr_id]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)