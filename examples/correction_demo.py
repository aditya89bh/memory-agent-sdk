from memory_agent_sdk import Memory

m=Memory(); old=m.remember("User prefers verbose answers",tags=["preference"]); new=m.correct(memory_id=old.id,new_text="User prefers concise answers"); print(old.status.value); print(new.text)
