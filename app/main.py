from __future__ import annotations

import json
from pathlib import Path

from app.core.memory_store import MemoryStore
from app.core.spec_loader import SpecLoader
from app.graph.executor import GraphExecutor


def run_task(repo_path: Path, task_name: str, request_text: str, runtime_provider: str | None = None) -> dict:
    spec_root = Path(__file__).resolve().parents[1] / "specs"
    loader = SpecLoader(spec_root)
    task_spec = loader.load_task(task_name)
    executor = GraphExecutor(
        loader,
        MemoryStore(repo_path / ".." / "logs" / "trajectories"),
        runtime_provider=runtime_provider,
    )
    state = {
        "repo_path": repo_path,
        "task_spec": task_spec,
        "request": {
            "repo_path": str(repo_path),
            "feature_request": request_text,
        },
    }
    return executor.execute(state)


if __name__ == "__main__":
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)
    result = run_task(workspace, "implement_feature", "Add a tool router and tests")
    print(json.dumps(result, indent=2, default=str))
