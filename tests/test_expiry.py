from datetime import datetime, timedelta, timezone

from memory_agent_sdk import EventType, Memory, MemoryStatus


def test_expired_memory_is_marked_expired_before_retrieval():
    memory = Memory()
    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    record = memory.remember(
        "Temporary memory that should expire",
        tags=["temporary"],
        expires_at=expired_at,
    )

    results = memory.retrieve("Temporary memory")
    stored = memory.store.get(record.id, include_deleted=True)

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
    assert memory.store.get(expired_record.id, include_deleted=True).status == MemoryStatus.EXPIRED
    assert memory.store.get(active_record.id).status == MemoryStatus.ACTIVE


def test_retrieval_trace_reports_expired_rejection_after_expiry_processing():
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
    assert memory.store.get(record.id, include_deleted=True).status == MemoryStatus.EXPIRED
