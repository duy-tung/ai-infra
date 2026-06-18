"""MCP bridge integration test — full client⇄server round-trip over stdio.

Spawns the workbench MCP server as a subprocess, loads its tools through the
bridge, and calls one. Skipped if mcp isn't installed.
"""

import os
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from agent_workbench.mcp_bridge import MCPToolProvider  # noqa: E402

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])


def _server_env(workdir: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["AGENT_MCP_WORKDIR"] = str(workdir)
    # Ensure the subprocess can import the package.
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = PROJECT_ROOT + (os.pathsep + existing if existing else "")
    return env


def test_bridge_loads_and_calls_remote_tool(tmp_path: Path):
    (tmp_path / "config.txt").write_text("timeout=30\n", encoding="utf-8")

    with MCPToolProvider(
        command=sys.executable,
        args=["-m", "agent_workbench.mcp_server"],
        env=_server_env(tmp_path),
    ) as provider:
        names = sorted(t.name for t in provider.tools)
        assert names == ["read_file", "run_shell", "write_file"]

        read_tool = next(t for t in provider.tools if t.name == "read_file")
        result = read_tool.run(path="config.txt")
        assert not result.is_error
        assert "timeout=30" in result.content


def test_bridge_tools_are_gated_as_mutating(tmp_path: Path):
    # The bridge can't know what a remote tool does, so all MCP tools are
    # treated as mutating (and therefore go through the permission gate).
    with MCPToolProvider(
        command=sys.executable,
        args=["-m", "agent_workbench.mcp_server"],
        env=_server_env(tmp_path),
    ) as provider:
        assert all(t.mutating for t in provider.tools)
