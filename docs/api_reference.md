# API Reference

This document describes the public API currently implemented in `memory-agent-sdk`.

## Memory

`Memory` is the high-level interface for long-term memory operations.

```python
from memory_agent_sdk import Memory

memory = Memory()
```

### `Memory(store=None, policy=None)`

Creates a memory manager.

- `store`: optional store instance. Defaults to `InMemoryStore()`.
- `policy`: optional `MemoryPolicy`. Defaults to `MemoryPolicy()`.

### `remember(text, tags=None, importance=0.5, metadata=None, expires_at=None)`

Stores a memory if the active policy allows it.

Returns a `MemoryRecord`, or `None` if the policy ignores the memory.

```python
record = memory.remember(
    "User prefers concise answers",
    tags=["preference"],
    importance=0.9,
)
```

Parameters currently implemented:

- `text`: memory text.
- `tags`: optional list of string tags.
- `importance`: numeric importance score.
- `metadata`: optional dictionary.
- `expires_at`: optional `datetime` for expiry.

A `MEMORY_CREATED` audit event is recorded when a memory is saved.

### `retrieve(query, tags=None, limit=5)`

Retrieves matching active memories.

```python
results = memory.retrieve("concise answers", tags=["preference"])
```

Returns a list of `RetrievalResult` objects. Retrieval also expires outdated memories before searching and records a `MEMORY_RETRIEVED` event.

### `retrieve_trace(query, tags=None, limit=5)`

Runs retrieval and returns diagnostic metadata with the ranked results.

```python
trace = memory.retrieve_trace("concise answers", tags=["preference"])

print(trace.candidates_seen)
print(trace.candidates_scored)
print(trace.results)
print(trace.rejected)
```

Returns a `RetrievalTrace` object with:

- `query`: query string used for retrieval.
- `requested_tags`: tags requested by the caller.
- `candidates_seen`: number of memory records considered.
- `candidates_scored`: number of candidates that passed filters and were scored.
- `results`: ranked `RetrievalResult` objects.
- `rejected`: skipped records with rejection reasons.

A traced retrieval records a normal `MEMORY_RETRIEVED` audit event with `trace: True` in event details.

### `correct(new_text, memory_id=None, text_match=None, tags=None, importance=None)`

Corrects an existing memory by id or by text match.

```python
corrected = memory.correct(
    memory_id=record.id,
    new_text="User prefers concise Python examples",
)
```

Current behavior:

- finds the old memory by `memory_id` or `text_match`
- creates a new memory record with `new_text`
- marks the previous memory as `SUPERSEDED`
- sets `superseded_by` on the previous memory
- adds `corrects` metadata to the new memory
- records a `MEMORY_CORRECTED` audit event

Raises `MemoryNotFoundError` if no matching memory is found.

### `forget(memory_id=None, text_match=None, tag=None, soft_delete=True)`

Forgets memories by id, text match, or tag.

```python
memory.forget(tag="temporary")
```

Current behavior marks matching memories as `FORGOTTEN` and records `MEMORY_FORGOTTEN` audit events. The `soft_delete` parameter is recorded in event details, but the current implementation uses status-based soft deletion.

Raises `MemoryInputError` if no selector is provided.

### `events()`

Returns audit events from the active store.

```python
for event in memory.events():
    print(event.type, event.memory_id)
```

## RetrievalResult

`RetrievalResult` represents one ranked retrieval result.

Fields:

- `record`: original `MemoryRecord`.
- `score`: combined retrieval score.
- `keyword_score`: query-to-memory keyword overlap score.
- `recency_score`: recency contribution.
- `importance_score`: importance contribution.
- `text`: convenience property for `record.text`.
- `id`: convenience property for `record.id`.

## RetrievalTrace

`RetrievalTrace` represents a traced retrieval run.

Fields:

- `query`
- `requested_tags`
- `candidates_seen`
- `candidates_scored`
- `rejected`
- `results`

Rejected entries are dictionaries with:

- `id`: memory id.
- `reason`: rejection reason.

Current rejection reasons include:

- `deleted`
- `expired`
- `tag_mismatch`
- `no_keyword_overlap`

