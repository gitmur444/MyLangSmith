from agents.websocket.web_actor import WebActor
from messages.fipa_message import FIPAMessage


class Echo(WebActor):
    """Worker that echoes back any request as an inform message."""

    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "request":
            reply = f"ack: {message.content}"
            await self.send(message.sender, "inform", reply)
