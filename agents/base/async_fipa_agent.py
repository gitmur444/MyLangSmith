import asyncio
from typing import Optional

from messages.fipa_message import FIPAMessage
from buses.base.fipa_message_bus import FipaMessageBus
from agents.base.fipa_agent import FIPAAgent

class AsyncFIPAAgent(FIPAAgent):
    """Asynchronous variant of ``FIPAAgent`` that schedules ``on_message`` calls."""

    async def on_message(self, message: FIPAMessage) -> None:  # pragma: no cover - to be overridden
        await asyncio.sleep(0)

    def receive(self, message: FIPAMessage) -> None:
        """Store message and schedule async ``on_message`` execution."""
        self.inbox.append(message)
        asyncio.create_task(self.on_message(message))
