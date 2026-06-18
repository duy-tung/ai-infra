"""MCP server test — builds the server and checks its tools.

Skipped automatically if the mcp package isn't installed (pip install -e ".[mcp]").
"""

import asyncio
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from agent_workbench.mcp_server import build_server  # noqa: E402


def test_server_exposes_three_tools(tmp_path: Path):
    server = build_server(tmp_path)
    tools = asyncio.run(server.list_tools())
    names = sorted(t.name for t in tools)
    assert names == ["read_file", "run_shell", "write_file"]


def test_tool_has_input_schema(tmp_path: Path):
    server = build_server(tmp_path)
    tools = {t.name: t for t in asyncio.run(server.list_tools())}
    schema = tools["write_file"].inputSchema
    assert schema["type"] == "object"
    assert "path" in schema["properties"]
    assert "content" in schema["properties"]
