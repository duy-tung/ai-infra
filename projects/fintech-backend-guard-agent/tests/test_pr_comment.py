from fintech_guard.cli import main
from fintech_guard.pipeline import Guard
from fintech_guard.pr_comment import MARKER, is_guard_comment, to_comment

RISKY = "+++ b/wallet.go\n@@ -0,0 +1,1 @@\n+    Balance float64\n"


def test_comment_has_marker_findings_and_footer():
    report = Guard(reviewer=None).review_diff(RISKY)
    body = to_comment(report)
    assert MARKER in body
    assert "money_float" in body
    assert "advisory" in body.lower()
    assert is_guard_comment(body)


def test_is_guard_comment_false_for_other_text():
    assert not is_guard_comment("a normal review comment")
    assert not is_guard_comment("")


def test_cli_comment_flag_emits_marker(tmp_path, capsys):
    diff = tmp_path / "pr.diff"
    diff.write_text(RISKY, encoding="utf-8")
    rc = main(["--diff", str(diff), "--comment"])
    out = capsys.readouterr().out
    assert MARKER in out
    assert "money_float" in out
    assert rc == 0  # advisory by default → never blocks


def test_cli_enforce_blocks_on_high(tmp_path, capsys):
    diff = tmp_path / "pr.diff"
    diff.write_text(RISKY, encoding="utf-8")
    rc = main(["--diff", str(diff), "--enforce", "--threshold", "high"])
    capsys.readouterr()
    assert rc == 1  # money_float is HIGH
