import pytest

from memory_agent_sdk import Memory, MemoryInputError, MemoryNotFoundError


def test_forget_without_selector_raises_memory_input_error():
    memory = Memory()

    with pytest.raises(MemoryInputError, match="Provide memory_id, text_match, or tag"):
        memory.forget()


def test_correct_missing_memory_raises_memory_not_found_error():
    memory = Memory()

    with pytest.raises(MemoryNotFoundError, match="No matching memory found to correct"):
        memory.correct(memory_id="missing-id", new_text="Updated memory text")


def test_correct_missing_text_match_raises_memory_not_found_error():
    memory = Memory()
    memory.remember("User prefers concise explanations", tags=["preference"])

    with pytest.raises(MemoryNotFoundError, match="No matching memory found to correct"):
        memory.correct(text_match="nonexistent phrase", new_text="Updated memory text")
