from memory_agent_sdk import JSONStore, Memory, SQLiteStore


def test_json_store_persists_records_and_events(tmp_path):
    store_path = tmp_path / "memory.json"

    memory = Memory(store=JSONStore(store_path))
    record = memory.remember(
        "User prefers concise technical explanations.",
        tags=["preference"],
        importance=0.9,
    )
    memory.retrieve("technical explanations")

    reloaded_memory = Memory(store=JSONStore(store_path))
    records = reloaded_memory.store.all()
    events = reloaded_memory.events()

    assert len(records) == 1
    assert records[0].id == record.id
    assert records[0].text == "User prefers concise technical explanations."
    assert records[0].tags == ["preference"]
    assert records[0].importance == 0.9
    assert len(events) == 2
    assert [event.type.value for event in events] == ["MEMORY_CREATED", "MEMORY_RETRIEVED"]


def test_sqlite_store_persists_records_and_events(tmp_path):
    store_path = tmp_path / "memory.sqlite"

    memory = Memory(store=SQLiteStore(store_path))
    record = memory.remember(
        "Agent should preserve correction history.",
        tags=["agent-memory", "correction"],
        importance=0.8,
    )
    memory.retrieve("correction history")

    reloaded_memory = Memory(store=SQLiteStore(store_path))
    records = reloaded_memory.store.all()
    events = reloaded_memory.events()

    assert len(records) == 1
    assert records[0].id == record.id
    assert records[0].text == "Agent should preserve correction history."
    assert records[0].tags == ["agent-memory", "correction"]
    assert records[0].importance == 0.8
    assert len(events) == 2
    assert [event.type.value for event in events] == ["MEMORY_CREATED", "MEMORY_RETRIEVED"]
