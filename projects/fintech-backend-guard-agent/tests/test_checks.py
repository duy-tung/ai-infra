from fintech_guard.checks import run_static_checks
from fintech_guard.diff import FileDiff
from fintech_guard.findings import Severity


def _fd(path, *lines):
    return [FileDiff(path=path, added=[(i + 1, ln) for i, ln in enumerate(lines)])]


def _categories(files):
    return {f.category for f in run_static_checks(files)}


def test_money_float_flagged():
    files = _fd("wallet.go", "type W struct {", "\tBalance float64", "}")
    assert "money_float" in _categories(files)


def test_money_int_not_flagged():
    files = _fd("wallet.go", "type W struct {", "\tBalanceCents int64", "}")
    assert "money_float" not in _categories(files)


def test_migration_index_lock():
    files = _fd("migrations/1.sql", "CREATE INDEX idx ON tbl (col);")
    assert "migration_index_lock" in _categories(files)


def test_migration_index_concurrently_ok():
    files = _fd("migrations/1.sql", "CREATE INDEX CONCURRENTLY idx ON tbl (col);")
    assert "migration_index_lock" not in _categories(files)


def test_migration_not_null_without_default():
    files = _fd("migrations/2.sql", "ALTER TABLE accounts ADD COLUMN status text NOT NULL;")
    cats = _categories(files)
    assert "migration_not_null" in cats


def test_secret_flagged_as_critical():
    files = _fd("config.py", 'KEY = "sk-abcdefghijklmnopqrstuvwxyz0123"')
    findings = run_static_checks(files)
    pii = [f for f in findings if f.category == "pii_secret"]
    assert pii and pii[0].severity is Severity.CRITICAL


def test_error_swallow():
    files = _fd("pay.py", "    try:", "        capture()", "    except Exception:", "        pass")
    assert "error_swallow" in _categories(files)


def test_missing_audit_on_ledger_write():
    files = _fd("ledger.py", 'db.execute("INSERT INTO ledger (acct) VALUES (1)")')
    assert "missing_audit" in _categories(files)


def test_missing_audit_silenced_when_audit_present():
    files = _fd(
        "ledger.py",
        'db.execute("INSERT INTO ledger (acct) VALUES (1)")',
        "audit.record(actor, 'post', before, after)",
    )
    assert "missing_audit" not in _categories(files)


def test_clean_code_no_findings():
    files = _fd("util.py", "def slugify(name):", '    return name.lower()')
    assert _categories(files) == set()


def test_ledger_matches_plural_tables():
    # regression: \baccount\b must also match "accounts"
    files = _fd("a.py", 'db.execute("UPDATE accounts SET x = 1")')
    assert "missing_audit" in _categories(files)


def test_txn_boundary_two_writes_no_transaction():
    files = _fd("t.py",
                'db.execute("UPDATE accounts SET bal = bal - 1")',
                'db.execute("UPDATE accounts SET bal = bal + 1")',
                'audit.record("x")')
    assert "txn_boundary" in _categories(files)


def test_txn_boundary_silenced_by_transaction():
    files = _fd("t.py",
                "with db.begin():",
                '    db.execute("UPDATE accounts SET bal = bal - 1")',
                '    db.execute("UPDATE accounts SET bal = bal + 1")')
    assert "txn_boundary" not in _categories(files)


def test_ledger_imbalance_single_sided():
    files = _fd("l.py", "db.execute(\"INSERT INTO ledger (side) VALUES ('debit')\")", 'audit.record("x")')
    assert "ledger_imbalance" in _categories(files)


def test_money_division_flagged():
    assert "money_division" in _categories(_fd("m.py", "x = amount / 100"))


def test_money_division_ignores_comment():
    assert "money_division" not in _categories(_fd("m.py", "# amount / 100 is fine"))


def test_unbounded_retry_flagged():
    files = _fd("r.py", "while True: charge(o)", "    retry()")
    assert "unbounded_retry" in _categories(files)


def test_bounded_retry_ok():
    files = _fd("r.py", "for i in range(max_attempts):", "    charge(o); retry()")
    assert "unbounded_retry" not in _categories(files)


def test_missing_reconciliation_flagged():
    assert "missing_reconciliation" in _categories(_fd("s.py", "payout(batch)"))


def test_reconciliation_present_ok():
    files = _fd("s.py", "payout(batch)", "reconcile(batch)")
    assert "missing_reconciliation" not in _categories(files)
