import json
from pathlib import Path

from agent_workbench.config import Settings
from agent_workbench.redaction import Redactor, luhn_valid, shannon_entropy
from agent_workbench.tracing import Tracer, Usage


def test_email_redacted():
    out = Redactor().redact("contact me at alice@example.com please")
    assert "alice@example.com" not in out
    assert "[REDACTED:email]" in out


def test_valid_credit_card_redacted_invalid_kept():
    r = Redactor()
    # 4242 4242 4242 4242 is a well-known Luhn-valid test card.
    assert "[REDACTED:credit_card]" in r.redact("card 4242 4242 4242 4242")
    # A 16-digit run that fails Luhn should not be flagged as a card.
    assert "1234567812345678" in r.redact("id 1234567812345678 ok")


def test_aws_jwt_and_prefixed_tokens_redacted():
    r = Redactor()
    assert "[REDACTED:aws_key]" in r.redact("key AKIAIOSFODNN7EXAMPLE here")
    assert "[REDACTED:api_token]" in r.redact("token sk-abcdefghijklmnopqrstuvwxyz0123 here")
    assert "[REDACTED:api_token]" in r.redact("gh token ghp_abcdefghijklmnopqrstuvwxyz0123 ok")
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36"
    assert "[REDACTED:jwt]" in r.redact(f"auth {jwt}")


def test_private_key_block_redacted():
    block = "-----BEGIN RSA PRIVATE KEY-----\nMIIabc\n-----END RSA PRIVATE KEY-----"
    assert "[REDACTED:private_key]" in Redactor().redact(block)


def test_plain_text_untouched():
    text = "this is a normal sentence about postgres transactions and idempotency"
    assert Redactor().redact(text) == text


def test_luhn_and_entropy_helpers():
    assert luhn_valid("4242424242424242")
    assert not luhn_valid("4242424242424241")
    assert shannon_entropy("aaaa") < shannon_entropy("a8X!q9Zk")


def test_tracer_applies_redactor(tmp_path: Path):
    settings = Settings(trace_dir=tmp_path)
    tracer = Tracer(settings, redactor=Redactor())
    tracer.run_start("task")
    tracer.tool_call(
        "read_file", {"path": "x"}, "allow", "ok",
        result_preview="user email is bob@bank.com", is_error=False, latency_s=0.01,
    )
    tracer.run_end("completed", "done, secret sk-abcdefghijklmnopqrstuvwxyz0123")

    text = tracer.path.read_text(encoding="utf-8")
    assert "bob@bank.com" not in text
    assert "sk-abcdefghijklmnopqrstuvwxyz0123" not in text
    # And the JSONL is still valid.
    for line in text.strip().splitlines():
        json.loads(line)
