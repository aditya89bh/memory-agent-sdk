from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime
from .types import MemoryRecord, now_utc
_WORD_RE=re.compile(r"[a-zA-Z0-9_]+")
def tokenize(text:str)->set[str]: return {m.group(0).lower() for m in _WORD_RE.finditer(text)}
@dataclass
class RetrievalResult:
    record: MemoryRecord; score: float; keyword_score: float; recency_score: float; importance_score: float
    @property
    def text(self): return self.record.text
    @property
    def id(self): return self.record.id
def keyword_overlap(query,text):
    q=tokenize(query)
    return 0.0 if not q else len(q & tokenize(text))/len(q)
def recency_score(created_at:datetime, at:datetime|None=None):
    return 1/(1+max(((at or now_utc())-created_at).total_seconds(),0)/3600)
def retrieve_records(records, query, tags=None, limit=5):
    req=set(tags or []); out=[]
    for r in records:
        if r.deleted or r.is_expired() or (req and not req.issubset(set(r.tags))): continue
        k=keyword_overlap(query,r.text); rec=recency_score(r.created_at); imp=max(0,min(1,float(r.importance))); score=.55*k+.20*rec+.25*imp
        if query and k==0 and not req: continue
        out.append(RetrievalResult(r,score,k,rec,imp))
    return sorted(out,key=lambda x:x.score,reverse=True)[:limit]
