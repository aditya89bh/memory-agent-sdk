from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .memory import Memory
from .policies import MemoryPolicy


@dataclass
class EvaluationScenario:
    name: str
    query: str
    memories: list[dict]
    expected_result_texts: list[str] = field(default_factory=list)
    tags: list[str] | None = None
    policy: MemoryPolicy | None = None
    limit: int = 5


@dataclass
class EvaluationResult:
    scenario_name: str
    passed: bool
    expected_result_texts: list[str]
    actual_result_texts: list[str]
    missing_result_texts: list[str]
    unexpected_result_texts: list[str]


@dataclass
class EvaluationReport:
    results: list[EvaluationResult]

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for result in self.results if result.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def success_rate(self) -> float:
        return 0.0 if self.total == 0 else self.passed / self.total


def evaluate_scenario(
    scenario: EvaluationScenario,
    memory_factory: Callable[[], Memory] | None = None,
) -> EvaluationResult:
    memory = memory_factory() if memory_factory is not None else Memory(policy=scenario.policy)

    for item in scenario.memories:
        memory.remember(
            item["text"],
            tags=item.get("tags"),
            importance=item.get("importance", 0.5),
            metadata=item.get("metadata"),
            expires_at=item.get("expires_at"),
        )

    results = memory.retrieve(scenario.query, tags=scenario.tags, limit=scenario.limit)
    actual = [result.text for result in results]
    expected = list(scenario.expected_result_texts)

    missing = [text for text in expected if text not in actual]
    unexpected = [text for text in actual if text not in expected]

    return EvaluationResult(
        scenario_name=scenario.name,
        passed=not missing and not unexpected,
        expected_result_texts=expected,
        actual_result_texts=actual,
        missing_result_texts=missing,
        unexpected_result_texts=unexpected,
    )


def evaluate_scenarios(
    scenarios: list[EvaluationScenario],
    memory_factory: Callable[[], Memory] | None = None,
) -> EvaluationReport:
    return EvaluationReport(
        results=[evaluate_scenario(scenario, memory_factory=memory_factory) for scenario in scenarios]
    )