## SessionMemory

`SessionMemory` tracks short-lived conversational turns.

```python
from memory_agent_sdk import SessionMemory

session = SessionMemory()
```

### `add_turn(role, content)`

Adds a session turn and returns a `SessionTurn`.

```python
session.add_turn("user", "Remember that I prefer concise answers.")
```

### `get_turns()`

Returns a list of session turns.

```python
turns = session.get_turns()
```

### `summarize(max_turns=None)`

Returns a newline-separated text summary of turns.

```python
summary = session.summarize(max_turns=3)
```

If `max_turns` is omitted, all turns are included.

## Stores

Stores implement persistence for memory records and audit events.

### `InMemoryStore`

Ephemeral in-process store for tests and demos.

```python
from memory_agent_sdk import Memory, InMemoryStore

memory = Memory(store=InMemoryStore())
```

Records and events are lost when the process exits.

### `JSONStore`

File-backed JSON store.

```python
from memory_agent_sdk import Memory, JSONStore

memory = Memory(store=JSONStore("memory.json"))
```

The JSON file stores both records and audit events.

### `SQLiteStore`

SQLite-backed local store.

```python
from memory_agent_sdk import Memory, SQLiteStore

memory = Memory(store=SQLiteStore("memory.db"))
```

The current implementation creates `memories` and `events` tables automatically.

## Retrieval behavior

Retrieval is deterministic and local. It does not use embeddings, vector databases, or external APIs.

Current scoring uses:

- keyword overlap between query and memory text
- recency score based on memory creation time
- importance score from the memory record
- optional tag filtering

When tags are provided, returned memories must contain all requested tags.

Expired, forgotten, and otherwise deleted memories are excluded.

Use `retrieve_trace()` when you need to inspect candidates, score fields, and rejection reasons.

## Correction behavior

Correction preserves history rather than overwriting in place.

The previous memory is marked `SUPERSEDED`, and the new memory stores metadata linking back to the corrected memory id.

Correction can target:

- exact memory id
- first active memory containing a text match

## Forgetting behavior

Forgetting is status-based soft deletion.

Supported selectors:

- memory id
- text match
- tag
- expired memories through `forget_expired()` internally

Forgotten memories are excluded from normal store `.all()` results unless `include_deleted=True` is used at the store level.

## MemoryPolicy

`MemoryPolicy` decides whether text should be remembered.

```python
from memory_agent_sdk import Memory, MemoryPolicy

policy = MemoryPolicy(allow_sensitive=False, ignore_small_talk=True)
memory = Memory(policy=policy)
```

Currently implemented flags:

- `allow_sensitive`: if `False`, ignores text containing simple sensitive terms such as password, API key, secret, token, or SSN.
- `remember_preferences`: if `False`, ignores memories tagged `preference`.
- `remember_tasks`: if `False`, ignores memories tagged `task`.
- `ignore_small_talk`: if `True`, ignores small-talk-only text such as hi, hello, hey, thanks, ok, and okay.

Methods:

- `should_ignore(text, tags=None)`
- `should_remember(text, tags=None)`

## Exceptions

The package exposes SDK-specific exception classes:

- `MemoryAgentSDKError`: base exception for SDK errors.
- `MemoryInputError`: invalid memory operation input.
- `MemoryNotFoundError`: requested memory record could not be found.

Example:

```python
from memory_agent_sdk import Memory, MemoryNotFoundError

memory = Memory()

try:
    memory.correct(memory_id="missing", new_text="Updated memory")
except MemoryNotFoundError:
    print("No matching memory found")
```

## Audit events

Audit events are represented by `AuditEvent` and typed with `EventType`.

Currently implemented event types:

- `MEMORY_CREATED`
- `MEMORY_RETRIEVED`
- `MEMORY_CORRECTED`
- `MEMORY_FORGOTTEN`
- `MEMORY_EXPIRED`

Events include:

- `type`
- `memory_id`
- `details`
- `id`
- `created_at`

Example:

```python
memory.remember("User prefers concise answers", tags=["preference"])

for event in memory.events():
    print(event.type.value, event.memory_id, event.details)
```
