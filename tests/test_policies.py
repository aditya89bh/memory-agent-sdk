from memory_agent_sdk import Memory, MemoryPolicy

def test_policy_ignores_small_talk_and_sensitive_text_by_default():
    p=MemoryPolicy(); assert p.should_ignore("hey"); assert p.should_ignore("my password is abc"); assert not p.should_remember("my password is abc")

def test_policy_flags_control_preferences_and_tasks():
    p=MemoryPolicy(remember_preferences=False, remember_tasks=False)
    assert p.should_ignore("User likes short answers",tags=["preference"])
    assert p.should_ignore("Ship the feature",tags=["task"])

def test_memory_uses_policy_before_remembering():
    m=Memory(policy=MemoryPolicy(ignore_small_talk=True)); assert m.remember("hey") is None; assert m.store.all()==[]
