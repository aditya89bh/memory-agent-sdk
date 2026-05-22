from memory_agent_sdk import Memory, MemoryPolicy


def test_policy_ignores_empty_text():
    policy = MemoryPolicy()

    assert policy.should_remember("   ") is False


def test_policy_ignores_small_talk_by_default():
    memory = Memory(policy=MemoryPolicy())

    record = memory.remember("hello")

    assert record is None
    assert memory.store.all() == []
    assert memory.events() == []


def test_policy_can_allow_small_talk():
    memory = Memory(policy=MemoryPolicy(ignore_small_talk=False))

    record = memory.remember("hello")

    assert record is not None
    assert record.text == "hello"


def test_policy_blocks_sensitive_terms_by_default():
    memory = Memory(policy=MemoryPolicy())

    record = memory.remember("The API key is abc123")

    assert record is None
    assert memory.store.all() == []


def test_policy_can_allow_sensitive_terms():
    memory = Memory(policy=MemoryPolicy(allow_sensitive=True))

    record = memory.remember("The API key is abc123")

    assert record is not None
    assert record.text == "The API key is abc123"


def test_policy_can_disable_preference_memory():
    memory = Memory(policy=MemoryPolicy(remember_preferences=False))

    record = memory.remember("User prefers concise answers", tags=["preference"])

    assert record is None
    assert memory.store.all() == []


def test_policy_can_disable_task_memory():
    memory = Memory(policy=MemoryPolicy(remember_tasks=False))

    record = memory.remember("Follow up with the integration team", tags=["task"])

    assert record is None
    assert memory.store.all() == []
