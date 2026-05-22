import pytest

from memory_agent_sdk import EventType, Memory, MemoryNotFoundError, MemoryStatus


def test_correct_by_id_supersedes_previous_memory_and_preserves_audit_trail():
    memory = Memory()
    old = memory.remember(
        "User prefers verbose answers",
        tags=["preference", "communication"],
        importance=0.4,
        metadata={"source": "initial"},
    )

    new = memory.correct(
        memory_id=old.id,
        new_text="User prefers concise answers",
        tags=["preference", "communication"],
        importance=0.9,
    )

    stored_old = memory.store.get(old.id)

    assert stored_old.status == MemoryStatus.SUPERSEDED
    assert stored_old.superseded_by == new.id
    assert new.text == "User prefers concise answers"
    assert new.tags == ["preference", "communication"]
    assert new.importance == 0.9
    assert new.metadata["source"] == "initial"
    assert new.metadata["corrects"] == old.id
    assert memory.events()[-1].type == EventType.MEMORY_CORRECTED
    assert memory.events()[-1].memory_id == new.id
    assert memory.events()[-1].details == {"previous_id": old.id}


def test_correct_by_text_match_uses_existing_tags_and_importance_by_default():
    memory = Memory()
    old = memory.remember(
        "The repo is private",
        tags=["project", "status"],
        importance=0.8,
    )

    new = memory.correct(text_match="private", new_text="The repo is public")

    assert new.text == "The repo is public"
    assert new.tags == ["project", "status"]
    assert new.importance == 0.8
    assert new.metadata["corrects"] == old.id
    assert memory.store.get(old.id).status == MemoryStatus.SUPERSEDED


def test_correct_can_override_tags_without_losing_corrects_metadata():
    memory = Memory()
    old = memory.remember("Use temporary project framing", tags=["temporary"])

    new = memory.correct(
        memory_id=old.id,
        new_text="Use durable project framing",
        tags=["project", "durable"],
    )

    assert new.tags == ["project", "durable"]
    assert new.metadata["corrects"] == old.id


def test_correct_missing_memory_id_raises_memory_not_found_error():
    memory = Memory()

    with pytest.raises(MemoryNotFoundError, match="No matching memory found to correct"):
        memory.correct(memory_id="missing-id", new_text="Updated memory")


def test_correct_missing_text_match_raises_memory_not_found_error():
    memory = Memory()
    memory.remember("User prefers concise answers")

    with pytest.raises(MemoryNotFoundError, match="No matching memory found to correct"):
        memory.correct(text_match="nonexistent", new_text="Updated memory")
