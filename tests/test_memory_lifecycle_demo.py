import runpy
from pathlib import Path


def test_memory_lifecycle_demo_runs(capsys):
    demo_path = Path(__file__).resolve().parents[1] / "examples" / "memory_lifecycle_demo.py"

    runpy.run_path(str(demo_path), run_name="__main__")
    output = capsys.readouterr().out

    assert "Memory Agent SDK: Lifecycle Demo" in output
    assert "Stored Memories" in output
    assert "Audit Events" in output
    assert "Lifecycle Summary" in output
    assert "observe -> decide -> store -> retrieve -> use -> correct -> forget -> audit" in output
