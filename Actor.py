from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from Signal import Signal

if TYPE_CHECKING:
    from Bus import Bus


class Actor:
    """Base class for agents communicating via FIPA ACL."""

    def __init__(self, name: str, bus: Optional['Bus'] = None) -> None:
        self.name = name
        self.bus = bus
        self.inbox: List[Signal] = []
        if self.bus is not None:
            self.bus.register(self)

    def send(self, receiver: str, performative: str, content: str) -> None:
        if self.bus is None:
            raise RuntimeError("Actor is not connected to a message bus")
        message = Signal(
            performative=performative,
            sender=self.name,
            receiver=receiver,
            content=content,
        )
        self.bus.send(message)

    def receive(self, message: Signal) -> None:
        self.inbox.append(message)
        self.on_message(message)

    def on_message(self, message: Signal) -> None:
        """Handle an incoming message. Override in subclasses."""
        print(f"{self.name} received {message.performative} from {message.sender}: {message.content}")
