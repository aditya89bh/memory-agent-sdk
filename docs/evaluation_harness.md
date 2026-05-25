# Memory Evaluation Harness

Memory Agent SDK includes a small evaluation harness for checking whether memory behavior matches expected outcomes.

The goal is not to create a full benchmark suite yet. The goal is to give developers a lightweight way to define memory scenarios, run them, and inspect pass/fail results.

## Why This Exists

Agent memory systems need more than demos.

A demo shows that memory works once. An evaluation harness helps answer whether memory behavior keeps working across repeated scenarios.

This is useful for checking:

- retrieval behavior
- tag filtering
- expected memory recall
- missing results
- unexpected results
- policy-driven memory behavior
- future correction and forgetting scenarios

## Basic Example

```python
from memory_agent_sdk import EvaluationScenario, evaluate_scenario

scenario = EvaluationScenario(
    name="preference retrieval",
    query="concise answers",
    tags=["preference"],
    memories=[
        {
            "text": "User prefers concise answers",
            "tags": ["preference"],
            "importance": 0.9,
        },
        {
            "text": "Use pytest for tests",
            "tags": ["project"],
            "importance": 0.9,
        },
    ],
    expected_result_texts=["User prefers concise answers"],
)

result = evaluate_scenario(scenario)

print(result.passed)
print(result.actual_result_texts)
print(result.missing_result_texts)
print(result.unexpected_result_texts)
```

## EvaluationScenario

`EvaluationScenario` defines one memory behavior test case.

| Field | Purpose |
|---|---|
| `name` | Human-readable scenario name. |
| `query` | Retrieval query to run. |
| `memories` | Memory records to seed before retrieval. |
| `expected_result_texts` | Exact result texts expected from retrieval. |
| `tags` | Optional retrieval tags. |
| `policy` | Optional `MemoryPolicy` for the scenario. |
| `limit` | Retrieval result limit. Defaults to `5`. |

Each item in `memories` is a dictionary that can include:

| Key | Purpose |
|---|---|
| `text` | Memory text. Required. |
| `tags` | Optional memory tags. |
| `importance` | Optional importance score. Defaults to `0.5`. |
| `metadata` | Optional metadata dictionary. |
| `expires_at` | Optional expiry datetime. |

## EvaluationResult

`EvaluationResult` describes one scenario result.

| Field | Purpose |
|---|---|
| `scenario_name` | Name of the scenario. |
| `passed` | Whether actual results exactly matched expected results. |
| `expected_result_texts` | Expected retrieval result texts. |
| `actual_result_texts` | Actual retrieval result texts. |
| `missing_result_texts` | Expected texts that were not returned. |
| `unexpected_result_texts` | Returned texts that were not expected. |

## EvaluationReport

`EvaluationReport` aggregates multiple scenario results.

It exposes:

| Property | Purpose |
|---|---|
| `total` | Number of scenarios evaluated. |
| `passed` | Number of passing scenarios. |
| `failed` | Number of failing scenarios. |
| `success_rate` | Passing scenarios divided by total scenarios. |

## Evaluating Multiple Scenarios

```python
from memory_agent_sdk import EvaluationScenario, evaluate_scenarios

scenarios = [
    EvaluationScenario(
        name="project retrieval",
        query="pytest",
        memories=[{"text": "Use pytest for tests", "tags": ["project"]}],
        expected_result_texts=["Use pytest for tests"],
    ),
    EvaluationScenario(
        name="preference retrieval",
        query="concise answers",
        tags=["preference"],
        memories=[{"text": "User prefers concise answers", "tags": ["preference"]}],
        expected_result_texts=["User prefers concise answers"],
    ),
]

report = evaluate_scenarios(scenarios)

print(report.total)
print(report.passed)
print(report.failed)
print(report.success_rate)
```

## Using a Custom Memory Factory

Both `evaluate_scenario()` and `evaluate_scenarios()` accept an optional `memory_factory`.

This lets developers evaluate behavior against custom stores or custom `Memory` configuration.

```python
from memory_agent_sdk import EvaluationScenario, Memory, SQLiteStore, evaluate_scenario

scenario = EvaluationScenario(
    name="sqlite retrieval",
    query="persistent memory",
    memories=[{"text": "SQLite stores persistent memory", "tags": ["storage"]}],
    expected_result_texts=["SQLite stores persistent memory"],
)

result = evaluate_scenario(
    scenario,
    memory_factory=lambda: Memory(store=SQLiteStore(":memory:")),
)
```

## Current Scope

The v0.1 evaluation harness focuses on retrieval result matching.

It currently checks:

- which memories were returned
- which expected memories were missing
- which unexpected memories appeared
- aggregate pass/fail rates

## Current Limitations

The harness does not yet evaluate:

- correction sequences
- forgetting sequences
- expiry sequences
- trace-level scoring assertions
- latency or performance
- semantic retrieval quality
- multi-step agent workflows

Those are future extensions.

## Future Direction

Future versions could add:

- JSON scenario files
- benchmark runners
- score breakdown reports
- retrieval trace evaluation
- correction and forgetting scenario steps
- CLI command for running evaluations
- result export to JSON or Markdown

## Design Principle

Memory should be evaluated as behavior, not just stored as data.

The harness gives developers a first step toward repeatable checks for memory quality without introducing external services or framework dependencies.
