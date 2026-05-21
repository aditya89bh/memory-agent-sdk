from datetime import datetime
from .correction import correct_memory
from .events import AuditEvent, EventType
from .forgetting import forget_by_id, forget_by_tag, forget_by_text, forget_expired
from .policies import MemoryPolicy
from .retrieval import retrieve_records
from .store import InMemoryStore, Store
from .types import MemoryRecord
class Memory:
    def __init__(self, store:Store|None=None, policy:MemoryPolicy|None=None): self.store=store or InMemoryStore(); self.policy=policy or MemoryPolicy()
    def remember(self,text:str,tags=None,importance=.5,metadata=None,expires_at:datetime|None=None):
        tags=list(tags or [])
        if not self.policy.should_remember(text,tags): return None
        r=MemoryRecord(text=text,tags=tags,importance=importance,metadata=metadata or {},expires_at=expires_at); self.store.save(r); self.store.add_event(AuditEvent(EventType.MEMORY_CREATED,r.id,{"tags":tags})); return r
    def retrieve(self,query:str,tags=None,limit=5):
        self.forget_expired(); res=retrieve_records(self.store.all(),query,tags,limit); self.store.add_event(AuditEvent(EventType.MEMORY_RETRIEVED,None,{"query":query,"result_ids":[x.id for x in res]})); return res
    def correct(self,new_text:str,memory_id=None,text_match=None,tags=None,importance=None): return correct_memory(self.store,memory_id=memory_id,text_match=text_match,new_text=new_text,tags=tags,importance=importance)
    def forget(self,memory_id=None,text_match=None,tag=None,soft_delete=True):
        if memory_id: return forget_by_id(self.store,memory_id,soft_delete)
        if text_match: return forget_by_text(self.store,text_match,soft_delete)
        if tag: return forget_by_tag(self.store,tag,soft_delete)
        raise ValueError("Provide memory_id, text_match, or tag")
    def forget_expired(self): return forget_expired(self.store)
    def events(self): return self.store.events()
