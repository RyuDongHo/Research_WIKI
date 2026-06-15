"""Rebuildable SQLite index derived from canonical Markdown WIKI pages."""

from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
import sqlite3

from .config import AppConfig
from .markdown import parse_page
from .models import CONTENT_LANGUAGES, PAGE_TYPE_DIRECTORIES, PAGE_STATUSES

SCHEMA = """
CREATE TABLE IF NOT EXISTS pages (
    page_type TEXT NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    author TEXT NOT NULL,
    language TEXT NOT NULL,
    confidence TEXT NOT NULL,
    body TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    sources_text TEXT NOT NULL,
    tags_text TEXT NOT NULL,
    PRIMARY KEY (page_type, slug)
);
CREATE TABLE IF NOT EXISTS page_sources (
    page_type TEXT NOT NULL,
    slug TEXT NOT NULL,
    source TEXT NOT NULL,
    PRIMARY KEY (page_type, slug, source),
    FOREIGN KEY (page_type, slug) REFERENCES pages(page_type, slug) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS page_tags (
    page_type TEXT NOT NULL,
    slug TEXT NOT NULL,
    tag TEXT NOT NULL,
    PRIMARY KEY (page_type, slug, tag),
    FOREIGN KEY (page_type, slug) REFERENCES pages(page_type, slug) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_pages_status ON pages(status);
CREATE INDEX IF NOT EXISTS idx_page_tags_tag ON page_tags(tag);
CREATE INDEX IF NOT EXISTS idx_page_sources_source ON page_sources(source);
"""
RESET_SCHEMA = """
DROP TABLE IF EXISTS page_tags;
DROP TABLE IF EXISTS page_sources;
DROP TABLE IF EXISTS pages;
"""


@dataclass(frozen=True)
class SearchResult:
    page_type: str
    slug: str
    title: str
    status: str
    modified_at: str
    author: str
    language: str
    confidence: str
    relative_path: str
    tags: tuple[str, ...]
    sources: tuple[str, ...]
    excerpt: str


