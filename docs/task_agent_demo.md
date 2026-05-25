# Task Agent Demo

The task-agent demo shows how Memory Agent SDK can be used inside a small, inspectable agent loop.

It is intentionally simple. The goal is to demonstrate memory behavior, not to build a full autonomous agent framework.

## Run the Demo

```bash
python examples/task_agent_demo.py
```

## What It Demonstrates

The demo walks through a realistic memory lifecycle:

1. Seed durable preference memory.
2. Seed stale project memory.
3. Receive a task.
4. Retrieve relevant context with `retrieve_trace()`.
5. Make a task decision using retrieved memory.
6. Write a new project memory.
7. Correct stale memory.
8. Print the audit trail.

## Demo Flow

```text
seed memory
  -> receive task
  -> retrieve preference memory with trace
  -> decide next action
  -> remember new project state
  -> correct stale project state
  -> inspect audit trail
```

## Why This Matters

Most agent memory examples stop at storing and retrieving text.

This demo shows a more useful pattern:

- memory influences a decision
- retrieval is inspectable
- new state is written back
- stale state is corrected
- actions are auditable

That is closer to how memory should work inside real agent systems.

## Key SDK Features Used

| Feature | Purpose |
|---|---|
| `Memory.remember()` | Stores preference and project memories. |
| `Memory.retrieve_trace()` | Retrieves relevant memory and exposes diagnostic information. |
| `Memory.correct()` | Replaces stale memory while preserving history. |
| `Memory.events()` | Prints the audit trail. |
| `RetrievalTrace` | Shows candidates, scores, and retrieved results. |

## Expected Output Shape

The output includes sections like:

```text
=== Seed memory ===
=== Task ===
=== Retrieved memory trace ===
=== Decision ===
=== Write new memory ===
=== Correct stale memory ===
=== Audit trail ===
```

The exact memory ids will vary between runs.

## Design Boundary

This is not an LLM-powered agent.

The decision logic is deterministic so developers can inspect how memory changes behavior without involving external APIs, model calls, or framework dependencies.

This keeps the demo:

- local
- repeatable
- dependency-free
- easy to test
- easy to extend

## Extension Ideas

Future versions could extend this demo with:

- task-specific policies
- JSON or SQLite persistence
- multi-step task plans
- benchmark scenarios based on the demo
- optional LLM adapter examples
- structured decision traces

## Developer Takeaway

The demo shows the core SDK thesis in one place:

> Agent memory should be explicit, inspectable, correctable, auditable, and useful inside a decision loop.
