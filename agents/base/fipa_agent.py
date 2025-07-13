from typing import List, Optional

from messages.fipa_message import FIPAMessage
from buses.base.fipa_message_bus import FipaMessageBus

class FIPAAgent:
    """Base class for agents communicating via FIPA ACL."""

    def __init__(self, name: str, bus: Optional[FipaMessageBus] = None) -> None:
        self.name = name
        self.bus = bus
        self.inbox: List[FIPAMessage] = []
        if self.bus is not None:
            self.bus.register(self)

    async def send(self, receiver: str, performative: str, content: str) -> None:
        if self.bus is None:
            raise RuntimeError("Agent is not connected to a message bus")
        message = FIPAMessage(
            performative=performative,
            sender=self.name,
            receiver=receiver,
            content=content,
        )
        self.bus.send(message)

    def receive(self, message: FIPAMessage) -> None:
        self.inbox.append(message)
        self.on_message(message)

    def on_message(self, message: FIPAMessage) -> None:
        """Handle an incoming message. Override in subclasses."""
        print(
            f"{self.name} received {message.performative} from {message.sender}: {message.content}"
        )
