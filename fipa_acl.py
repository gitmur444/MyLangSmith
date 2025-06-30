from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


@dataclass
class FIPAMessage:
    """Minimal representation of a FIPA ACL message."""

    performative: str
    sender: str
    receiver: str
    content: str
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class MessageBus:
    """Simple in-memory message bus for agents."""

    def __init__(self) -> None:
        self.agents: Dict[str, FIPAAgent] = {}

    def register(self, agent: 'FIPAAgent') -> None:
        self.agents[agent.name] = agent

    def send(self, message: FIPAMessage) -> None:
        receiver = self.agents.get(message.receiver)
        if receiver:
            receiver.receive(message)


class FIPAAgent:
    """Base class for agents communicating via FIPA ACL."""

    def __init__(self, name: str, bus: Optional[MessageBus] = None) -> None:
        self.name = name
        self.bus = bus
        self.inbox: List[FIPAMessage] = []
        if self.bus is not None:
            self.bus.register(self)

    def send(self, receiver: str, performative: str, content: str) -> None:
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
