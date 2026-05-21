# Memory Agent SDK

Reusable memory primitives for AI agent developers.

`memory-agent-sdk` is a lightweight Python toolkit for adding inspectable memory behavior to agent prototypes without committing to a full framework. It gives developers simple building blocks for session memory, long-term memory, retrieval, correction, forgetting, policies, and audit events.

Most agent demos either keep memory hidden inside a framework or skip memory lifecycle concerns entirely. This repo makes those primitives explicit so developers can see what was remembered, why it was retrieved, how it was corrected, and when it was forgotten.

This is not a production agent framework. It is a clean, portfolio-grade SDK for experimenting with memory architecture using only the Python standard library in v0.1.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Example usage

```python
from memory_agent_sdk import Memory, InMemoryStore

memory = Memory(store=InMemoryStore())
record = memory.remember("User prefers concise answers", tags=["preference"], importance=0.9)
results = memory.retrieve("concise", tags=["preference"])
print(record.id)
print(results[0].text)
```

## Tests

```bash
pytest
```

## Roadmap

Placeholder for v0.2 ideas: richer policy hooks, export/import tools, deterministic summarization helpers, and optional adapters.
