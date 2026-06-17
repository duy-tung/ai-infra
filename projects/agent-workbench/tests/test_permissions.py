from agent_workbench.permissions import Decision, PermissionGate, PermissionRequest


def _req(name="write_file", mutating=True):
    return PermissionRequest(tool_name=name, tool_input={"path": "x"}, mutating=mutating)


def test_readonly_tools_always_allowed():
    gate = PermissionGate(mode="readonly")
    decision, _ = gate.check(_req(name="read_file", mutating=False))
    assert decision is Decision.ALLOW


def test_readonly_mode_denies_mutating():
    gate = PermissionGate(mode="readonly")
    decision, reason = gate.check(_req())
    assert decision is Decision.DENY
    assert "readonly" in reason


def test_auto_mode_allows_mutating():
    gate = PermissionGate(mode="auto")
    decision, _ = gate.check(_req())
    assert decision is Decision.ALLOW


def test_allowlist_overrides_ask():
    gate = PermissionGate(mode="ask", allowlist={"write_file"})
    decision, reason = gate.check(_req())
    assert decision is Decision.ALLOW
    assert reason == "allowlisted"


def test_ask_mode_yes_allows():
    gate = PermissionGate(mode="ask", prompt_fn=lambda _: "y")
    decision, _ = gate.check(_req())
    assert decision is Decision.ALLOW


def test_ask_mode_default_denies():
    gate = PermissionGate(mode="ask", prompt_fn=lambda _: "")
    decision, _ = gate.check(_req())
    assert decision is Decision.DENY
