from fastapi import WebSocket

from abc import ABC 
from abc import abstractmethod

class WebSocketManagerBase(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket):
        pass

    @abstractmethod
    def disconnect(self, websocket: WebSocket):
        pass

    @abstractmethod
    async def broadcast_message(self, message: str, websocket: WebSocket = None):
        pass
    
    @abstractmethod        
    async def receive_message(self, websocket: WebSocket):  
        pass      
    
class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    @abstractmethod
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_message(self, message: str, websocket: WebSocket = None):
        for connection in self.active_connections:
            if connection!= websocket:
                await connection.send_text(message)
                
    async def receive_message(self, websocket: WebSocket):  
        pass      
       
    
class SignalWebSocketManager(WebSocketManager):
    async def receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        await self.broadcast_message(data, websocket)


class StreamingWebSocketManager(WebSocketManager):
    async def receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        await self.broadcast_message(data, websocket)