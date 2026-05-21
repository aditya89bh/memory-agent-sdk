from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4
from .types import now_utc
class EventType(str, Enum):
    MEMORY_CREATED="MEMORY_CREATED"; MEMORY_RETRIEVED="MEMORY_RETRIEVED"; MEMORY_CORRECTED="MEMORY_CORRECTED"; MEMORY_FORGOTTEN="MEMORY_FORGOTTEN"; MEMORY_EXPIRED="MEMORY_EXPIRED"
@dataclass
class AuditEvent:
    type: EventType
    memory_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=now_utc)
