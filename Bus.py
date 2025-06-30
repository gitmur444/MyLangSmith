from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from Signal import Signal

if TYPE_CHECKING:
    from Actor import Actor


class Bus:
    """Simple in-memory message bus for actors."""

    def __init__(self) -> None:
        self.agents: Dict[str, Actor] = {}

    def register(self, agent: 'Actor') -> None:
        self.agents[agent.name] = agent

    def send(self, message: Signal) -> None:
        receiver = self.agents.get(message.receiver)
        if receiver:
            receiver.receive(message)
