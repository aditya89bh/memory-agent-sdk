# Changelog

## v0.1.0 - Initial SDK foundation

- Added the core `Memory` API with `remember()`, `retrieve()`, `correct()`, `forget()`, and `events()`.
- Added `SessionMemory` for short-lived conversational turn tracking and summaries.
- Added local store implementations: `InMemoryStore`, `JSONStore`, and `SQLiteStore`.
- Added retrieval support using keyword overlap, recency score, importance score, and tag filtering.
- Added correction support for updating memories by id or text match while preserving superseded history.
- Added forgetting support by id, text match, tag, and expiry with soft-delete behavior.
- Added audit events for memory creation, retrieval, correction, forgetting, and expiry.
- Added runnable examples for session memory, retrieval, correction, forgetting, and a simple agent loop.
- Added pytest coverage for session memory, retrieval, correction, forgetting, and policies.
- Added GitHub Actions CI for Python 3.10, 3.11, and 3.12.
- Added `RESULTS.md` with local validation output for tests and examples.
