# Memory Lifecycle Diagram

Memory Agent SDK treats memory as a lifecycle, not a passive log.

A useful agent memory system should be able to decide what to store, retrieve relevant context, repair stale information, forget intentionally, and expose what happened through audit events.

## High-Level Loop

```text
+-------------------------+
| User / Agent Interaction|
+------------+------------+
             |
             v
+-------------------------+
| Observe Context         |
| message, task, outcome  |
+------------+------------+
             |
             v
+-------------------------+
| Memory Policy           |
| remember or ignore?     |
+------------+------------+
             |
             v
+-------------------------+
| Store Memory            |
| InMemory / JSON / SQLite|
+------------+------------+
             |
             v
+-------------------------+
| Retrieve Memory         |
| keyword, recency,       |
| importance, tags        |
+------------+------------+
             |
             v
+-------------------------+
| Use in Agent Context    |
| decision support        |
+------------+------------+
             |
             v
+-------------------------+
| Correct / Forget        |
| supersede, expire,      |
| soft delete             |
+------------+------------+
             |
             v
+-------------------------+
| Audit Events            |
| created, retrieved,     |
| corrected, forgotten    |
+------------+------------+
             |
             v
        back to loop
```

## Lifecycle Stages

| Stage | Purpose | SDK Concept |
|---|---|---|
| Observe | Receive new context from an interaction, task, or agent outcome. | Agent/app code |
| Decide | Determine whether the information should be stored or ignored. | `MemoryPolicy` |
| Store | Persist useful memory records. | `MemoryRecord`, `Store` |
| Retrieve | Bring relevant memory back into context. | `Memory.retrieve()` |
| Use | Let the agent apply retrieved context to its next decision. | Agent/app code |
| Correct | Replace stale or incorrect memory while preserving history. | `Memory.correct()` |
| Forget | Remove temporary, expired, or unwanted memory. | `Memory.forget()` |
| Audit | Record memory operations for inspection and debugging. | `AuditEvent` |

## Where Policies Fit

Policies sit before storage.

They answer questions like:

- Should this memory be stored?
- Is this just small talk?
- Is this a preference?
- Is this a task?
- Should sensitive content be ignored?

The policy layer prevents the memory store from becoming a junk drawer.

## Where Retrieval Fits

Retrieval sits between stored memory and agent context.

It decides which memories are worth bringing back for the current query.

In v0.1, retrieval uses:

- keyword overlap
- recency score
- importance score
- tag filtering

The design goal is inspectability before sophistication.

## Where Correction Fits

Correction exists because memory can become wrong.

A user may change preferences. A project fact may become stale. A previous assumption may be replaced by better information.

Correction should not simply erase history. In this SDK, corrected memories can supersede old records while preserving an audit trail.

## Where Forgetting Fits

Forgetting is not a failure. It is memory hygiene.

Forgetting helps remove:

- temporary notes
- expired facts
- stale preferences
- unwanted records
- noisy retrieval candidates

A memory system that only adds information eventually becomes a liability.

## Where Audit Events Fit

Audit events make memory behavior visible.

They help developers answer:

- What was remembered?
- What was retrieved?
- What was corrected?
- What was forgotten?
- Why did this agent have this context?

This is essential for debugging long-running agents.

## Current Implementation Scope

The current SDK supports the lifecycle through:

- `Memory.remember()`
- `Memory.retrieve()`
- `Memory.correct()`
- `Memory.forget()`
- `Memory.events()`
- `MemoryPolicy`
- `InMemoryStore`
- `JSONStore`
- `SQLiteStore`

It does not yet include production-grade tracing, distributed storage, vector retrieval, access control, or retention governance.

## Design Principle

Memory should behave like infrastructure.

It should have lifecycle controls, inspection points, and clear boundaries. Without those, agent memory becomes a pile of context that slowly drifts away from reality.
