from pathlib import Path

from agent_workbench.tools.fs import ReadFileTool, WriteFileTool, resolve_in_root


def test_resolve_rejects_parent_escape(tmp_path: Path):
    try:
        resolve_in_root(tmp_path, "../../etc/passwd")
    except PermissionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected PermissionError")


def test_resolve_allows_nested(tmp_path: Path):
    target = resolve_in_root(tmp_path, "a/b/c.txt")
    assert str(target).startswith(str(tmp_path.resolve()))


def test_write_then_read_roundtrip(tmp_path: Path):
    writer = WriteFileTool(tmp_path)
    reader = ReadFileTool(tmp_path)
    w = writer.run(path="sub/hello.txt", content="hi there")
    assert not w.is_error
    r = reader.run(path="sub/hello.txt")
    assert not r.is_error
    assert r.content == "hi there"


def test_write_escape_is_blocked(tmp_path: Path):
    writer = WriteFileTool(tmp_path)
    result = writer.run(path="../escape.txt", content="x")
    assert result.is_error
    assert "escapes workdir" in result.content
