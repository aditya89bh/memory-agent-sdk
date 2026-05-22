from datetime import timedelta

from memory_agent_sdk import EventType, JSONStore, Memory, MemoryStatus, SQLiteStore
from memory_agent_sdk.types import now_utc


def get_record_including_deleted(memory, memory_id):
    return next(record for record in memory.store.all(include_deleted=True) if record.id == memory_id)


def run_store_round_trip(store_factory):
    memory = Memory(store=store_factory())
    expires_at = now_utc() + timedelta(days=7)

    original = memory.remember(
        "User prefers concise technical explanations",
        tags=["preference", "communication"],
        importance=0.85,
        metadata={"source": "test", "confidence": "high"},
        expires_at=expires_at,
    )
    corrected = memory.correct(
        memory_id=original.id,
        new_text="User prefers concise explanations with engineering tradeoffs",
        tags=["preference", "communication"],
        importance=0.95,
    )
    memory.retrieve_trace("concise engineering", tags=["preference"])

    reloaded = Memory(store=store_factory())
    old_record = get_record_including_deleted(reloaded, original.id)
    new_record = reloaded.store.get(corrected.id)
    events = reloaded.events()

    assert old_record.status == MemoryStatus.SUPERSEDED
    assert old_record.superseded_by == corrected.id
    assert old_record.tags == ["preference", "communication"]
    assert old_record.metadata == {"source": "test", "confidence": "high"}
    assert old_record.expires_at == expires_at

    assert new_record.text == "User prefers concise explanations with engineering tradeoffs"
    assert new_record.tags == ["preference", "communication"]
    assert new_record.importance == 0.95
    assert new_record.metadata["source"] == "test"
    assert new_record.metadata["confidence"] == "high"
    assert new_record.metadata["corrects"] == original.id
    assert new_record.expires_at == expires_at

    assert [event.type for event in events] == [
        EventType.MEMORY_CREATED,
        EventType.MEMORY_CORRECTED,
        EventType.MEMORY_RETRIEVED,
    ]
    assert events[0].details == {"tags": ["preference", "communication"]}
    assert events[1].memory_id == corrected.id
    assert events[1].details == {"previous_id": original.id}
    assert events[2].details["query"] == "concise engineering"
    assert events[2].details["trace"] is True
    assert events[2].details["result_ids"] == [corrected.id]


def test_json_store_round_trips_records_status_metadata_and_events(tmp_path):
    store_path = tmp_path / "memory.json"

    run_store_round_trip(lambda: JSONStore(store_path))


def test_sqlite_store_round_trips_records_status_metadata_and_events(tmp_path):
    store_path = tmp_path / "memory.sqlite"

    run_store_round_trip(lambda: SQLiteStore(store_path))
