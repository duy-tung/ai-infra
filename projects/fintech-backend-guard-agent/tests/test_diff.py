from fintech_guard.diff import parse_unified_diff

DIFF = """diff --git a/svc/pay.py b/svc/pay.py
--- a/svc/pay.py
+++ b/svc/pay.py
@@ -10,3 +10,4 @@ def existing():
 context line
-removed line
+added one
+added two
"""


def test_parses_path_and_added_lines():
    files = parse_unified_diff(DIFF)
    assert len(files) == 1
    fd = files[0]
    assert fd.path == "svc/pay.py"
    texts = [t for _, t in fd.added]
    assert texts == ["added one", "added two"]


def test_added_line_numbers_track_new_file():
    fd = parse_unified_diff(DIFF)[0]
    # hunk starts at new line 10: context(10), added(11), added(12)
    linenos = [ln for ln, _ in fd.added]
    assert linenos == [11, 12]


def test_is_sql_detection():
    files = parse_unified_diff(
        "diff --git a/migrations/x.sql b/migrations/x.sql\n+++ b/migrations/x.sql\n@@ -0,0 +1,1 @@\n+SELECT 1;\n"
    )
    assert files[0].is_sql()


def test_dev_null_skipped():
    # A deleted file (+++ /dev/null) should not create a FileDiff.
    diff = "diff --git a/x b/x\n--- a/x\n+++ /dev/null\n@@ -1,1 +0,0 @@\n-gone\n"
    assert parse_unified_diff(diff) == []
