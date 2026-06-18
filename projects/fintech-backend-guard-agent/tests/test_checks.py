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
