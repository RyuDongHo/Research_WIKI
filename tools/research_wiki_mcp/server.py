"""FastMCP server exposing the research WIKI through stdio."""

from __future__ import annotations

import argparse
from dataclasses import replace
from hmac import compare_digest
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .config import AppConfig
from .mcp_catalog import McpSettingsStore
from .service import ResearchWikiService


class SharedTokenMiddleware:
    """Require one configured bearer token for the Streamable HTTP endpoint."""

    def __init__(self, app: ASGIApp, *, token: str, protected_path: str = "/mcp") -> None:
        if not token:
            raise ValueError("shared HTTP token must not be empty")
        self.app = app
        self.token = token
        self.protected_path = protected_path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope.get("path") == self.protected_path:
            authorization = self._authorization_header(scope)
            if not self._is_authorized(authorization):
                response = PlainTextResponse(
                    "Unauthorized",
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                )
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)

    def _is_authorized(self, authorization: str) -> bool:
        prefix = "Bearer "
        if not authorization.startswith(prefix):
            return False
        return compare_digest(authorization[len(prefix) :], self.token)

    @staticmethod
    def _authorization_header(scope: Scope) -> str:
        for name, value in scope.get("headers", ()):
            if name.lower() == b"authorization":
                return value.decode("latin-1")
        return ""


