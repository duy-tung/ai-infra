"""Append-only, hash-chained audit log.

Separate from the trace (which is for debugging/cost): the audit log is the
*compliance* record of state-changing actions and the permission decisions that
gated them. Each entry carries the SHA-256 of the previous entry, so the file is
tamper-evident — change or drop a record and `verify()` detects the broken
chain. This is the fintech audit-trail pattern in miniature; the same idea
scales to a real append-only store.

Each record:  {seq, ts, actor, action, target, decision, reason, prev_hash, hash}
where hash = sha256(canonical_json(record_without_hash)).
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

GENESIS = "0" * 64


def _hash_record(record: dict[str, Any]) -> str:
    payload = {k: v for k, v in record.items() if k != "hash"}
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class AuditLog:
    path: Path
    actor: str = "agent"

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._seq = 0
        self._prev_hash = GENESIS
        if self.path.exists():
            self._resume()

    def _resume(self) -> None:
        last = None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                last = json.loads(line)
        if last is not None:
            self._seq = last["seq"] + 1
            self._prev_hash = last["hash"]

    def record(
        self,
        action: str,
        target: str,
        decision: str,
        reason: str,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "seq": self._seq,
            "ts": round(time.time(), 3),
            "actor": self.actor,
            "action": action,
            "target": target,
            "decision": decision,
            "reason": reason,
            "prev_hash": self._prev_hash,
        }
        if extra:
            entry["extra"] = extra
        entry["hash"] = _hash_record(entry)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self._seq += 1
        self._prev_hash = entry["hash"]
        return entry


def verify(path: str | Path) -> tuple[bool, str]:
    """Verify the hash chain of an audit file. Returns (ok, message)."""
    path = Path(path)
    if not path.exists():
        return False, "audit file does not exist"
    prev = GENESIS
    expected_seq = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("seq") != expected_seq:
            return False, f"seq gap at {expected_seq} (got {rec.get('seq')})"
        if rec.get("prev_hash") != prev:
            return False, f"broken chain at seq {rec.get('seq')}: prev_hash mismatch"
        if _hash_record(rec) != rec.get("hash"):
            return False, f"tampered record at seq {rec.get('seq')}: hash mismatch"
        prev = rec["hash"]
        expected_seq += 1
    return True, f"chain valid ({expected_seq} records)"
