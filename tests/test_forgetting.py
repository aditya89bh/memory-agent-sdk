from datetime import timedelta
from memory_agent_sdk import EventType, Memory, MemoryStatus
from memory_agent_sdk.types import now_utc

def test_forget_by_id_soft_deletes_memory():
    m=Memory(); r=m.remember("Forget this"); f=m.forget(memory_id=r.id)
    assert f[0].status==MemoryStatus.FORGOTTEN
    assert m.retrieve("Forget this")==[]

def test_forget_by_text_and_tag():
    m=Memory(); m.remember("Task one",tags=["task"]); m.remember("Note two",tags=["note"])
    assert len(m.forget(text_match="one"))==1
    assert len(m.forget(tag="note"))==1

def test_forget_expired_memories():
    m=Memory(); m.remember("Expired",expires_at=now_utc()-timedelta(seconds=1)); expired=m.forget_expired()
    assert expired[0].status==MemoryStatus.EXPIRED
    assert m.events()[-1].type==EventType.MEMORY_EXPIRED
