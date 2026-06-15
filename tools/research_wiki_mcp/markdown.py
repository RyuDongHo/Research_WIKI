"""Render and parse the project's constrained Markdown frontmatter schema."""

from __future__ import annotations

from datetime import datetime

from .models import WikiPage

SCALAR_FIELDS = ("type", "slug", "title", "status", "modified_at", "author", "language", "confidence")
LIST_FIELDS = ("sources", "tags")


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def render_page(page: WikiPage) -> str:
    page.validated()
    if page.updated_at is None:
        raise ValueError("updated_at must be set before rendering")
    lines = [
        "---",
        f"type: {_quote(page.page_type)}",
        f"slug: {_quote(page.slug)}",
        f"title: {_quote(page.title)}",
        f"status: {_quote(page.status)}",
        f"modified_at: {_quote(page.updated_at.isoformat())}",
        f"author: {_quote(page.author)}",
        f"language: {_quote(page.language)}",
        f"confidence: {_quote(page.confidence)}",
        "sources:",
        *[f"  - {_quote(value)}" for value in page.sources],
        "tags:",
        *[f"  - {_quote(value)}" for value in page.tags],
        "---",
        "",
        page.body.rstrip(),
        "",
    ]
    return "\n".join(lines)


def parse_page(text: str) -> WikiPage:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Markdown page must begin with YAML frontmatter")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Markdown page frontmatter is not closed") from exc

    scalars: dict[str, str] = {}
    lists: dict[str, list[str]] = {field: [] for field in LIST_FIELDS}
    current_list: str | None = None
    for line in lines[1:closing_index]:
        if line.startswith("  - "):
            if current_list is None:
                raise ValueError("list item must follow a supported list field")
            lists[current_list].append(_unquote(line[4:]))
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if key in LIST_FIELDS:
            if raw_value:
                raise ValueError(f"{key} must use block-list syntax")
            current_list = key
            continue
        if key not in SCALAR_FIELDS:
            raise ValueError(f"unsupported frontmatter field: {key}")
        if not raw_value:
            raise ValueError(f"{key} must not be empty")
        scalars[key] = _unquote(raw_value)
        current_list = None

    missing = [field for field in SCALAR_FIELDS if field not in scalars]
    if missing:
        raise ValueError(f"missing frontmatter fields: {', '.join(missing)}")
    try:
        updated_at = datetime.fromisoformat(scalars["modified_at"])
    except ValueError as exc:
        raise ValueError("modified_at must be an ISO-8601 datetime") from exc

    page = WikiPage(
        page_type=scalars["type"],
        slug=scalars["slug"],
        title=scalars["title"],
        status=scalars["status"],
        updated_at=updated_at,
        author=scalars["author"],
        language=scalars["language"],
        confidence=scalars["confidence"],
        sources=tuple(lists["sources"]),
        tags=tuple(lists["tags"]),
        body="\n".join(lines[closing_index + 1 :]).strip(),
    )
    return page.validated()
