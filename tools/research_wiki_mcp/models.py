"""Validated models for canonical Markdown WIKI pages."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import PurePosixPath
from re import fullmatch

PAGE_TYPE_DIRECTORIES = {
    "source": "sources",
    "concept": "concepts",
    "comparison": "comparisons",
    "claim": "claims",
    "question": "questions",
    "system": "system",
    "skill": "skills",
}
PAGE_STATUSES = frozenset({"draft", "reviewed"})
CONFIDENCE_LEVELS = frozenset({"low", "medium", "high"})
CONTENT_LANGUAGES = frozenset({"ko", "en"})


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def validate_slug(slug: str) -> str:
    """Return a safe relative page slug without its Markdown suffix."""

    if not fullmatch(r"[a-z0-9]+(?:[a-z0-9._-]*[a-z0-9])?", slug):
        raise ValueError("slug must use lowercase letters, digits, dots, underscores, or hyphens")
    path = PurePosixPath(slug)
    if path.name != slug or slug in {".", ".."}:
        raise ValueError("slug must identify one WIKI page")
    return slug


@dataclass(frozen=True)
class WikiPage:
    """A canonical Markdown WIKI page with provenance metadata."""

    page_type: str
    slug: str
    title: str
    status: str = "draft"
    updated_at: datetime | None = None
    author: str = ""
    language: str = "ko"
    confidence: str = "low"
    sources: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    body: str = ""

    def validated(self) -> "WikiPage":
        if self.page_type not in PAGE_TYPE_DIRECTORIES:
            raise ValueError(f"unsupported page type: {self.page_type}")
        validate_slug(self.slug)
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if self.status not in PAGE_STATUSES:
            raise ValueError(f"unsupported page status: {self.status}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported confidence level: {self.confidence}")
        if self.language not in CONTENT_LANGUAGES:
            raise ValueError(f"unsupported content language: {self.language}")
        if not self.author.strip():
            raise ValueError("author must not be empty")
        if any(not item.strip() for item in (*self.sources, *self.tags)):
            raise ValueError("sources and tags must not contain empty values")
        return self

    def with_timestamp(self, timestamp: datetime | None = None) -> "WikiPage":
        return replace(self, updated_at=timestamp or utc_now())

    def reviewed(self) -> "WikiPage":
        return replace(self, status="reviewed")
