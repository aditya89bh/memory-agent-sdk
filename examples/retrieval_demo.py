from memory_agent_sdk import Memory

m=Memory(); m.remember("User prefers concise answers",tags=["preference"],importance=.9); m.remember("Project uses pytest",tags=["project"]); [print(f"{r.score:.2f}: {r.text}") for r in m.retrieve("concise preference")]
