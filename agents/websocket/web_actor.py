import asyncio
import json
import websockets

from agents.base.actor import Actor
from messages.fipa_message import FIPAMessage

class WebActor(Actor):
    """Actor that communicates over a websocket."""

    def __init__(self, name: str, uri: str) -> None:
        super().__init__(name)
        self.uri = uri
        self.websocket = None

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.uri)
        await self.websocket.send(json.dumps({"type": "register", "name": self.name}))
        asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        async for message in self.websocket:
            data = json.loads(message)
            await self.on_message(FIPAMessage(**data))

    async def send(self, receiver: str, performative: str, content: str) -> None:
        msg = FIPAMessage(
            performative=performative,
            sender=self.name,
            receiver=receiver,
            content=content,
        )
        await self.websocket.send(json.dumps(msg.__dict__))

    async def on_message(self, message: FIPAMessage) -> None:
        print(f"{self.name} received {message.performative} from {message.sender}: {message.content}")
