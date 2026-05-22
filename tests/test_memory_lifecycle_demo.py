from examples.memory_lifecycle_demo import main


def test_memory_lifecycle_demo_runs(capsys):
    main()
    output = capsys.readouterr().out

    assert "Memory Agent SDK: Lifecycle Demo" in output
    assert "Stored Memories" in output
    assert "Retrieved Memories" in output
    assert "Corrected Memory" in output
    assert "Retrieval After Forgetting Temporary Memory" in output
    assert "Audit Events" in output
    assert "Lifecycle Summary" in output
    assert "observe -> decide -> store -> retrieve -> use -> correct -> forget -> audit" in output
