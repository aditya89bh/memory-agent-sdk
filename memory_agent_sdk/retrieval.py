from __future__ import annotations
import re
from dataclasses import dataclass, field
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
@dataclass
class RetrievalTrace:
    query: str
    requested_tags: list[str] = field(default_factory=list)
    candidates_seen: int = 0
    candidates_scored: int = 0
    rejected: list[dict[str, str]] = field(default_factory=list)
    results: list[RetrievalResult] = field(default_factory=list)
def keyword_overlap(query,text):
    q=tokenize(query)
    return 0.0 if not q else len(q & tokenize(text))/len(q)
def recency_score(created_at:datetime, at:datetime|None=None):
    return 1/(1+max(((at or now_utc())-created_at).total_seconds(),0)/3600)
def _score_record(record, query):
    k=keyword_overlap(query,record.text); rec=recency_score(record.created_at); imp=max(0,min(1,float(record.importance))); score=.55*k+.20*rec+.25*imp
    return RetrievalResult(record,score,k,rec,imp)
def retrieve_records_trace(records, query, tags=None, limit=5):
    req=set(tags or []); out=[]; trace=RetrievalTrace(query=query, requested_tags=list(tags or []))
    for r in records:
        trace.candidates_seen += 1
        if r.deleted:
            trace.rejected.append({"id":r.id,"reason":"deleted"}); continue
        if r.is_expired():
            trace.rejected.append({"id":r.id,"reason":"expired"}); continue
        if req and not req.issubset(set(r.tags)):
            trace.rejected.append({"id":r.id,"reason":"tag_mismatch"}); continue
        result=_score_record(r,query)
        if query and result.keyword_score==0 and not req:
            trace.rejected.append({"id":r.id,"reason":"no_keyword_overlap"}); continue
        out.append(result)
    trace.candidates_scored=len(out)
    trace.results=sorted(out,key=lambda x:x.score,reverse=True)[:limit]
    return trace
def retrieve_records(records, query, tags=None, limit=5):
    return retrieve_records_trace(records, query, tags, limit).results
