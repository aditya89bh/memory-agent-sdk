from datetime import timedelta

from memory_agent_sdk import EventType, Memory, MemoryInputError, MemoryStatus
from memory_agent_sdk.types import now_utc


def get_record_including_deleted(memory, memory_id):
    return next(record for record in memory.store.all(include_deleted=True) if record.id == memory_id)


def test_forget_by_id_marks_memory_forgotten_and_excludes_from_retrieval():
    memory = Memory()
    record = memory.remember("Forget this durable memory", tags=["temporary"])

    forgotten = memory.forget(memory_id=record.id)
    stored = get_record_including_deleted(memory, record.id)

    assert [item.id for item in forgotten] == [record.id]
    assert stored.status == MemoryStatus.FORGOTTEN
    assert memory.retrieve("durable memory") == []
    assert memory.events()[-2].type == EventType.MEMORY_FORGOTTEN
    assert memory.events()[-2].memory_id == record.id
    assert memory.events()[-2].details == {"method": "id", "soft_delete": True}


def test_forget_by_text_match_only_forgets_matching_records():
    memory = Memory()
    target = memory.remember("Temporary task one", tags=["task"])
    kept = memory.remember("Permanent note two", tags=["note"])

    forgotten = memory.forget(text_match="task one")

    assert [item.id for item in forgotten] == [target.id]
    assert get_record_including_deleted(memory, target.id).status == MemoryStatus.FORGOTTEN
    assert memory.store.get(kept.id).status == MemoryStatus.ACTIVE
    assert memory.events()[-1].details == {"method": "text", "soft_delete": True}


def test_forget_by_tag_forgets_all_matching_records():
    memory = Memory()
    first = memory.remember("Temporary note one", tags=["temporary"])
    second = memory.remember("Temporary note two", tags=["temporary"])
    kept = memory.remember("Durable note", tags=["durable"])

    forgotten = memory.forget(tag="temporary")

    assert {item.id for item in forgotten} == {first.id, second.id}
    assert get_record_including_deleted(memory, first.id).status == MemoryStatus.FORGOTTEN
    assert get_record_including_deleted(memory, second.id).status == MemoryStatus.FORGOTTEN
    assert memory.store.get(kept.id).status == MemoryStatus.ACTIVE
    assert [event.details for event in memory.events()[-2:]] == [
        {"method": "tag", "soft_delete": True},
        {"method": "tag", "soft_delete": True},
    ]


def test_forget_missing_id_returns_empty_list():
    memory = Memory()

    assert memory.forget(memory_id="missing-id") == []


def test_forget_missing_text_match_returns_empty_list():
    memory = Memory()
    memory.remember("Stored memory")

    assert memory.forget(text_match="not present") == []


def test_forget_missing_tag_returns_empty_list():
    memory = Memory()
    memory.remember("Stored memory", tags=["project"])

    assert memory.forget(tag="missing") == []


def test_forget_without_selector_raises_memory_input_error():
    memory = Memory()

    try:
        memory.forget()
    except MemoryInputError as error:
        assert str(error) == "Provide memory_id, text_match, or tag"
    else:
        raise AssertionError("Expected MemoryInputError")


def test_forget_expired_memories_marks_expired_and_emits_event():
    memory = Memory()
    record = memory.remember("Expired", expires_at=now_utc() - timedelta(seconds=1))

    expired = memory.forget_expired()

    assert [item.id for item in expired] == [record.id]
    assert get_record_including_deleted(memory, record.id).status == MemoryStatus.EXPIRED
    assert memory.events()[-1].type == EventType.MEMORY_EXPIRED
    assert memory.events()[-1].memory_id == record.id
    assert memory.events()[-1].details == {"method": "expiry"}
