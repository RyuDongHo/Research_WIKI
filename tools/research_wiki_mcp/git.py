"""Small Git boundary for WIKI revision history."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess


@dataclass(frozen=True)
class Revision:
    commit: str
    author: str
    email: str
    committed_at: str
    message: str


class GitRepository:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def ensure_initialized(self) -> None:
        if not (self.root / ".git").exists():
            self._run("init", "-b", "main")

    def commit_file(self, path: Path, *, author: str, email: str, message: str) -> str | None:
        return self.commit_files((path,), author=author, email=email, message=message)

    def commit_files(self, paths: tuple[Path, ...], *, author: str, email: str, message: str) -> str | None:
        relative_paths = tuple(self._relative_path(path) for path in paths)
        if not relative_paths:
            return None
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": author,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_COMMITTER_NAME": author,
            "GIT_COMMITTER_EMAIL": email,
        }
        self._run("add", "--", *relative_paths, env=env)
        staged = self._run("diff", "--cached", "--quiet", "--", *relative_paths, env=env, check=False)
        if staged.returncode == 0:
            return None
        self._run("commit", "-m", message, "--", *relative_paths, env=env)
        return self._run("rev-parse", "HEAD").stdout.strip()

    def history(self, path: Path) -> list[Revision]:
        relative_path = self._relative_path(path)
        result = self._run(
            "log",
            "--format=%H%x1f%an%x1f%ae%x1f%aI%x1f%s",
            "--",
            relative_path,
        )
        revisions = []
        for line in result.stdout.splitlines():
            commit, author, email, committed_at, message = line.split("\x1f", 4)
            revisions.append(Revision(commit, author, email, committed_at, message))
        return revisions

    def read_file_at_revision(self, path: Path, revision: str) -> str:
        relative_path = self._relative_path(path)
        return self._run("show", f"{revision}:{relative_path}").stdout

    def _relative_path(self, path: Path) -> str:
        resolved_path = path.resolve()
        try:
            relative_path = resolved_path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Git path must stay inside the repository") from exc
        return relative_path.as_posix()

    def _run(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-c", "core.fscache=false", *args],
            cwd=self.root,
            env=env,
            stdin=subprocess.DEVNULL,
            check=check,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
