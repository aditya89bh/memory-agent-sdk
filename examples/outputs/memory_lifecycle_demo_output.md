# Memory Lifecycle Demo Output

This file documents the expected output shape for:

```bash
python examples/memory_lifecycle_demo.py
```

The exact memory IDs are generated dynamically and will differ between runs.

## Expected Output Shape

```text
Memory Agent SDK: Lifecycle Demo
================================

Stored Memories
  - User prefers concise technical explanations.
    id=<generated-memory-id>
    tags=['preference', 'communication']
    importance=0.9
    status=active
  - User is building a reusable SDK for agent memory primitives.
    id=<generated-memory-id>
    tags=['project', 'sdk', 'agent-memory']
    importance=0.95
    status=active
  - Temporary note: validate the local demo output before committing.
    id=<generated-memory-id>
    tags=['temporary', 'validation']
    importance=0.3
    status=active

Retrieved Memories
  - <retrieved memory records ranked by relevance, recency, importance, and tags>

Corrected Memory
  - User prefers concise explanations with concrete engineering tradeoffs.
    id=<generated-memory-id>
    tags=['preference', 'communication']
    importance=0.95
    status=active

Retrieval After Forgetting Temporary Memory
  - <remaining non-forgotten records>

Audit Events
  - memory_created: memory_id=<generated-memory-id>, details={...}
  - memory_created: memory_id=<generated-memory-id>, details={...}
  - memory_created: memory_id=<generated-memory-id>, details={...}
  - memory_retrieved: memory_id=None, details={...}
  - memory_corrected: memory_id=<generated-memory-id>, details={...}
  - memory_forgotten: memory_id=<generated-memory-id>, details={...}
  - memory_retrieved: memory_id=None, details={...}

Lifecycle Summary
  observe -> decide -> store -> retrieve -> use -> correct -> forget -> audit
```

## What This Demonstrates

The lifecycle demo shows that the SDK can express a complete memory workflow:

1. Store durable memory records.
2. Retrieve relevant records for an agent query.
3. Correct stale or incomplete memory.
4. Forget temporary memory using tags.
5. Inspect audit events for memory operations.

## Notes

This is documentation of the expected output shape, not a frozen snapshot. Generated IDs and event details may vary across runs.
