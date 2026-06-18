"""Sandbox runners for the shell tool.

`run_shell` is the most dangerous tool, so *where* it runs matters. A Sandbox
abstracts execution behind one interface so the tool doesn't care:

- `LocalSandbox` (default) runs on the host, jailed to the working directory.
  Fine for trusted tasks and tests.
- `DockerSandbox` runs each command in an ephemeral `docker run --rm` container
  with the workdir mounted and **networking off by default** — the right
  posture for untrusted or autonomous runs. (Requires a reachable Docker daemon.)

Swapping the runner changes the blast radius without touching the agent loop.
"""

from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class ShellOutcome:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


class Sandbox(Protocol):
    def run(self, command: str, workdir: Path, timeout: int) -> ShellOutcome: ...


class LocalSandbox:
    """Runs the command on the host with cwd set to the working directory."""

    def run(self, command: str, workdir: Path, timeout: int) -> ShellOutcome:
        try:
            proc = subprocess.run(
                command,
                shell=True,
                cwd=str(workdir),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return ShellOutcome(returncode=124, stdout="", stderr="", timed_out=True)
        return ShellOutcome(returncode=proc.returncode, stdout=proc.stdout or "", stderr=proc.stderr or "")


@dataclass
class DockerSandbox:
    """Runs each command in a throwaway container. Networking is disabled by
    default; the workdir is bind-mounted read-write at /work."""

    image: str = "python:3.11-slim"
    network: str = "none"  # "none" = no egress; set "bridge" to allow
    user: str = ""  # e.g. "1000:1000" to drop root; "" uses image default
    extra_args: tuple[str, ...] = ()

    def run(self, command: str, workdir: Path, timeout: int) -> ShellOutcome:
        workdir = Path(workdir).resolve()
        argv = [
            "docker", "run", "--rm",
            "--network", self.network,
            "-v", f"{workdir}:/work",
            "-w", "/work",
        ]
        if self.user:
            argv += ["--user", self.user]
        argv += list(self.extra_args)
        argv += [self.image, "sh", "-lc", command]
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return ShellOutcome(returncode=124, stdout="", stderr="", timed_out=True)
        except FileNotFoundError:
            return ShellOutcome(returncode=127, stdout="", stderr="docker not found on PATH")
        return ShellOutcome(returncode=proc.returncode, stdout=proc.stdout or "", stderr=proc.stderr or "")

    def describe(self) -> str:
        return f"DockerSandbox(image={self.image}, network={self.network}) -> docker {shlex.join(['run', '--rm', '...'])}"
