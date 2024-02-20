from fastapi import WebSocket

from abc import ABCMeta
from abc import abstractmethod
import weakref
import json

from app.config import settings

class WebSocketManagerBase(metaclass=ABCMeta):
    @abstractmethod
    async def connect(self, websocket: WebSocket, **args):
        pass

    @abstractmethod
    async def disconnect(self, websocket: WebSocket, **args):
        pass

    @abstractmethod
    async def broadcast_message(self, message: str, websocket: WebSocket = None, **args):
        pass
    
    @abstractmethod        
    async def receive_message(self, websocket: WebSocket, **args):  
        pass      
    
class SignalWebSocketManager(WebSocketManagerBase):
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, **args):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, **args):
        await websocket.close()
        self.active_connections.remove(websocket)

    async def broadcast_message(self, message: str, websocket: WebSocket = None, **args):
        for connection in self.active_connections:
            if connection!= websocket:
                await connection.send_text(message)
                
    async def receive_message(self, websocket: WebSocket, **args):
        data = await websocket.receive_text()
        await self.broadcast_message(data, websocket)

class StreamingWebSocketManager(WebSocketManagerBase):
    '''
        client: web
        server: ue
    '''
    def __init__(self):
        super().__init__()
        
        self.__clients: dict[int, WebSocket] = {}
        self.__client_id: int = 100

        self.__server: WebSocket = None
    
    async def __client_connect(self, websocket: WebSocket):
        if self.__server:
            return
        
        await websocket.accept()
        self.__clients[self.__client_id] = websocket
        self.__client_id += 1
        
        msg = {
            'type': 'palyerCount',
            'count': f'{len(self.__clients)}'
        }
        await self.broadcast_message(json.dumps(msg), type_='client')
        
        config = {
            'type': 'config',
            'peerConnectionOptions': {}
        }
        await websocket.send_text(json.dumps(config)) 
    
    async def connect(self, websocket: WebSocket, **args):
        type_ = args.get('type_', '')
        if type_ == 'client':
            await self.__client_connect(websocket)
        elif type_ =='server':
            await self.__server_connect(websocket)

    async def disconnect(self, websocket: WebSocket, **args):
        pass
    
    async def broadcast_message(self, message: str, websocket: WebSocket = None, **args):
        type_ = args.get('type_', '')
        if type_ == 'client':
            for v in self.__clients.values():
                if v != websocket:
                    v.send_text(message)
        elif type_ =='server':
            if self.__server:
                self.__server.send_text(message)
                
    async def receive_message(self, websocket: WebSocket, **args):  
        type_ = args.get('type_', '')
        if type_ == 'client':
            await self.__client_receive_message(websocket)
        elif type_ =='server':
            await self.__server_receive_message(websocket)
        
    async def __client_receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return
        
        for k, v in self.__clients.items():
            if websocket == v:
                player_id = k
                
        data['player_id'] = player_id
        
        if data['type'] == 'offer':
            await self.__server.send_text(json.dumps(data))
            
        elif data['type'] == 'iceCandidate':
            if settings.SSR_ICE_ENABLE:
                candidate_msg: str = data['candidate']['candidate']
                candidate_msgs = candidate_msg.split(' ')
                candidate_msgs[4] = settings.SSR_HOST
                data['candidate']['candidate'] = ' '.join(candidate_msgs)

            await self.__server.send_text(json.dumps(data))
            
        elif data['type'] == 'stats':
            pass
        elif data['type'] == 'kick':
            for k, v in self.__clients.items():
                if k != player_id:
                    await v.close(1000, 'kicked')
        else:
            return
    
    async def __server_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.__server = websocket
        
    async def __server_receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return
        
        if data['type'] == 'ping':
            msg = {
                'type': 'pong',
                'time': data['time']
            }
            await websocket.send_text(json.dumps(msg))
            return
        
        try:
            player_id = int(data.get('player_id'))
        except (ValueError, TypeError):
            return
        
        player = self.__clients[player_id]
        if player is None:
            return
       
        if data['type'] == 'answer':
            await player.send_text(json.dumps(data))
        elif data['type'] == 'iceCandidate':
            await player.send_text(json.dumps(data))
        elif data['type'] == 'disconnectPlayer':
            await player.close(1011, data['reason'])
        else:
            return