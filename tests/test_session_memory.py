from memory_agent_sdk import SessionMemory

def test_session_memory_adds_and_summarizes_turns():
    s=SessionMemory(); s.add_turn("user","hello"); s.add_turn("assistant","hi")
    assert len(s.get_turns())==2
    assert s.summarize()=="user: hello\nassistant: hi"
