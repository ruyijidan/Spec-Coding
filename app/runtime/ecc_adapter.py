from __future__ import annotations

import sys
from pathlib import Path

from app.runtime.command_executor import CommandExecutor
from app.runtime.patch_applier import PatchApplier


class ECCAdapter:
    provider_name = "mock"

    def __init__(self) -> None:
        self.command_executor = CommandExecutor()
        self.patch_applier = PatchApplier()

    def run_command(self, cmd: list[str], cwd: Path) -> tuple[int, str]:
        return self.command_executor.run(cmd, cwd)

    def edit_file(self, path: Path, content: str) -> None:
        self.patch_applier.write_text(path, content)

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def run_tests(self, target: Path) -> tuple[int, str]:
        return self.run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=target)
