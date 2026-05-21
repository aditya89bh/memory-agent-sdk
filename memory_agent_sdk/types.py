from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

def now_utc() -> datetime: return datetime.now(timezone.utc)
class MemoryStatus(str, Enum):
    ACTIVE="active"; SUPERSEDED="superseded"; FORGOTTEN="forgotten"; EXPIRED="expired"
@dataclass
class MemoryRecord:
    text: str
    tags: list[str] = field(default_factory=list)
    importance: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=now_utc)
    updated_at: datetime = field(default_factory=now_utc)
    expires_at: datetime | None = None
    status: MemoryStatus = MemoryStatus.ACTIVE
    superseded_by: str | None = None
    @property
    def deleted(self) -> bool: return self.status in {MemoryStatus.FORGOTTEN, MemoryStatus.EXPIRED}
    def is_expired(self, at: datetime | None = None) -> bool: return self.expires_at is not None and self.expires_at <= (at or now_utc())
