from __future__ import annotations

from memory_agent_sdk import EventType, Memory


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def decide_next_action(memory: Memory, task: str) -> str:
    trace = memory.retrieve_trace(task, tags=["preference"], limit=3)

    print_section("Retrieved memory trace")
    print(f"query: {trace.query}")
    print(f"candidates_seen: {trace.candidates_seen}")
    print(f"candidates_scored: {trace.candidates_scored}")

    for result in trace.results:
        print(f"memory: {result.text}")
        print(f"score: {result.score:.3f}")

    if any("concise" in result.text.lower() for result in trace.results):
        return "Create a concise implementation plan with tests first."

    return "Create a detailed implementation plan."


def print_audit_trail(memory: Memory) -> None:
    print_section("Audit trail")

    for event in memory.events():
        event_name = event.type.value if isinstance(event.type, EventType) else str(event.type)
        print(f"{event_name}: memory_id={event.memory_id} details={event.details}")


def main() -> None:
    memory = Memory()

    print_section("Seed memory")
    preference = memory.remember(
        "User prefers concise implementation plans with clear validation steps",
        tags=["preference", "planning"],
        importance=0.9,
    )
    stale = memory.remember(
        "The benchmark runner is not part of CI",
        tags=["project", "status"],
        importance=0.8,
    )

    print(f"stored preference: {preference.text}")
    print(f"stored stale project memory: {stale.text}")

    task = "Plan the next SDK improvement with concise steps"

    print_section("Task")
    print(task)

    action = decide_next_action(memory, task)

    print_section("Decision")
    print(action)

    print_section("Write new memory")
    new_memory = memory.remember(
        "Next SDK improvement should include an integrated task-agent demo",
        tags=["project", "next-step"],
        importance=0.85,
    )
    print(f"new memory: {new_memory.text}")

    print_section("Correct stale memory")
    corrected = memory.correct(
        memory_id=stale.id,
        new_text="The benchmark runner is now part of CI",
        tags=["project", "status"],
        importance=0.95,
    )
    print(f"corrected memory: {corrected.text}")

    print_audit_trail(memory)


if __name__ == "__main__":
    main()
