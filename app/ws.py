from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from abc import ABCMeta
from abc import abstractmethod
import logging
import json

from app.config import settings

logger = logging.Logger(__name__)

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
        # await websocket.close()
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
        if not self.__server or self.__server.application_state != WebSocketState.CONNECTED:
            return
        
        await websocket.accept()
        self.__clients[self.__client_id] = websocket
        self.__client_id += 1
        
        msg = {
            'type': 'playerCount',
            'count': len(self.__clients)
        }
        await self.broadcast_message(json.dumps(msg), websocket, type_='client')
        
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
        type_ = args.get('type_', '')
        if type_ == 'client':
            await self.__client_disconnect(websocket)
        elif type_ =='server':
            await self.__server_disconnect(websocket)
    
    async def __client_disconnect(self, websocket: WebSocket):
        for k, v in self.__clients.items():
            if v == websocket:
                # await v.close()
                del self.__clients[k]
                break
        
    async def __server_disconnect(self, websocket: WebSocket):
        # await websocket.close()
        self.__server = None
        
    async def broadcast_message(self, message: str, websocket: WebSocket, **args):
        type_ = args.get('type_', '')
        if type_ == 'client':
            for v in self.__clients.values():
                if v != websocket:
                    await v.send_text(message)
        elif type_ =='server':
            if self.__server:
                await self.__server.send_text(message)
                
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
                break
                
        data['playerId'] = player_id
        
        if data['type'] == 'offer':
            msg = json.dumps(data)
            await self.__server.send_text(msg)
            
        elif data['type'] == 'iceCandidate':
            if settings.SSR_ICE_ENABLE:
                candidate_msg: str = data['candidate']['candidate']
                candidate_msgs = candidate_msg.split(' ')
                candidate_msgs[4] = settings.SSR_HOST
                data['candidate']['candidate'] = ' '.join(candidate_msgs)

            await websocket.send_text(json.dumps(data))
            
        elif data['type'] == 'stats':
            logger.info(f'[Player] <- {player_id} stats: {data}')
            
        elif data['type'] == 'kick':
            for k, v in self.__clients.items():
                if k != player_id:
                    await v.close(1000, 'kicked')
        else:
            return
    
    async def __server_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.__server = websocket
        
        config = {
            'type': 'config',
            'peerConnectionOptions': {}
        }
        await websocket.send_text(json.dumps(config))
        
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
            player_id = int(data.get('playerId'))
        except (ValueError, TypeError):
            logger.error(f'[Server] Invalid playerId: {data.get("playerId")}')
            return
        
        player = self.__clients[player_id]
        if player is None:
            logger.error(f'[Server] Player not found: {player_id}')
            return
       
        if data['type'] == 'answer':
            await player.send_text(json.dumps(data))
        elif data['type'] == 'iceCandidate':
            await player.send_text(json.dumps(data))
        elif data['type'] == 'disconnectPlayer':
            await player.close(1011, data['reason'])
        else:
            return