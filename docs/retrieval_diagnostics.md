# Retrieval Diagnostics

Memory Agent SDK uses a simple, inspectable retrieval model in v0.1.

The goal is not to hide ranking behind a black box. The goal is to make it clear why a memory was returned, why another memory was ignored, and what developers can improve later.

## Retrieval Flow

When `Memory.retrieve()` is called, the SDK:

1. Expires outdated memories.
2. Loads active records from the store.
3. Applies optional tag filtering.
4. Computes keyword overlap with the query.
5. Computes a recency score.
6. Reads the memory importance score.
7. Combines the scores into a final ranking.
8. Returns the top results.
9. Records a `MEMORY_RETRIEVED` audit event.

## Scoring Components

### Keyword Overlap

The query and memory text are tokenized into lowercase words.

A keyword score is computed from the overlap between query tokens and memory tokens.

This favors memories that directly match the user's current query.

### Recency Score

Recent memories receive a higher recency score.

The score decays as a memory gets older. This gives newer context more influence while still allowing older high-importance memories to be retrieved.

### Importance Score

Each memory can be stored with an `importance` value.

Higher-importance memories receive a stronger ranking boost.

This is useful for preferences, durable project facts, safety constraints, or long-term agent instructions.

### Tag Filtering

Retrieval can be restricted with tags.

For example:

```python
memory.retrieve("communication style", tags=["preference"])
```

This only returns memories that include the requested tag.

## Current Ranking Formula

The v0.1 retrieval score combines:

- keyword overlap
- recency
- importance

The current weighting favors keyword relevance first, then importance, then recency.

This keeps retrieval predictable and easy to debug.

## Why a Memory May Not Be Returned

A memory may be skipped if:

- it has been forgotten
- it has expired
- it does not match required tags
- it has no keyword overlap with the query
- it falls below the top result limit

This is intentional. The SDK avoids returning unrelated memories just because they exist.

## Debugging Retrieval Behavior

If retrieval returns unexpected results, check:

1. Does the memory text share keywords with the query?
2. Is the memory still active?
3. Has the memory expired?
4. Was the memory forgotten?
5. Are required tags too restrictive?
6. Is the memory importance too low?
7. Is the result limit too small?
8. Are there audit events confirming retrieval occurred?

## Example

```python
from memory_agent_sdk import Memory

memory = Memory()

memory.remember(
    "User prefers concise technical explanations.",
    tags=["preference", "communication"],
    importance=0.9,
)

results = memory.retrieve(
    "How should I explain this technical concept?",
    tags=["preference"],
)

for result in results:
    print(result.text)
```

## Current Limitations

Retrieval in v0.1 is intentionally simple.

Current limitations:

- no embeddings
- no semantic similarity
- no vector store adapters
- no query expansion
- no retrieval tracing object yet
- no per-result score explanation in the public API yet
- no benchmark suite for retrieval quality yet

These are roadmap items, not missing accidents.

## Future Diagnostics Roadmap

Future versions could add:

- retrieval trace objects
- per-result score breakdowns
- query token inspection
- rejected-memory explanations
- retrieval quality tests
- embedding adapter interfaces
- vector store adapters
- memory evaluation harnesses

## Design Position

Retrieval should be inspectable before it becomes sophisticated.

A simple retrieval system that developers can understand is more useful for early agent architecture work than a complex black box that silently injects stale or irrelevant memories.
