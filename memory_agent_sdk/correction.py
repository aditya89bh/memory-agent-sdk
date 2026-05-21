from .events import AuditEvent, EventType
from .store import Store
from .types import MemoryRecord, MemoryStatus, now_utc

def correct_memory(store:Store, *, memory_id=None, text_match=None, new_text:str, tags=None, importance=None):
    old=store.get(memory_id) if memory_id else None
    if old is None and text_match: old=next((r for r in store.all() if text_match.lower() in r.text.lower()), None)
    if old is None: raise ValueError("No matching memory found to correct")
    new=MemoryRecord(text=new_text, tags=list(tags if tags is not None else old.tags), importance=old.importance if importance is None else importance, metadata={**old.metadata,"corrects":old.id}, expires_at=old.expires_at)
    old.status=MemoryStatus.SUPERSEDED; old.superseded_by=new.id; old.updated_at=now_utc(); store.save(old); store.save(new)
    store.add_event(AuditEvent(EventType.MEMORY_CORRECTED,new.id,{"previous_id":old.id}))
    return new
