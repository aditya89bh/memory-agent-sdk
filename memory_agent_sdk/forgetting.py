from .events import AuditEvent, EventType
from .store import Store
from .types import MemoryRecord, MemoryStatus, now_utc

def _mark(r:MemoryRecord,status): r.status=status; r.updated_at=now_utc(); return r
def forget_by_id(store:Store,memory_id:str,soft_delete=True):
    r=store.get(memory_id)
    if not r: return []
    _mark(r,MemoryStatus.FORGOTTEN); store.save(r); store.add_event(AuditEvent(EventType.MEMORY_FORGOTTEN,r.id,{"method":"id","soft_delete":soft_delete})); return [r]
def forget_by_text(store,text_match,soft_delete=True):
    ms=[r for r in store.all() if text_match.lower() in r.text.lower()]
    for r in ms: _mark(r,MemoryStatus.FORGOTTEN); store.save(r); store.add_event(AuditEvent(EventType.MEMORY_FORGOTTEN,r.id,{"method":"text","soft_delete":soft_delete}))
    return ms
def forget_by_tag(store,tag,soft_delete=True):
    ms=[r for r in store.all() if tag in r.tags]
    for r in ms: _mark(r,MemoryStatus.FORGOTTEN); store.save(r); store.add_event(AuditEvent(EventType.MEMORY_FORGOTTEN,r.id,{"method":"tag","soft_delete":soft_delete}))
    return ms
def forget_expired(store):
    ms=[r for r in store.all() if r.is_expired()]
    for r in ms: _mark(r,MemoryStatus.EXPIRED); store.save(r); store.add_event(AuditEvent(EventType.MEMORY_EXPIRED,r.id,{"method":"expiry"}))
    return ms
