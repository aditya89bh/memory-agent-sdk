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

## Core primitives

| Primitive | Purpose |
|---|---|
| `Memory` | High-level API for remembering, retrieving, correcting, forgetting, and reading audit events. |
| `SessionMemory` | Short-lived conversational turns for an active interaction. |
| `MemoryRecord` | Data object for one long-term memory item. |
| `MemoryPolicy` | Rules for deciding what should be remembered or ignored. |
| `InMemoryStore` | Fast ephemeral store for tests and demos. |
| `JSONStore` | Simple file-backed persistence for small local projects. |
| `SQLiteStore` | Durable local persistence using the Python standard library. |
| Retrieval helpers | Keyword overlap, recency, importance, and tag-based filtering. |
| Correction helpers | Supersede old memory records while preserving history. |
| Forgetting helpers | Soft-delete memories by id, text match, tag, or expiry. |
| Audit events | Track created, retrieved, corrected, forgotten, and expired memory operations. |

## Design principles

- **Standard library first:** no LangChain, OpenAI API, vector database, or hosted service dependency in v0.1.
- **Readable over clever:** each primitive should be understandable by agent builders.
- **Lifecycle-aware:** memory is not just storage; it needs retrieval, correction, forgetting, and auditability.
- **Framework-neutral:** the SDK should be usable from any agent loop or application.
- **Portfolio-grade honesty:** useful primitives and examples, but not positioned as production infrastructure yet.

## Current status

This repo is an early SDK/prototype for demonstrating memory architecture. It is suitable for learning, portfolio work, local experiments, and extension into future integrations. It is not yet hardened for production scale, concurrent writes, distributed storage, or sensitive data governance.

## Tests

```bash
pytest
```

## Roadmap

- Add richer policy hooks for custom memory filtering.
- Add deterministic summarization helpers.
- Add import/export utilities for memory records and audit logs.
- Add more examples for agent loops and task memory.
- Consider optional adapters for agent frameworks later, while keeping the core dependency-free.
