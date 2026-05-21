from __future__ import annotations
import json, sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from .events import AuditEvent, EventType
from .types import MemoryRecord, MemoryStatus

def _dt_to_str(v: datetime | None) -> str | None: return v.isoformat() if v else None
def _dt_from_str(v: str | None) -> datetime | None: return datetime.fromisoformat(v) if v else None
def record_to_dict(r: MemoryRecord) -> dict[str, Any]:
    return {"id":r.id,"text":r.text,"tags":list(r.tags),"importance":r.importance,"metadata":dict(r.metadata),"created_at":_dt_to_str(r.created_at),"updated_at":_dt_to_str(r.updated_at),"expires_at":_dt_to_str(r.expires_at),"status":r.status.value,"superseded_by":r.superseded_by}
def record_from_dict(d: dict[str, Any]) -> MemoryRecord:
    return MemoryRecord(id=d["id"], text=d["text"], tags=list(d.get("tags",[])), importance=float(d.get("importance",0.5)), metadata=dict(d.get("metadata",{})), created_at=_dt_from_str(d.get("created_at")), updated_at=_dt_from_str(d.get("updated_at")), expires_at=_dt_from_str(d.get("expires_at")), status=MemoryStatus(d.get("status",MemoryStatus.ACTIVE.value)), superseded_by=d.get("superseded_by"))
def event_to_dict(e: AuditEvent) -> dict[str, Any]: return {"id":e.id,"type":e.type.value,"memory_id":e.memory_id,"details":dict(e.details),"created_at":_dt_to_str(e.created_at)}
def event_from_dict(d: dict[str, Any]) -> AuditEvent: return AuditEvent(id=d["id"], type=EventType(d["type"]), memory_id=d.get("memory_id"), details=dict(d.get("details",{})), created_at=_dt_from_str(d.get("created_at")))
class Store(ABC):
    @abstractmethod
    def save(self, record: MemoryRecord) -> MemoryRecord: ...
    @abstractmethod
    def get(self, memory_id: str) -> MemoryRecord | None: ...
    @abstractmethod
    def all(self, include_deleted: bool=False) -> list[MemoryRecord]: ...
    @abstractmethod
    def add_event(self, event: AuditEvent) -> AuditEvent: ...
    @abstractmethod
    def events(self) -> list[AuditEvent]: ...
class InMemoryStore(Store):
    def __init__(self): self._records={}; self._events=[]
    def save(self, record): self._records[record.id]=record; return record
    def get(self, memory_id): return self._records.get(memory_id)
    def all(self, include_deleted=False):
        rs=list(self._records.values())
        return sorted(rs if include_deleted else [r for r in rs if not r.deleted], key=lambda r:r.created_at)
    def add_event(self,event): self._events.append(event); return event
    def events(self): return list(self._events)
class JSONStore(InMemoryStore):
    def __init__(self,path): self.path=Path(path); super().__init__(); self._load()
    def _load(self):
        if self.path.exists():
            d=json.loads(self.path.read_text()); self._records={x["id"]:record_from_dict(x) for x in d.get("records",[])}; self._events=[event_from_dict(x) for x in d.get("events",[])]
    def _flush(self):
        self.path.parent.mkdir(parents=True, exist_ok=True); self.path.write_text(json.dumps({"records":[record_to_dict(r) for r in self._records.values()],"events":[event_to_dict(e) for e in self._events]}, indent=2))
    def save(self, record): super().save(record); self._flush(); return record
    def add_event(self,event): super().add_event(event); self._flush(); return event
class SQLiteStore(Store):
    def __init__(self,path=":memory:"):
        self.path=str(path); self.conn=sqlite3.connect(self.path); self.conn.row_factory=sqlite3.Row; self._init_schema()
    def _init_schema(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS memories (id TEXT PRIMARY KEY,text TEXT NOT NULL,tags TEXT NOT NULL,importance REAL NOT NULL,metadata TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,expires_at TEXT,status TEXT NOT NULL,superseded_by TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY,type TEXT NOT NULL,memory_id TEXT,details TEXT NOT NULL,created_at TEXT NOT NULL)"); self.conn.commit()
    def save(self,r):
        d=record_to_dict(r); self.conn.execute("INSERT OR REPLACE INTO memories VALUES (?,?,?,?,?,?,?,?,?,?)", (d["id"],d["text"],json.dumps(d["tags"]),d["importance"],json.dumps(d["metadata"]),d["created_at"],d["updated_at"],d["expires_at"],d["status"],d["superseded_by"])); self.conn.commit(); return r
    def get(self,memory_id):
        row=self.conn.execute("SELECT * FROM memories WHERE id=?",(memory_id,)).fetchone(); return self._row_to_record(row) if row else None
    def all(self, include_deleted=False):
        rs=[self._row_to_record(x) for x in self.conn.execute("SELECT * FROM memories ORDER BY created_at").fetchall()]
        return rs if include_deleted else [r for r in rs if not r.deleted]
    def add_event(self,e):
        d=event_to_dict(e); self.conn.execute("INSERT OR REPLACE INTO events VALUES (?,?,?,?,?)", (d["id"],d["type"],d["memory_id"],json.dumps(d["details"]),d["created_at"])); self.conn.commit(); return e
    def events(self):
        return [event_from_dict({"id":r["id"],"type":r["type"],"memory_id":r["memory_id"],"details":json.loads(r["details"]),"created_at":r["created_at"]}) for r in self.conn.execute("SELECT * FROM events ORDER BY created_at").fetchall()]
    def _row_to_record(self,row):
        return record_from_dict({"id":row["id"],"text":row["text"],"tags":json.loads(row["tags"]),"importance":row["importance"],"metadata":json.loads(row["metadata"]),"created_at":row["created_at"],"updated_at":row["updated_at"],"expires_at":row["expires_at"],"status":row["status"],"superseded_by":row["superseded_by"]})
