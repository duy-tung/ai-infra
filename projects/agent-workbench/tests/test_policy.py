from agent_workbench.permissions import Decision, PermissionRequest
from agent_workbench.policy import Policy, PolicyGate

POLICY = {
    "default": "ask",
    "tools": {"read_file": "allow", "write_file": "ask", "run_shell": "deny"},
    "deny_paths": ["*.env", "*secrets*"],
    "deny_commands": [r"rm\s+-rf", r"curl.*\|\s*sh"],
}


def _req(name, **inp):
    return PermissionRequest(tool_name=name, tool_input=inp, mutating=True)


def test_allow_action():
    gate = PolicyGate(Policy.from_dict(POLICY))
    d, _ = gate.check(_req("read_file", path="a.txt"))
    assert d is Decision.ALLOW


def test_deny_action():
    gate = PolicyGate(Policy.from_dict(POLICY))
    d, reason = gate.check(_req("run_shell", command="ls"))
    assert d is Decision.DENY and "policy: deny" in reason


def test_ask_action_prompts():
    gate = PolicyGate(Policy.from_dict(POLICY), prompt_fn=lambda _: "y")
    d, _ = gate.check(_req("write_file", path="a.txt"))
    assert d is Decision.ALLOW


def test_deny_path_rule_overrides_action():
    gate = PolicyGate(Policy.from_dict(POLICY))
    # read_file is 'allow', but the path matches a deny rule.
    d, reason = gate.check(_req("read_file", path="config/.env"))
    assert d is Decision.DENY and "deny rule" in reason


def test_deny_command_rule():
    gate = PolicyGate(Policy.from_dict(POLICY), prompt_fn=lambda _: "y")
    # run_shell is 'deny' anyway; use a command rule against an 'ask'/default tool.
    p = dict(POLICY, tools={"run_shell": "ask"})
    gate = PolicyGate(Policy.from_dict(p), prompt_fn=lambda _: "y")
    d, reason = gate.check(_req("run_shell", command="rm -rf /tmp/x"))
    assert d is Decision.DENY and "deny rule" in reason


def test_unknown_action_rejected():
    try:
        Policy.from_dict({"default": "maybe"})
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
