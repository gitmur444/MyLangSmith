import asyncio
import json
import websockets

from buses.base.bus import Bus


class WebBus(Bus):
    """Simple WebSocket-based message bus for actors."""

    def __init__(self) -> None:
        super().__init__()
        self.clients = {}

    async def handler(self, websocket, path):
        print("DEBUG: handler called with websocket and path:", websocket, path, flush=True)
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
        print(f"DEBUG: websockets.serve(self.handler={self.handler}, type={type(self.handler)})", flush=True)
        async with websockets.serve(self.handler, host, port):
            await asyncio.Future()  # run forever
