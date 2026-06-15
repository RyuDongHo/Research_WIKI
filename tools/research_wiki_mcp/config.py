"""Application configuration and canonical workspace layout."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

WIKI_PAGE_TYPES = (
    "sources",
    "concepts",
    "comparisons",
    "claims",
    "questions",
    "system",
    "skills",
    "templates",
)


@dataclass(frozen=True)
class AppConfig:
    """Paths and local-server defaults derived from a project root."""

    project_root: Path
    shared_token_env: str = "RESEARCH_WIKI_MCP_TOKEN"
    http_host: str = "127.0.0.1"
    http_port: int = 8765

    @classmethod
    def from_root(cls, project_root: str | Path) -> "AppConfig":
        return cls(project_root=Path(project_root).resolve())

    @property
    def wiki_root(self) -> Path:
        return self.project_root / "wiki"

    @property
    def raw_papers_root(self) -> Path:
        return self.project_root / "raw" / "papers"

    @property
    def screenshots_root(self) -> Path:
        return self.project_root / "raw" / "screenshots"

    @property
    def wiki_assets_root(self) -> Path:
        return self.wiki_root / "assets"

    @property
    def index_path(self) -> Path:
        return self.project_root / "data" / "wiki-index.sqlite3"

    @property
    def mcp_settings_path(self) -> Path:
        return self.project_root / "mcp-settings.json"

    def ensure_workspace_layout(self) -> None:
        """Create canonical and derived-state directories when absent."""

        self.wiki_root.mkdir(parents=True, exist_ok=True)
        for page_type in WIKI_PAGE_TYPES:
            (self.wiki_root / page_type).mkdir(parents=True, exist_ok=True)
        self.raw_papers_root.mkdir(parents=True, exist_ok=True)
        self.screenshots_root.mkdir(parents=True, exist_ok=True)
        self.wiki_assets_root.mkdir(parents=True, exist_ok=True)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
