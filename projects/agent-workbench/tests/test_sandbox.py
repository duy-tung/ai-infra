import subprocess
from pathlib import Path

import pytest

from agent_workbench.sandbox import DockerSandbox, LocalSandbox


def test_local_runs_command(tmp_path: Path):
    out = LocalSandbox().run("echo sandboxed", tmp_path, timeout=10)
    assert out.returncode == 0
    assert "sandboxed" in out.stdout
    assert not out.timed_out


def test_local_reports_nonzero_exit(tmp_path: Path):
    out = LocalSandbox().run("exit 3", tmp_path, timeout=10)
    assert out.returncode == 3


def test_local_times_out(tmp_path: Path):
    out = LocalSandbox().run("sleep 3", tmp_path, timeout=1)
    assert out.timed_out


def test_local_runs_in_workdir(tmp_path: Path):
    (tmp_path / "marker.txt").write_text("x")
    out = LocalSandbox().run("ls", tmp_path, timeout=10)
    assert "marker.txt" in out.stdout


def _docker_available() -> bool:
    try:
        r = subprocess.run(["docker", "run", "--rm", "busybox", "true"],
                           capture_output=True, timeout=30)
        return r.returncode == 0
    except Exception:
        return False


@pytest.mark.skipif(not _docker_available(), reason="docker daemon not reachable")
def test_docker_runs_command(tmp_path: Path):
    out = DockerSandbox(image="busybox").run("echo from-container", tmp_path, timeout=60)
    assert out.returncode == 0
    assert "from-container" in out.stdout
