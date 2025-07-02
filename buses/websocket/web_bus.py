import asyncio
import json
import websockets

from buses.base.bus import Bus


class WebBus(Bus):
    """Simple WebSocket-based message bus for actors."""

    def __init__(self) -> None:
        super().__init__()
        self.clients = {}

    async def handler(self, websocket):
        register_msg = await websocket.recv()
        register = json.loads(register_msg)
        if register.get("type") != "register":
            await websocket.close()
            return
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                sender = data.get("sender", "unknown")
                receiver = data.get("receiver", "unknown")
                content = data.get("content", "")
                print(f"{sender} --> {receiver}: {content}", flush=True)
                # Пересылаем сообщение всем, кроме отправителя
                for client in self.clients:
                    if client != websocket:
                        await client.send(message)
        finally:
            self.clients.remove(websocket)

    async def start(self, host: str = "localhost", port: int = 8765) -> None:
        async with websockets.serve(self.handler, host, port):
            await asyncio.Future()  # run forever
