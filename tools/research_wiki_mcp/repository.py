"""Canonical Markdown page storage with Git-backed revisions."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .config import AppConfig
from .git import GitRepository, Revision
from .markdown import parse_page, render_page
from .models import PAGE_TYPE_DIRECTORIES, WikiPage, validate_slug


class PageRepository:
    def __init__(self, config: AppConfig, git: GitRepository | None = None) -> None:
        self.config = config
        self.git = git or GitRepository(config.project_root)
        self.config.ensure_workspace_layout()
        self.git.ensure_initialized()

    def save(
        self,
        page: WikiPage,
        *,
        author_email: str,
        commit_message: str | None = None,
    ) -> WikiPage:
        if not author_email.strip():
            raise ValueError("author_email must not be empty")
        stored_page = page.with_timestamp().validated()
        path = self.path_for(stored_page.page_type, stored_page.slug)
        path.write_text(render_page(stored_page), encoding="utf-8")
        message = commit_message or f"wiki: save {stored_page.page_type}/{stored_page.slug}"
        self.git.commit_file(
            path,
            author=stored_page.author,
            email=author_email,
            message=message,
        )
        return stored_page

    def read(self, page_type: str, slug: str) -> WikiPage:
        return parse_page(self.path_for(page_type, slug).read_text(encoding="utf-8"))

    def review(self, page_type: str, slug: str, *, author: str, author_email: str) -> WikiPage:
        page = replace(self.read(page_type, slug).reviewed(), author=author)
        return self.save(
            page,
            author_email=author_email,
            commit_message=f"wiki: review {page_type}/{slug}",
        )

    def history(self, page_type: str, slug: str) -> list[Revision]:
        return self.git.history(self.path_for(page_type, slug))

    def read_revision(self, page_type: str, slug: str, revision: str) -> WikiPage:
        text = self.git.read_file_at_revision(self.path_for(page_type, slug), revision)
        return parse_page(text)

    def restore_revision(
        self,
        page_type: str,
        slug: str,
        revision: str,
        *,
        author: str,
        author_email: str,
    ) -> WikiPage:
        page = replace(self.read_revision(page_type, slug, revision), author=author)
        return self.save(
            page,
            author_email=author_email,
            commit_message=f"wiki: restore {page_type}/{slug} from {revision[:12]}",
        )

    def path_for(self, page_type: str, slug: str) -> Path:
        if page_type == "system" and slug == "index" and (self.config.wiki_root / "index.md").exists():
            return self.config.wiki_root / "index.md"
        try:
            directory = PAGE_TYPE_DIRECTORIES[page_type]
        except KeyError as exc:
            raise ValueError(f"unsupported page type: {page_type}") from exc
        return self.config.wiki_root / directory / f"{validate_slug(slug)}.md"
