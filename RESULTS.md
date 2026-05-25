# Validation Results

This document captures validation evidence for `memory-agent-sdk`.

## Install validation

The package installs in editable development mode with:

```bash
pip install -e ".[dev]"
```

## Test validation

Command:

```bash
pytest
```

Current CI runs the test suite across Python 3.10, 3.11, and 3.12.

The suite covers:

- session memory
- retrieval
- retrieval traces
- correction
- forgetting
- expiry
- memory policies
- custom exceptions
- JSON and SQLite persistence
- store serialization
- evaluation harness behavior

## Benchmark validation

Command:

```bash
python benchmarks/run_benchmarks.py
```

Observed local output:

```text
Memory benchmark report
total: 5
passed: 5
failed: 0
success_rate: 1.00

[PASS] policy_small_talk_memory
[PASS] retrieval_preference
[PASS] retrieval_project_memory
[PASS] retrieval_robotics_memory
[PASS] tag_filter_project_memory
```

Snapshot file:

```text
benchmarks/results/latest_results.json
```

Current benchmark coverage includes:

- small-talk policy filtering
- preference retrieval
- project memory retrieval
- robotics memory retrieval
- tag-based filtering

## Runnable examples

The repo includes runnable examples for:

- basic session memory
- retrieval
- correction
- forgetting
- agent loop usage
- full memory lifecycle demo

## What this proves

- The package imports correctly from an editable install.
- Memory records can be stored, retrieved, corrected, forgotten, expired, and audited.
- Retrieval behavior can be inspected with trace objects.
- JSON and SQLite persistence are covered by tests.
- Benchmark scenarios are runnable and CI-backed.
- The repo now has developer-grade validation beyond simple examples.

## Current limitations

- Retrieval is keyword, recency, importance, and tag based, not semantic/vector based.
- Stores are lightweight local implementations, not distributed production stores.
- SQLite support is suitable for local experiments, not high-concurrency workloads.
- Audit events are local SDK events, not external observability integrations.
- Benchmark scenarios currently validate retrieval-style outcomes, not full multi-step agent workflows.
- No external agent framework integrations are included yet.