def create_server(config: AppConfig) -> FastMCP:
    service = ResearchWikiService(config)
    settings = McpSettingsStore(config)
    mcp = FastMCP(
        "Research WIKI MCP",
        instructions=(
            "연구 WIKI를 읽고 쓰는 MCP 서버입니다. 모델 기반 요약과 novelty 분석은 연결된 Codex 또는 Claude Code가 수행합니다. "
            "대화 중 재사용 가치가 있는 논문 해석, 핵심 개념, 비교 결과, 연구 claim 또는 열린 질문이 구체화되면 "
            "wiki_capture_discussion을 적극적으로 호출하여 적절한 WIKI 페이지에 저장하세요. "
            "사소한 질의응답, 아직 합의되지 않은 추측, 중복 내용은 저장하지 마세요."
        ),
        host=config.http_host,
        port=config.http_port,
        json_response=True,
        stateless_http=True,
    )

    def register_if_enabled(kind: str, name: str, decorator):
        """Register one MCP primitive only when enabled in startup settings."""

        return decorator if settings.is_enabled(kind, name) else lambda function: function

    @register_if_enabled("resource", "wiki_index", mcp.resource("wiki://index", mime_type="application/json"))
    def wiki_index() -> str:
        """Return the searchable WIKI index."""

        return service.index_resource()

    @register_if_enabled("resource", "wiki_papers", mcp.resource("wiki://papers", mime_type="application/json"))
    def wiki_papers() -> str:
        """Return local paper ingest states for GUI and agent use."""

        return service.papers_resource()

    @register_if_enabled(
        "resource",
        "wiki_page",
        mcp.resource("wiki://page/{page_type}/{slug}", mime_type="application/json"),
    )
    def wiki_page(page_type: str, slug: str) -> str:
        """Return one canonical WIKI page."""

        return service.page_resource(page_type, slug)

    @register_if_enabled("tool", "wiki_search", mcp.tool())
    def wiki_search(
        query: str = "",
        page_type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        language: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Search canonical WIKI content through the rebuildable index."""

        return service.search(
            query,
            page_type=page_type,
            status=status,
            tag=tag,
            language=language,
            limit=limit,
        )

    @register_if_enabled("tool", "wiki_read_page", mcp.tool())
    def wiki_read_page(page_type: str, slug: str) -> dict:
        """Read one canonical WIKI Markdown page as structured data."""

        return service.read_page(page_type, slug)

    @register_if_enabled("tool", "wiki_save_page", mcp.tool())
    def wiki_save_page(
        page_type: str,
        slug: str,
        title: str,
        author: str,
        author_email: str,
        body: str,
        status: str = "draft",
        language: str = "ko",
        confidence: str = "low",
        sources: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Create or edit a Git-managed canonical Markdown page."""

        return service.save_page(
            page_type=page_type,
            slug=slug,
            title=title,
            author=author,
            author_email=author_email,
            body=body,
            status=status,
            language=language,
            confidence=confidence,
            sources=sources,
            tags=tags,
        )

    @register_if_enabled("tool", "wiki_create_research_page", mcp.tool())
    def wiki_create_research_page(
        page_type: str,
        slug: str,
        title: str,
        author: str,
        author_email: str,
        body: str,
        language: str = "ko",
        confidence: str = "low",
        sources: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Create a user-driven claim or question page."""

        return service.create_research_page(
            page_type=page_type,
            slug=slug,
            title=title,
            author=author,
            author_email=author_email,
            body=body,
            language=language,
            confidence=confidence,
            sources=sources,
            tags=tags,
        )

    @register_if_enabled("tool", "wiki_capture_discussion", mcp.tool())
    def wiki_capture_discussion(
        page_type: str,
        slug: str,
        title: str,
        author: str,
        author_email: str,
        entry: str,
        rationale: str,
        language: str = "ko",
        confidence: str = "medium",
        sources: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Persist durable knowledge discovered during discussion into an appropriate WIKI page."""

        return service.capture_discussion(
            page_type=page_type,
            slug=slug,
            title=title,
            author=author,
            author_email=author_email,
            entry=entry,
            rationale=rationale,
            language=language,
            confidence=confidence,
            sources=sources,
            tags=tags,
        )

    @register_if_enabled("tool", "wiki_review_page", mcp.tool())
    def wiki_review_page(page_type: str, slug: str, author: str, author_email: str) -> dict:
        """Promote a draft WIKI page to reviewed."""

        return service.review_page(page_type, slug, author=author, author_email=author_email)

    @register_if_enabled("tool", "wiki_list_revisions", mcp.tool())
    def wiki_list_revisions(page_type: str, slug: str) -> list[dict]:
        """List Git revisions for one WIKI page."""

        return service.list_revisions(page_type, slug)

    @register_if_enabled("tool", "wiki_restore_revision", mcp.tool())
    def wiki_restore_revision(
        page_type: str,
        slug: str,
        revision: str,
        author: str,
        author_email: str,
    ) -> dict:
        """Restore one WIKI page from a prior Git revision."""

        return service.restore_revision(
            page_type,
            slug,
            revision,
            author=author,
            author_email=author_email,
        )

    @register_if_enabled("tool", "wiki_rebuild_index", mcp.tool())
    def wiki_rebuild_index() -> dict:
        """Rebuild the derived SQLite index from canonical Markdown."""

        return service.rebuild_index()

    @register_if_enabled("tool", "pdf_extract_text", mcp.tool())
    def pdf_extract_text(
        pdf_path: str,
        pages: str | None = None,
        reflection_language: str = "ko",
    ) -> list[dict]:
        """Extract original PDF text for selected pages."""

        return service.extract_pdf_text(
            pdf_path,
            pages=pages,
            reflection_language=reflection_language,
        )

    @register_if_enabled("tool", "pdf_render_screenshots", mcp.tool())
    def pdf_render_screenshots(
        pdf_path: str,
        pages: str | None = None,
        dpi: int = 144,
        reflection_language: str = "ko",
    ) -> list[dict]:
        """Render selected PDF pages as PNG-plus-text artifacts."""

        return service.render_pdf_screenshots(
            pdf_path,
            pages=pages,
            dpi=dpi,
            reflection_language=reflection_language,
        )

    @register_if_enabled("tool", "wiki_publish_pdf_screenshots", mcp.tool())
    def wiki_publish_pdf_screenshots(
        pdf_path: str,
        asset_group: str,
        author: str,
        author_email: str,
        pages: str | None = None,
        dpi: int = 144,
        reflection_language: str = "ko",
    ) -> list[dict]:
        """Publish selected PDF pages as Git-managed WIKI images with Markdown snippets."""

        return service.publish_pdf_screenshots(
            pdf_path=pdf_path,
            asset_group=asset_group,
            author=author,
            author_email=author_email,
            pages=pages,
            dpi=dpi,
            reflection_language=reflection_language,
        )

    @register_if_enabled("tool", "prepare_comparison_workflow", mcp.tool())
    def prepare_comparison_workflow(topic: str, source_slugs: list[str], language: str = "ko") -> dict:
        """Prepare an optional client-side comparison synthesis task."""

        return {
            "topic": topic,
            "source_slugs": source_slugs,
            "language": language,
            "next_step": "Use the comparison_reflection prompt, then save a comparison page with wiki_save_page.",
        }

    @register_if_enabled("prompt", "paper_ingest_workflow", mcp.prompt())
    def paper_ingest_workflow(
        pdf_path: str,
        reading_mode: str = "text",
        pages: str = "",
        reflection_language: str = "ko",
        include_comparison: str = "false",
    ) -> str:
        """Guide a client through paper extraction and WIKI reflection."""

        return _paper_ingest_prompt(pdf_path, reading_mode, pages, reflection_language, include_comparison)

    @register_if_enabled("prompt", "claim_refinement_workflow", mcp.prompt())
    def claim_refinement_workflow(claim_slug: str, reflection_language: str = "ko") -> str:
        """Guide client-side claim fitness assessment."""

        return _claim_refinement_prompt(claim_slug, reflection_language)

    @register_if_enabled("prompt", "novelty_review_workflow", mcp.prompt())
    def novelty_review_workflow(claim_slug: str, reflection_language: str = "ko") -> str:
        """Guide client-side novelty review."""

        return _novelty_review_prompt(claim_slug, reflection_language)

    return mcp


def create_http_app(config: AppConfig, *, shared_token: str) -> ASGIApp:
    """Return the token-protected Streamable HTTP ASGI application."""

    return SharedTokenMiddleware(
        create_server(config).streamable_http_app(),
        token=shared_token,
    )


def load_shared_token(config: AppConfig, environ: dict[str, str] | None = None) -> str:
    """Read the shared HTTP token from the configured environment variable."""

    token = (environ or os.environ).get(config.shared_token_env, "")
    if not token:
        raise RuntimeError(f"Set {config.shared_token_env} before starting Streamable HTTP")
    return token


def run_streamable_http(config: AppConfig, *, shared_token: str) -> None:
    """Run the token-protected Streamable HTTP MCP endpoint."""

    import uvicorn

    uvicorn.run(
        create_http_app(config, shared_token=shared_token),
        host=config.http_host,
        port=config.http_port,
        log_level="info",
    )


def _paper_ingest_prompt(
    pdf_path: str,
    reading_mode: str,
    pages: str,
    reflection_language: str,
    include_comparison: str,
) -> str:
    language_instruction = "한국어" if reflection_language == "ko" else "English"
    tool_name = "pdf_extract_text" if reading_mode == "text" else "pdf_render_screenshots"
    return (
        f"{tool_name}를 사용하여 로컬 PDF `{pdf_path}`를 읽으세요. "
        f"페이지 범위는 `{pages or '전체'}`, WIKI 반영 언어는 {language_instruction}입니다. "
        "원문 근거와 해석을 구분하여 source 페이지와 재사용 가능한 concept 페이지를 draft로 저장하세요. "
        f"comparison 요청 여부는 `{include_comparison}`입니다."
    )


def _claim_refinement_prompt(claim_slug: str, reflection_language: str) -> str:
    language_instruction = "한국어" if reflection_language == "ko" else "English"
    return (
        f"`claim/{claim_slug}`를 읽고 {language_instruction}로 claim fitness를 검토하세요. "
        "동기, 원리적 insight, 기존 연구와의 겹침, 필요한 실험, 미해결 위험을 분리하여 같은 claim 페이지에 반영하세요."
    )


def _novelty_review_prompt(claim_slug: str, reflection_language: str) -> str:
    language_instruction = "한국어" if reflection_language == "ko" else "English"
    return (
        f"`claim/{claim_slug}`에 대해 {language_instruction}로 novelty review를 수행하세요. "
        "가장 가까운 prior art, mechanism-level overlap, 남는 차이, 검증 실험, 불확실성을 구분하여 저장하세요."
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Research WIKI MCP server.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root containing wiki/, raw/, and data/.")
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default="stdio",
        help="MCP transport to run.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Streamable HTTP bind host.")
    parser.add_argument("--port", type=int, default=8765, help="Streamable HTTP bind port.")
    args = parser.parse_args(argv)
    config = replace(AppConfig.from_root(args.root), http_host=args.host, http_port=args.port)
    if args.transport == "stdio":
        create_server(config).run(transport="stdio")
        return
    run_streamable_http(config, shared_token=load_shared_token(config))


if __name__ == "__main__":
    main()
