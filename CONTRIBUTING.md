# Contributing

Thank you for considering a contribution to `memory-agent-sdk`.

## Project purpose

`memory-agent-sdk` provides lightweight, reusable memory primitives for AI agent developers. The goal is to make memory lifecycle concepts easy to inspect and extend: session memory, long-term memory, retrieval, correction, forgetting, policies, and audit events.

This is a portfolio-grade developer tooling SDK, not a production framework.

## Local setup

```bash
git clone https://github.com/aditya89bh/memory-agent-sdk.git
cd memory-agent-sdk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

Run tests before pushing changes or opening a pull request.

## Adding examples

Examples live in `examples/` and should be runnable from the repository root:

```bash
python examples/example_name.py
```

Keep examples small and focused on one memory concept at a time. Prefer readable flows over clever abstractions.

## Adding memory primitives

When adding or changing memory primitives:

- keep the API small and explicit
- add tests for expected behavior
- preserve auditability where relevant
- document lifecycle behavior in plain language
- avoid coupling primitives to a specific agent framework

## Code style expectations

- Use only the Python standard library for core SDK code.
- Prefer simple functions and classes over complex abstractions.
- Keep modules readable and narrowly scoped.
- Use clear names for memory lifecycle concepts.
- Add comments only when they clarify non-obvious behavior.

## Commit discipline

Use one task per commit.

- Break work into clear tasks before editing.
- Make one separate commit per completed task.
- Do not bundle unrelated changes.
- Commit immediately after each task.
- Use clear commit messages.
- Run tests before final push.
- If tests fail, fix the failure in a separate commit.
- Push only after all task commits are complete and validation passes.

## What not to add yet

For v0.1, do not add:

- LLM API dependencies
- vector database integrations
- LangChain dependencies
- LlamaIndex dependencies
- production-readiness claims

The core should remain lightweight, framework-neutral, and standard-library first.
