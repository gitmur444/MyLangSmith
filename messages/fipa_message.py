from __future__ import annotations

from dataclasses import dataclass, field
import uuid


@dataclass
class FIPAMessage:
    """Minimal representation of a FIPA ACL message."""

    performative: str
    sender: str
    receiver: str
    content: str
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
