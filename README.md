# Memory Agent SDK

[![CI](https://github.com/aditya89bh/memory-agent-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/aditya89bh/memory-agent-sdk/actions/workflows/ci.yml)

Reusable memory primitives for AI agent developers.

`memory-agent-sdk` is a lightweight Python toolkit for adding inspectable memory behavior to agent prototypes without committing to a full framework. It gives developers simple building blocks for session memory, long-term memory, retrieval, correction, forgetting, policies, and audit events.

Most agent demos either keep memory hidden inside a framework or skip memory lifecycle concerns entirely. This repo makes those primitives explicit so developers can see what was remembered, why it was retrieved, how it was corrected, and when it was forgotten.

This is not a production agent framework. It is a clean, developer-grade SDK foundation for experimenting with memory architecture using only the Python standard library in v0.1.

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

For the full flow, run:

```bash
python examples/memory_lifecycle_demo.py
```

This demo walks through storing memories, retrieving relevant context, correcting stale information, forgetting temporary state, and inspecting audit events.

## Developer-grade status

This repo has moved beyond a pure portfolio demo and is now being hardened as a developer-grade SDK foundation.

Current developer-grade signals:

- installable Python package
- public API reference
- typed package marker through `py.typed`
- Ruff linting in CI
- GitHub Actions test matrix for Python 3.10, 3.11, and 3.12
- custom SDK exceptions
- retrieval trace API for inspectable ranking behavior
- memory evaluation harness and benchmark runner
- integrated task-agent demo
- JSON and SQLite persistence tests
- policy, correction, forgetting, expiry, and serialization tests
- release checklist, security notes, contributor docs, issue templates, and PR template

Still not production-grade:

- no encryption layer
- no migration system
- no concurrency guarantees
- no semantic/vector retrieval adapters
- no stable backward-compatibility policy yet
- no published package release workflow yet

See [Developer-Grade Hardening](docs/developer_grade_hardening.md) and [Production Readiness](docs/production_readiness.md) for the maturity roadmap.

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
python examples/memory_lifecycle_demo.py
python examples/task_agent_demo.py
```

Recommended first demo:

```bash
python examples/task_agent_demo.py
```

## Documentation

| Document | Purpose |
|---|---|
| [API Reference](docs/api_reference.md) | Public SDK API and usage notes. |
| [Architecture](docs/architecture.md) | How the memory components fit together. |
| [Memory Lifecycle](docs/memory_lifecycle.md) | How memories move through remember, retrieve, correct, forget, and audit stages. |
| [Memory Lifecycle Diagram](docs/memory_lifecycle_diagram.md) | Visual ASCII diagram of the memory loop and where each primitive fits. |
| [Retrieval Diagnostics](docs/retrieval_diagnostics.md) | How retrieval scoring works and how to debug unexpected results. |
| [Retrieval Trace API](docs/retrieval_trace_api.md) | How to inspect candidates, scores, rejection reasons, and traced retrieval events. |
| [Evaluation Harness](docs/evaluation_harness.md) | How to define memory scenarios and evaluate expected retrieval behavior. |
| [Benchmarks](docs/benchmarks.md) | How to run benchmark scenarios and interpret results. |
| [Task Agent Demo](docs/task_agent_demo.md) | How the SDK works inside a small inspectable agent loop. |
| [Comparison](docs/comparison.md) | How this approach compares to chat history, prompt stuffing, vector memory, and full agent platforms. |
| [Production Readiness](docs/production_readiness.md) | Current maturity, gaps, and roadmap toward production-grade use. |
| [Developer-Grade Hardening](docs/developer_grade_hardening.md) | Maturity path from portfolio-grade repo to reusable developer tool. |
| [Release Checklist](docs/release_checklist.md) | Release validation steps, versioning guidance, and release note template. |
| [Repo Audit](docs/repo_audit.md) | Current status, completed areas, limitations, and next roadmap items. |
| [Roadmap](docs/roadmap.md) | Planned future improvements. |
| [Results](RESULTS.md) | Validation outputs and what the current examples prove. |
| [Changelog](CHANGELOG.md) | Version history and shipped changes. |
| [Contributing](CONTRIBUTING.md) | Local setup, contribution expectations, and project boundaries. |
| [Contributor Norms](CONTRIBUTOR_NORMS.md) | Collaboration style, project boundaries, and contribution principles. |
| [Security](SECURITY.md) | Security scope, sensitive data guidance, and production hardening notes. |

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
| `RetrievalTrace` | Diagnostic object for inspecting retrieval candidates, scores, and rejection reasons. |
| `EvaluationScenario` | Declarative scenario object for testing expected memory retrieval behavior. |
| Retrieval helpers | Keyword overlap, recency, importance, and tag-based filtering. |
| Correction helpers | Supersede old memory records while preserving history. |
| Forgetting helpers | Soft-delete memories by id, text match, tag, or expiry. |
| Audit events | Track created, retrieved, corrected, forgotten, and expired memory operations. |

## Design principles

- **Standard library first:** no LangChain, OpenAI API, vector database, or hosted service dependency in v0.1.
- **Readable over clever:** each primitive should be understandable by agent builders.
- **Lifecycle-aware:** memory is not just storage; it needs retrieval, correction, forgetting, and auditability.
- **Framework-neutral:** the SDK should be usable from any agent loop or application.
- **Honest maturity:** developer-grade hardening is underway, but production-readiness is still explicitly scoped as future work.

## Current status

This repo is an experimental SDK foundation for demonstrating memory architecture. It is suitable for learning, local experiments, developer exploration, and extension into future integrations. It is not yet hardened for production scale, concurrent writes, distributed storage, or sensitive data governance.

## Tests

```bash
pytest
python benchmarks/run_benchmarks.py
```

## Roadmap

- Add richer policy hooks for custom memory filtering.
- Add deterministic summarization helpers.
- Add import/export utilities for memory records and audit logs.
- Expand the memory evaluation harness into multi-step benchmark scenarios.
- Add optional adapter interfaces for embeddings and vector stores later, while keeping the core dependency-free.
