from pathlib import Path

from agent_workbench.audit import AuditLog, verify


def test_records_and_verifies(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(path)
    log.record("write_file", "path=a.txt", "allow", "approved")
    log.record("run_shell", "command=ls", "deny", "denied by human")
    ok, msg = verify(path)
    assert ok, msg


def test_resume_continues_chain(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    AuditLog(path).record("write_file", "path=a", "allow", "ok")
    # New instance, same file — should pick up seq 1 and keep the chain valid.
    AuditLog(path).record("write_file", "path=b", "allow", "ok")
    ok, msg = verify(path)
    assert ok, msg
    assert "2 records" in msg


def test_tamper_is_detected(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(path)
    log.record("write_file", "path=a.txt", "allow", "approved")
    log.record("write_file", "path=b.txt", "allow", "approved")

    # Tamper with the first record's content without fixing the hash chain.
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace("a.txt", "evil.txt")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, msg = verify(path)
    assert not ok
    assert "tampered" in msg or "broken chain" in msg
