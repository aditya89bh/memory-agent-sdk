# Production Readiness

## Current status

`memory-agent-sdk` is an experimental SDK for memory architecture exploration. It is not production-ready.

The project is intended to demonstrate clean, reusable memory primitives for agent builders: session memory, long-term memory, retrieval, correction, forgetting, policies, stores, and audit events. It is suitable for local experiments, portfolio work, learning, and early design exploration.

Do not use this as-is for sensitive production memory workloads.

## What is currently solid

- **Clear API shape:** the `Memory` API exposes explicit methods for remembering, retrieving, correcting, forgetting, and reading events.
- **Memory lifecycle primitives:** the SDK models the core lifecycle from creation to retrieval, correction, forgetting, expiry, and auditability.
- **Local persistence with JSON and SQLite:** `JSONStore` and `SQLiteStore` provide lightweight local persistence using the Python standard library.
- **Tests:** pytest coverage exists for session memory, retrieval, correction, forgetting, and policies.
- **CI:** GitHub Actions runs tests on Python 3.10, 3.11, and 3.12.
- **Runnable examples:** examples demonstrate session memory, retrieval, correction, forgetting, and a simple agent loop.

## What is not production-ready yet

- **No concurrency guarantees:** stores are not designed for concurrent writers or distributed workloads.
- **No migration system:** SQLite schema changes are not versioned or migrated.
- **No encryption/privacy controls:** memory records are stored in plaintext.
- **No access control:** there is no user, tenant, role, or permission model.
- **No async API:** all APIs are synchronous.
- **No scaling benchmarks:** behavior has not been measured at large memory volumes.
- **No vector store adapters:** retrieval is local and deterministic, without embedding/vector search integrations.
- **No memory evaluation harness:** retrieval and memory quality are not benchmarked across datasets.
- **Limited retrieval sophistication:** retrieval uses simple keyword, recency, importance, and tag scoring.

## Production readiness checklist

Before positioning this SDK as production-grade, the following areas need explicit work:

- **Storage durability:** define durability guarantees, backup behavior, corruption handling, and recovery paths.
- **Schema migrations:** add versioned migrations for persistent stores.
- **Privacy and retention policies:** support data minimization, retention windows, deletion guarantees, and sensitive-data handling.
- **Correction audit trail:** strengthen correction lineage and make audit trails queryable and exportable.
- **Observability:** add structured logs, metrics, traces, and operational diagnostics.
- **Retrieval quality evaluation:** create reproducible evaluation datasets and metrics for memory retrieval quality.
- **API stability:** define public API boundaries and compatibility promises.
- **Versioning:** publish semantic versioning rules and release notes.
- **Integration adapters:** add optional adapters for agent frameworks, vector stores, and external storage without bloating the core.
- **Security review:** review storage, serialization, privacy, and dependency boundaries.

## Roadmap from experimental to production-grade

### Phase 1: Harden local reliability

- Add store-level tests for persistence edge cases.
- Add SQLite migration support.
- Add export/import validation.
- Improve error handling for corrupt JSON and SQLite files.

### Phase 2: Improve auditability and evaluation

- Add a memory evaluation harness.
- Track retrieval quality across deterministic scenarios.
- Expand audit event querying.
- Add examples for correction and forgetting review workflows.

### Phase 3: Add privacy and policy controls

- Add configurable retention policies.
- Add sensitive-memory handling patterns.
- Add optional encryption hooks.
- Document safe handling of personal or confidential data.

### Phase 4: Prepare integration boundaries

- Stabilize public APIs.
- Add semantic versioning and compatibility notes.
- Add optional adapters while keeping the core standard-library first.
- Document integration patterns for agent loops and application services.

## Warning

This SDK should not be used as-is for production systems that store sensitive, personal, regulated, or business-critical memory. It currently lacks the privacy, security, durability, concurrency, and operational controls expected from production memory infrastructure.
