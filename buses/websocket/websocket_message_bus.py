import asyncio
import json
import websockets

from buses.base.fipa_message_bus import FipaMessageBus

class WebSocketMessageBus(FipaMessageBus):
    """Simple WebSocket-based message bus for FIPA agents."""

    def __init__(self) -> None:
        super().__init__()
        self.clients = {}

    async def handler(self, websocket, path):
        # Expect a registration message first
        register_msg = await websocket.recv()
        register = json.loads(register_msg)
        if register.get("type") != "register":
            await websocket.close()
            return
        name = register["name"]
        self.clients[name] = websocket
        try:
            async for msg in websocket:
                data = json.loads(msg)
                receiver = data.get("receiver")
                target = self.clients.get(receiver)
                if target:
                    await target.send(msg)
        finally:
            self.clients.pop(name, None)
# handler принимает два аргумента: websocket, path

    async def start(self, host: str = "localhost", port: int = 8765) -> None:
        async with websockets.serve(self.handler, host, port):
            await asyncio.Future()  # run forever
