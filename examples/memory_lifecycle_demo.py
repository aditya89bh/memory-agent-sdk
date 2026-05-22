"""Demonstrate the full memory lifecycle.

Run with:
    python examples/memory_lifecycle_demo.py

This example shows how an agent can:
- remember useful context
- retrieve relevant memory
- correct stale memory
- forget temporary memory
- inspect audit events
"""

from memory_agent_sdk import Memory


def print_records(title, records):
    print(f"\n{title}")
    if not records:
        print("  No records found.")
        return
    for record in records:
        print(f"  - {record.text}")
        print(f"    id={record.id}")
        print(f"    tags={record.tags}")
        print(f"    importance={record.importance}")
        print(f"    status={record.status.value}")


def print_events(memory):
    print("\nAudit Events")
    for event in memory.events():
        print(f"  - {event.type.value}: memory_id={event.memory_id}, details={event.details}")


def main():
    memory = Memory()

    print("Memory Agent SDK: Lifecycle Demo")
    print("================================")

    preference = memory.remember(
        "User prefers concise technical explanations.",
        tags=["preference", "communication"],
        importance=0.9,
    )
    task = memory.remember(
        "User is building a reusable SDK for agent memory primitives.",
        tags=["project", "sdk", "agent-memory"],
        importance=0.95,
    )
    temporary_note = memory.remember(
        "Temporary note: validate the local demo output before committing.",
        tags=["temporary", "validation"],
        importance=0.3,
    )

    print_records("Stored Memories", [preference, task, temporary_note])

    retrieved = memory.retrieve("How should I explain the agent memory SDK?", limit=3)
    print_records("Retrieved Memories", retrieved)

    corrected = memory.correct(
        memory_id=preference.id,
        new_text="User prefers concise explanations with concrete engineering tradeoffs.",
        tags=["preference", "communication"],
        importance=0.95,
    )
    print_records("Corrected Memory", [corrected])

    memory.forget(tag="temporary")
    remaining = memory.retrieve("demo validation temporary note", limit=5)
    print_records("Retrieval After Forgetting Temporary Memory", remaining)

    print_events(memory)

    print("\nLifecycle Summary")
    print("  observe -> decide -> store -> retrieve -> use -> correct -> forget -> audit")


if __name__ == "__main__":
    main()
