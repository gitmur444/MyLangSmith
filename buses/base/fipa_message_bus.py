from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from messages.fipa_message import FIPAMessage

if TYPE_CHECKING:
    from agents.base.fipa_agent import FIPAAgent


class FipaMessageBus:
    """Simple in-memory message bus for agents."""

    def __init__(self) -> None:
        self.agents: Dict[str, 'FIPAAgent'] = {}

    def register(self, agent: 'FIPAAgent') -> None:
        self.agents[agent.name] = agent

    def send(self, message: FIPAMessage) -> None:
        receiver = self.agents.get(message.receiver)
        if receiver:
            receiver.receive(message)
