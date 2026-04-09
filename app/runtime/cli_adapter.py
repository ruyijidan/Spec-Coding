from __future__ import annotations

from app.runtime.ecc_adapter import ECCAdapter


class ClaudeCodeAdapter(ECCAdapter):
    provider_name = "claude_code"


class CodexCLIAdapter(ECCAdapter):
    provider_name = "codex_cli"
