from agents.base.async_fipa_agent import AsyncFIPAAgent
from messages.fipa_message import FIPAMessage


class Echo(AsyncFIPAAgent):
    """Worker that echoes back any request as an inform message."""

    async def on_message(self, message: FIPAMessage) -> None:
        print(
            f"{self.name} received {message.performative} from {message.sender}: {message.content}",
            flush=True,
        )
        if message.performative == "request":
            reply = f"ack: {message.content}"
            await self.send(message.sender, "inform", reply)
