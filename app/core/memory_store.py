from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, name: str, payload: dict[str, Any]) -> Path:
        path = self.root / f"{name}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
