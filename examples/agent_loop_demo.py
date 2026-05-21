from memory_agent_sdk import Memory, SessionMemory

memory=Memory(); session=SessionMemory()
def agent_turn(text):
    session.add_turn("user",text)
    if "prefer" in text.lower(): memory.remember(text,tags=["preference"],importance=.8)
    ctx=memory.retrieve(text,tags=["preference"],limit=2)
    reply="Using memory: "+"; ".join(r.text for r in ctx) if ctx else "No relevant memory yet."
    session.add_turn("assistant",reply); return reply
print(agent_turn("I prefer concise technical answers.")); print(agent_turn("How should you answer me?"))