class WikiIndex:
    """SQLite search index that can always be rebuilt from Markdown."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.config.ensure_workspace_layout()

    def rebuild(self) -> int:
        """Replace the derived index from canonical Markdown files."""

        indexed_pages = []
        for path in self._canonical_paths():
            page = parse_page(path.read_text(encoding="utf-8"))
            relative_path = path.relative_to(self.config.wiki_root)
            self._validate_location(path, relative_path, page.page_type, page.slug)
            if path.stem != page.slug:
                raise ValueError(f"{path} filename does not match slug {page.slug}")
            indexed_pages.append((relative_path.as_posix(), page))

        with closing(self._connect()) as connection:
            connection.executescript(RESET_SCHEMA)
            connection.executescript(SCHEMA)
            with connection:
                for relative_path, page in indexed_pages:
                    connection.execute(
                        """
                        INSERT INTO pages (
                            page_type, slug, title, status, modified_at, author,
                            language, confidence, body, relative_path, sources_text, tags_text
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            page.page_type,
                            page.slug,
                            page.title,
                            page.status,
                            page.updated_at.isoformat(),
                            page.author,
                            page.language,
                            page.confidence,
                            page.body,
                            relative_path,
                            "\n".join(page.sources),
                            "\n".join(page.tags),
                        ),
                    )
                    connection.executemany(
                        "INSERT INTO page_sources (page_type, slug, source) VALUES (?, ?, ?)",
                        [(page.page_type, page.slug, source) for source in page.sources],
                    )
                    connection.executemany(
                        "INSERT INTO page_tags (page_type, slug, tag) VALUES (?, ?, ?)",
                        [(page.page_type, page.slug, tag) for tag in page.tags],
                    )
        return len(indexed_pages)

    def search(
        self,
        query: str = "",
        *,
        page_type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        language: str | None = None,
        limit: int = 50,
    ) -> list[SearchResult]:
        if page_type is not None and page_type not in PAGE_TYPE_DIRECTORIES:
            raise ValueError(f"unsupported page type: {page_type}")
        if status is not None and status not in PAGE_STATUSES:
            raise ValueError(f"unsupported page status: {status}")
        if language is not None and language not in CONTENT_LANGUAGES:
            raise ValueError(f"unsupported content language: {language}")
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")

        clauses = []
        parameters: list[str | int] = []
        if query.strip():
            clauses.append(
                """
                (
                    lower(p.title) LIKE ? OR lower(p.body) LIKE ? OR
                    lower(p.tags_text) LIKE ? OR lower(p.sources_text) LIKE ?
                )
                """
            )
            pattern = f"%{query.strip().lower()}%"
            parameters.extend([pattern, pattern, pattern, pattern])
        if page_type is not None:
            clauses.append("p.page_type = ?")
            parameters.append(page_type)
        if status is not None:
            clauses.append("p.status = ?")
            parameters.append(status)
        if tag is not None:
            clauses.append(
                "EXISTS (SELECT 1 FROM page_tags t WHERE t.page_type = p.page_type AND t.slug = p.slug AND t.tag = ?)"
            )
            parameters.append(tag)
        if language is not None:
            clauses.append("p.language = ?")
            parameters.append(language)

        where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.append(limit)
        with closing(self._connect()) as connection:
            rows = connection.execute(
                f"""
                SELECT
                    p.page_type, p.slug, p.title, p.status, p.modified_at,
                    p.author, p.language, p.confidence, p.relative_path, p.tags_text,
                    p.sources_text, p.body
                FROM pages p
                {where_clause}
                ORDER BY p.modified_at DESC, p.page_type, p.slug
                LIMIT ?
                """,
                parameters,
            ).fetchall()
        return [self._to_result(row, query) for row in rows]

    def count(self) -> int:
        with closing(self._connect()) as connection:
            return connection.execute("SELECT COUNT(*) FROM pages").fetchone()[0]

    def _canonical_paths(self) -> list[Path]:
        paths = []
        for directory in PAGE_TYPE_DIRECTORIES.values():
            paths.extend((self.config.wiki_root / directory).glob("*.md"))
        root_index = self.config.wiki_root / "index.md"
        if root_index.exists():
            paths.append(root_index)
        return sorted(paths)

    @staticmethod
    def _validate_location(path: Path, relative_path: Path, page_type: str, slug: str) -> None:
        if relative_path.as_posix() == "index.md" and page_type == "system" and slug == "index":
            return
        expected_directory = PAGE_TYPE_DIRECTORIES[page_type]
        if relative_path.parts[0] != expected_directory:
            raise ValueError(f"{path} is stored outside the {expected_directory} directory")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.config.index_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _to_result(row: sqlite3.Row | tuple, query: str) -> SearchResult:
        body = row[11]
        excerpt = WikiIndex._excerpt(body, query)
        return SearchResult(
            page_type=row[0],
            slug=row[1],
            title=row[2],
            status=row[3],
            modified_at=row[4],
            author=row[5],
            language=row[6],
            confidence=row[7],
            relative_path=row[8],
            tags=tuple(filter(None, row[9].splitlines())),
            sources=tuple(filter(None, row[10].splitlines())),
            excerpt=excerpt,
        )

    @staticmethod
    def _excerpt(body: str, query: str, width: int = 180) -> str:
        normalized_body = " ".join(body.split())
        if len(normalized_body) <= width:
            return normalized_body
        query_index = normalized_body.lower().find(query.strip().lower()) if query.strip() else -1
        start = max(0, query_index - width // 3) if query_index >= 0 else 0
        end = min(len(normalized_body), start + width)
        excerpt = normalized_body[start:end]
        if start:
            excerpt = f"...{excerpt}"
        if end < len(normalized_body):
            excerpt = f"{excerpt}..."
        return excerpt
