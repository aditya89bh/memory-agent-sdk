# Memory Agent SDK

Reusable memory primitives for AI agent developers.

`memory-agent-sdk` is a lightweight Python toolkit for adding inspectable memory behavior to agent prototypes without committing to a full framework. It gives developers simple building blocks for session memory, long-term memory, retrieval, correction, forgetting, policies, and audit events.

Most agent demos either keep memory hidden inside a framework or skip memory lifecycle concerns entirely. This repo makes those primitives explicit so developers can see what was remembered, why it was retrieved, how it was corrected, and when it was forgotten.

This is not a production agent framework. It is a clean, portfolio-grade SDK for experimenting with memory architecture using only the Python standard library in v0.1.

## Architecture

```text
Agent / app code
    ↓
Memory API
    ↓
MemoryPolicy ── decides what should be remembered or ignored
    ↓
Store ── InMemoryStore, JSONStore, or SQLiteStore
    ↓
Retrieval / Correction / Forgetting
    ↓
Audit events
```

The SDK keeps each memory concern separate. Stores persist records, retrieval ranks them, correction preserves superseded history, forgetting marks memories inactive, and events provide a lightweight audit trail.

## Memory lifecycle

```text
remember → retrieve → correct → forget / expire → audit
```

A memory starts as a `MemoryRecord`, can be retrieved by query and tags, corrected without losing the previous version, and eventually forgotten or expired. Each major action emits an audit event so agent builders can inspect memory behavior during development.

## Quickstart

```bash
git clone https://github.com/aditya89bh/memory-agent-sdk.git
cd memory-agent-sdk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Example usage

```python
from memory_agent_sdk import Memory, InMemoryStore

memory = Memory(store=InMemoryStore())

record = memory.remember(
    "User prefers concise Python examples",
    tags=["preference"],
    importance=0.9,
)

results = memory.retrieve("Python preference", tags=["preference"])

print(record.id)
print(results[0].text)
```

## Runnable examples

```bash
python examples/basic_session_memory.py
python examples/retrieval_demo.py
python examples/correction_demo.py
python examples/forgetting_demo.py
python examples/agent_loop_demo.py
```

## Tests

```bash
pytest
```

## Roadmap

Placeholder for v0.2 ideas: richer policy hooks, export/import tools, deterministic summarization helpers, and optional adapters.
