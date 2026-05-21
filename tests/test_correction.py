from memory_agent_sdk import EventType, Memory, MemoryStatus

def test_correct_by_id_supersedes_previous_memory_and_preserves_audit_trail():
    m=Memory(); old=m.remember("User prefers verbose answers",tags=["preference"]); new=m.correct(memory_id=old.id,new_text="User prefers concise answers")
    stored=m.store.get(old.id)
    assert stored.status==MemoryStatus.SUPERSEDED
    assert stored.superseded_by==new.id
    assert new.metadata["corrects"]==old.id
    assert m.events()[-1].type==EventType.MEMORY_CORRECTED

def test_correct_by_text_match():
    m=Memory(); m.remember("The repo is private")
    assert m.correct(text_match="private",new_text="The repo is public").text=="The repo is public"
