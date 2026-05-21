# Memory Agent SDK

Reusable memory primitives for AI agent developers: session memory, long-term memory, retrieval, correction, forgetting, memory policies, and audit events.

This is a lightweight portfolio-grade tooling repo, not a production framework. v0.1 uses only the Python standard library.

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
