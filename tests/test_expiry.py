from datetime import datetime, timedelta, timezone

from memory_agent_sdk import EventType, Memory, MemoryStatus


def get_record_including_deleted(memory, memory_id):
    return next(record for record in memory.store.all(include_deleted=True) if record.id == memory_id)


def test_expired_memory_is_marked_expired_before_retrieval():
    memory = Memory()
    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    record = memory.remember(
        "Temporary memory that should expire",
        tags=["temporary"],
        expires_at=expired_at,
    )

    results = memory.retrieve("Temporary memory")
    stored = get_record_including_deleted(memory, record.id)

    assert results == []
    assert stored.status == MemoryStatus.EXPIRED
    assert memory.events()[-2].type == EventType.MEMORY_EXPIRED
    assert memory.events()[-2].memory_id == record.id
    assert memory.events()[-2].details == {"method": "expiry"}
    assert memory.events()[-1].type == EventType.MEMORY_RETRIEVED
    assert memory.events()[-1].details["result_ids"] == []


def test_forget_expired_returns_expired_records():
    memory = Memory()
    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    expired_record = memory.remember(
        "Expired memory",
        tags=["temporary"],
        expires_at=expired_at,
    )
    active_record = memory.remember(
        "Active memory",
        tags=["durable"],
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    expired = memory.forget_expired()

    assert [record.id for record in expired] == [expired_record.id]
    assert get_record_including_deleted(memory, expired_record.id).status == MemoryStatus.EXPIRED
    assert memory.store.get(active_record.id).status == MemoryStatus.ACTIVE


def test_retrieval_trace_excludes_expired_memory_after_expiry_processing():
    memory = Memory()
    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    record = memory.remember(
        "Expired preference memory",
        tags=["preference"],
        expires_at=expired_at,
    )

    trace = memory.retrieve_trace("preference", tags=["preference"])

    assert trace.results == []
    assert trace.candidates_seen == 0
    assert trace.candidates_scored == 0
    assert trace.rejected == []
    assert get_record_including_deleted(memory, record.id).status == MemoryStatus.EXPIRED
