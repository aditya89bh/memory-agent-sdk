from memory_agent_sdk import EvaluationScenario, evaluate_scenario, evaluate_scenarios


def test_evaluate_scenario_passes_when_expected_results_match():
    scenario = EvaluationScenario(
        name="preference retrieval",
        query="concise answers",
        tags=["preference"],
        memories=[
            {"text": "User prefers concise answers", "tags": ["preference"], "importance": 0.9},
            {"text": "Use pytest for tests", "tags": ["project"], "importance": 0.9},
        ],
        expected_result_texts=["User prefers concise answers"],
    )

    result = evaluate_scenario(scenario)

    assert result.passed is True
    assert result.scenario_name == "preference retrieval"
    assert result.actual_result_texts == ["User prefers concise answers"]
    assert result.missing_result_texts == []
    assert result.unexpected_result_texts == []


def test_evaluate_scenario_reports_missing_and_unexpected_results():
    scenario = EvaluationScenario(
        name="mismatch",
        query="concise answers",
        memories=[
            {"text": "User prefers concise answers", "tags": ["preference"]},
        ],
        expected_result_texts=["Different expected memory"],
    )

    result = evaluate_scenario(scenario)

    assert result.passed is False
    assert result.missing_result_texts == ["Different expected memory"]
    assert result.unexpected_result_texts == ["User prefers concise answers"]


def test_evaluate_scenarios_reports_success_rate():
    passing = EvaluationScenario(
        name="passing",
        query="pytest",
        memories=[{"text": "Use pytest for tests", "tags": ["project"]}],
        expected_result_texts=["Use pytest for tests"],
    )
    failing = EvaluationScenario(
        name="failing",
        query="pytest",
        memories=[{"text": "Use pytest for tests", "tags": ["project"]}],
        expected_result_texts=["Missing result"],
    )

    report = evaluate_scenarios([passing, failing])

    assert report.total == 2
    assert report.passed == 1
    assert report.failed == 1
    assert report.success_rate == 0.5
