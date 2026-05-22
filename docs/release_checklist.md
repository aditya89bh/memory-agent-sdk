# Release Checklist

This checklist keeps Memory Agent SDK releases small, verifiable, and honest.

The project is currently experimental, so releases should avoid production-readiness claims unless the implementation and validation support them.

## Before Cutting a Release

- [ ] Confirm the release scope is clear.
- [ ] Confirm each task was committed separately.
- [ ] Confirm README reflects the current package behavior.
- [ ] Confirm API documentation matches the implementation.
- [ ] Confirm examples still run locally.
- [ ] Confirm tests pass locally with `pytest`.
- [ ] Confirm GitHub Actions CI is green.
- [ ] Confirm `CHANGELOG.md` is updated.
- [ ] Confirm `RESULTS.md` is still accurate.
- [ ] Confirm production-readiness language is honest.

## Version Scope

Use small version increments.

| Version Type | Use When |
|---|---|
| Patch | Docs fixes, small bug fixes, test improvements. |
| Minor | New memory primitives, new stores, new examples, new public APIs. |
| Major | Breaking public API changes. |

## Documentation Checks

Before release, check:

- [ ] `README.md`
- [ ] `docs/api_reference.md`
- [ ] `docs/architecture.md`
- [ ] `docs/memory_lifecycle.md`
- [ ] `docs/memory_lifecycle_diagram.md`
- [ ] `docs/retrieval_diagnostics.md`
- [ ] `docs/comparison.md`
- [ ] `docs/production_readiness.md`
- [ ] `docs/roadmap.md`
- [ ] `CONTRIBUTING.md`
- [ ] `CONTRIBUTOR_NORMS.md`
- [ ] `SECURITY.md`

## Validation Commands

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python examples/basic_session_memory.py
python examples/retrieval_demo.py
python examples/correction_demo.py
python examples/forgetting_demo.py
python examples/agent_loop_demo.py
python examples/memory_lifecycle_demo.py
```

## Release Notes Template

```markdown
## vX.Y.Z

### Added

- 

### Changed

- 

### Fixed

- 

### Validation

- `pytest` passed
- GitHub Actions CI passed
- Relevant examples were run

### Known Limitations

- 
```

## Release Principle

A release should make the SDK easier to trust.

That means clear scope, passing validation, accurate documentation, and no inflated claims.
