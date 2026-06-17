from pathlib import Path

from agent_workbench.tools import default_registry
from agent_workbench.tools.base import Tool, ToolResult
from agent_workbench.tools.registry import ToolRegistry


def test_default_registry_has_expected_tools(tmp_path: Path):
    reg = default_registry(tmp_path)
    assert reg.names() == ["read_file", "run_shell", "write_file"]


def test_schemas_are_sorted_for_stable_prefix(tmp_path: Path):
    reg = default_registry(tmp_path)
    names = [s["name"] for s in reg.api_schemas()]
    assert names == sorted(names)


def test_unknown_tool_returns_error(tmp_path: Path):
    reg = default_registry(tmp_path)
    result = reg.execute("nope", {})
    assert result.is_error
    assert "unknown tool" in result.content


def test_bad_arguments_are_reported_not_raised(tmp_path: Path):
    reg = default_registry(tmp_path)
    result = reg.execute("read_file", {"wrong_arg": 1})
    assert result.is_error
    assert "invalid arguments" in result.content


def test_duplicate_registration_rejected(tmp_path: Path):
    class Dummy(Tool):
        name = "dup"
        description = "d"

        @property
        def input_schema(self):
            return {"type": "object", "properties": {}}

        def run(self, **kwargs):
            return ToolResult("ok")

    reg = ToolRegistry()
    reg.register(Dummy())
    try:
        reg.register(Dummy())
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
