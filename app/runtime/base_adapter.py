from __future__ import annotations

from pathlib import Path
from typing import Protocol


class RuntimeAdapter(Protocol):
    provider_name: str

    def run_command(self, cmd: list[str], cwd: Path) -> tuple[int, str]:
        ...

    def edit_file(self, path: Path, content: str) -> None:
        ...

    def read_file(self, path: Path) -> str:
        ...

    def run_tests(self, target: Path) -> tuple[int, str]:
        ...
