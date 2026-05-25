from __future__ import annotations

import json
import sys
from pathlib import Path

from memory_agent_sdk import EvaluationScenario, evaluate_scenarios


SCENARIO_DIR = Path(__file__).parent / "scenarios"


def load_scenario(path: Path) -> EvaluationScenario:
    data = json.loads(path.read_text())
    return EvaluationScenario(
        name=data["name"],
        query=data["query"],
        memories=data["memories"],
        expected_result_texts=data.get("expected_result_texts", []),
        tags=data.get("tags"),
        limit=data.get("limit", 5),
    )


def load_scenarios() -> list[EvaluationScenario]:
    return [load_scenario(path) for path in sorted(SCENARIO_DIR.glob("*.json"))]


def main() -> int:
    scenarios = load_scenarios()
    report = evaluate_scenarios(scenarios)

    print("Memory benchmark report")
    print(f"total: {report.total}")
    print(f"passed: {report.passed}")
    print(f"failed: {report.failed}")
    print(f"success_rate: {report.success_rate:.2f}")
    print()

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.scenario_name}")
        if not result.passed:
            print(f"  expected: {result.expected_result_texts}")
            print(f"  actual: {result.actual_result_texts}")
            print(f"  missing: {result.missing_result_texts}")
            print(f"  unexpected: {result.unexpected_result_texts}")

    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
