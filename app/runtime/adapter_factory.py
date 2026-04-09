from __future__ import annotations

import os

from app.runtime.cli_adapter import ClaudeCodeAdapter, CodexCLIAdapter
from app.runtime.ecc_adapter import ECCAdapter


def build_runtime_adapter(provider: str | None = None) -> ECCAdapter:
    selected = (provider or os.getenv("SPEC_RUNTIME_PROVIDER", "mock")).lower()
    if selected == "claude_code":
        return ClaudeCodeAdapter()
    if selected == "codex_cli":
        return CodexCLIAdapter()
    return ECCAdapter()
