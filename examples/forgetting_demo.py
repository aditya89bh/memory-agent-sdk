from memory_agent_sdk import Memory

m=Memory(); m.remember("Temporary note",tags=["note"]); m.forget(tag="note"); print(m.retrieve("Temporary")); print([e.type.value for e in m.events()])
