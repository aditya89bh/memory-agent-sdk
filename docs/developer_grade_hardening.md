# Developer-Grade Hardening Roadmap

Memory Agent SDK is currently a strong portfolio-grade repo and an experimental SDK foundation.

The next maturity target is developer-grade.

Developer-grade means the repo should be usable, understandable, validated, and extensible by other developers without relying on the original author for context.

It does not mean production-ready yet.

## Maturity Definitions

| Level | Meaning |
|---|---|
| Portfolio-grade | Clear thesis, working demos, tests, docs, CI, and strong presentation. |
| Developer-grade | Reusable package shape, stable public API direction, stronger tests, linting, typing, release discipline, and clear contribution boundaries. |
| Production-grade | Security hardening, migrations, concurrency guarantees, performance benchmarks, stable releases, backwards compatibility, and operational maturity. |

## Current Target

Current target: **developer-grade hardening**.

The goal is to make the SDK feel like a real developer tool while keeping the v0.1 scope small and inspectable.

## Developer-Grade Requirements

| Area | Requirement | Status |
|---|---|---|
| Package structure | Installable Python package | Done |
| Public API | Clear API surface documented | Done |
| Examples | Runnable examples for core flows | Done |
| Tests | Baseline unit and persistence tests | In progress |
| CI | Tests run on supported Python versions | Done |
| Linting | Automated style/static checks | Pending |
| Formatting | Consistent formatting rules | Pending |
| Typing | Type marker and stricter annotations | Pending |
| Error handling | Custom exceptions and predictable failures | Pending |
| Retrieval transparency | Trace objects and score breakdowns | Pending |
| Release discipline | Checklist and changelog | Done |
| Contribution flow | Templates and contributor docs | Done |

## Recommended Hardening Sequence

1. Add `ruff` for linting.
2. Add formatting rules through `ruff format`.
3. Add `py.typed` for typed package support.
4. Add custom exceptions for memory, store, retrieval, correction, and forgetting errors.
5. Add retrieval trace objects with score breakdowns.
6. Add tests for policy behavior.
7. Add tests for correction and forgetting edge cases.
8. Add tests for expired memory behavior.
9. Add benchmark/evaluation harness for memory scenarios.
10. Add one realistic integrated agent workflow demo.

## Not Yet Required

The following are production-grade concerns and should not block developer-grade maturity:

- encrypted storage
- distributed storage
- multi-user access control
- async APIs
- migration framework
- hosted service integration
- vector database adapters
- semantic retrieval
- package publishing automation

These can be planned, but they should not bloat v0.1.

## Developer-Grade Definition of Done

The repo can be considered developer-grade when:

- `pytest` passes in CI
- linting passes in CI
- package exports are typed with `py.typed`
- public errors are predictable
- retrieval behavior is inspectable
- core edge cases are tested
- docs match the implementation
- examples run without hidden setup
- contribution and release workflows are documented

## Principle

Developer-grade does not mean complicated.

It means another developer can clone the repo, understand the SDK, run it, extend it, and trust the basic engineering signals.
