from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


class FipaMessageBus:
    """Simple in-memory message bus for agents."""

    def __init__(self) -> None:
        self.agents: Dict[str, FIPAAgent] = {}

    def register(self, agent: 'FIPAAgent') -> None:
        self.agents[agent.name] = agent

    def send(self, message: FIPAMessage) -> None:
        receiver = self.agents.get(message.receiver)
        if receiver:
            receiver.receive(message)


