from memory_agent_sdk import SessionMemory

s=SessionMemory(); s.add_turn("user","Remember that I prefer concise answers."); s.add_turn("assistant","Got it."); print(s.summarize())
