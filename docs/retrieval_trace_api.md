# Retrieval Trace API

Retrieval traces make memory retrieval inspectable.

`Memory.retrieve()` returns matching memories. `Memory.retrieve_trace()` returns the same result set plus diagnostic information about what was considered, scored, rejected, and returned.

## Basic Usage

```python
from memory_agent_sdk import Memory

memory = Memory()

memory.remember(
    "User prefers concise answers.",
    tags=["preference"],
    importance=0.9,
)

trace = memory.retrieve_trace("concise answers", tags=["preference"])

print(trace.query)
print(trace.candidates_seen)
print(trace.candidates_scored)
print(trace.results)
print(trace.rejected)
```

## `Memory.retrieve_trace(query, tags=None, limit=5)`

Runs retrieval and returns a `RetrievalTrace` object.

Like `retrieve()`, it:

1. Expires outdated memories.
2. Loads active records from the store.
3. Applies tag filtering.
4. Scores matching records.
5. Returns the top results.
6. Records a `MEMORY_RETRIEVED` audit event.

Unlike `retrieve()`, it also exposes diagnostic metadata.

## `RetrievalTrace`

`RetrievalTrace` contains:

| Field | Meaning |
|---|---|
| `query` | Query string used for retrieval. |
| `requested_tags` | Tags requested by the caller. |
| `candidates_seen` | Number of memory records considered. |
| `candidates_scored` | Number of candidates that passed filters and were scored. |
| `results` | Ranked `RetrievalResult` objects returned by retrieval. |
| `rejected` | Records skipped during retrieval, with reasons. |

## `RetrievalResult`

Each result includes:

| Field | Meaning |
|---|---|
| `record` | Original `MemoryRecord`. |
| `score` | Combined retrieval score. |
| `keyword_score` | Query-to-memory keyword overlap score. |
| `recency_score` | Recency contribution. |
| `importance_score` | Importance contribution. |
| `text` | Convenience property for `record.text`. |
| `id` | Convenience property for `record.id`. |

## Rejection Reasons

The trace can include rejected records with reasons such as:

| Reason | Meaning |
|---|---|
| `deleted` | Memory was forgotten or otherwise marked deleted. |
| `expired` | Memory had expired. |
| `tag_mismatch` | Memory did not include all requested tags. |
| `no_keyword_overlap` | Query did not overlap with the memory text and no tag filter was supplied. |

## Example Debug Session

```python
trace = memory.retrieve_trace("concise answers", tags=["preference"])

for result in trace.results:
    print(result.text)
    print("score", result.score)
    print("keyword", result.keyword_score)
    print("recency", result.recency_score)
    print("importance", result.importance_score)

for rejected in trace.rejected:
    print(rejected["id"], rejected["reason"])
```

## When to Use `retrieve()` vs `retrieve_trace()`

Use `retrieve()` when the agent only needs results.

Use `retrieve_trace()` when you are:

- debugging retrieval behavior
- writing tests
- explaining why a memory was or was not returned
- inspecting scoring behavior
- building evaluation tools

## Audit Events

`retrieve_trace()` records a normal `MEMORY_RETRIEVED` event.

The event details include:

- `query`
- `result_ids`
- `trace: True`

This makes traced retrieval visible in the audit log without introducing a separate event type.

## Current Limitations

The trace object is intentionally simple.

It does not yet include:

- query tokens
- full per-candidate score breakdown for rejected records
- configurable scoring weights
- semantic similarity diagnostics
- vector retrieval diagnostics

Those are future developer-grade or production-grade improvements.
