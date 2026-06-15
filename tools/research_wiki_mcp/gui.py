"""Local web GUI for browsing and editing the shared research WIKI."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Awaitable, Callable
from urllib.parse import quote

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse, Response
from starlette.routing import Route
import uvicorn

from .config import AppConfig
from .mcp_catalog import McpSettingsStore
from .service import ResearchWikiService

JsonEndpoint = Callable[[Request], Awaitable[Response]]
PAGE_TYPES = ("source", "concept", "comparison", "claim", "question", "system", "skill")


def _json_endpoint(handler: JsonEndpoint) -> JsonEndpoint:
    """Return useful JSON failures for local GUI requests."""

    async def wrapped(request: Request) -> Response:
        try:
            return await handler(request)
        except FileNotFoundError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)
        except (KeyError, TypeError, ValueError) as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    return wrapped


def _asset_html() -> str:
    return (Path(__file__).with_name("gui_assets") / "index.html").read_text(encoding="utf-8")


def create_gui_app(config: AppConfig) -> Starlette:
    """Create the local-only GUI application."""

    service = ResearchWikiService(config)
    mcp_settings = McpSettingsStore(config)

    async def homepage(_: Request) -> Response:
        return HTMLResponse(_asset_html())

    @_json_endpoint
    async def dashboard(request: Request) -> Response:
        query = request.query_params.get("q", "")
        pages = service.search(query, limit=500)
        papers = service.list_papers()
        return JSONResponse(
            {
                "papers": papers,
                "pages": pages,
                "stats": {
                    "papers": len(papers),
                    "reflected_papers": sum(1 for paper in papers if paper["reflected"]),
                    "pages": len(pages),
                    "drafts": sum(1 for page in pages if page["status"] == "draft"),
                    "reviewed": sum(1 for page in pages if page["status"] == "reviewed"),
                },
                "page_types": PAGE_TYPES,
                "languages": ("ko", "en"),
            }
        )

    @_json_endpoint
    async def read_page(request: Request) -> Response:
        return JSONResponse(
            service.read_page(
                request.path_params["page_type"],
                request.path_params["slug"],
            )
        )

    @_json_endpoint
    async def save_page(request: Request) -> Response:
        payload = await request.json()
        return JSONResponse(
            service.save_page(
                page_type=payload["page_type"],
                slug=payload["slug"],
                title=payload["title"],
                author=payload["author"],
                author_email=payload["author_email"],
                body=payload.get("body", ""),
                status=payload.get("status", "draft"),
                language=payload.get("language", "ko"),
                confidence=payload.get("confidence", "low"),
                sources=payload.get("sources", []),
                tags=payload.get("tags", []),
            )
        )

    @_json_endpoint
    async def review_page(request: Request) -> Response:
        payload = await request.json()
        return JSONResponse(
            service.review_page(
                request.path_params["page_type"],
                request.path_params["slug"],
                author=payload["author"],
                author_email=payload["author_email"],
            )
        )

    @_json_endpoint
    async def rebuild_index(_: Request) -> Response:
        return JSONResponse(service.rebuild_index())

    @_json_endpoint
    async def mcp_status(_: Request) -> Response:
        return JSONResponse(mcp_settings.status())

    @_json_endpoint
    async def save_mcp_settings(request: Request) -> Response:
        payload = await request.json()
        mcp_settings.save(payload["capabilities"])
        return JSONResponse(mcp_settings.status())

    @_json_endpoint
    async def preview_pdf(request: Request) -> Response:
        payload = await request.json()
        reading_mode = payload.get("reading_mode", "text")
        common = {
            "pdf_path": payload["pdf_path"],
            "pages": payload.get("pages") or None,
            "reflection_language": payload.get("reflection_language", "ko"),
        }
        if reading_mode == "text":
            artifacts = service.extract_pdf_text(**common)
        elif reading_mode == "screenshot":
            artifacts = service.render_pdf_screenshots(
                **common,
                dpi=int(payload.get("dpi", 144)),
            )
            for artifact in artifacts:
                image_path = Path(artifact["image_path"]).resolve()
                relative = image_path.relative_to(config.screenshots_root.resolve())
                artifact["image_url"] = f"/artifacts/screenshots/{quote(relative.as_posix())}"
        else:
            raise ValueError("reading_mode must be text or screenshot")
        for artifact in artifacts:
            artifact["pdf_name"] = Path(payload["pdf_path"]).name
        return JSONResponse({"reading_mode": reading_mode, "artifacts": artifacts})

    @_json_endpoint
    async def register_pdf_source(request: Request) -> Response:
        payload = await request.json()
        return JSONResponse(
            service.register_pdf_source_draft(
                pdf_path=payload["pdf_path"],
                title=payload.get("title", ""),
                slug=payload.get("slug", ""),
                author=payload["author"],
                author_email=payload["author_email"],
                reading_mode=payload.get("reading_mode", "text"),
                pages=payload.get("pages") or None,
                dpi=int(payload.get("dpi", 144)),
                reflection_language=payload.get("reflection_language", "ko"),
            )
        )

    async def screenshot_artifact(request: Request) -> Response:
        relative = Path(request.path_params["artifact_path"])
        root = config.screenshots_root.resolve()
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            return JSONResponse({"error": "artifact path is outside screenshot root"}, status_code=404)
        if not candidate.is_file():
            return JSONResponse({"error": "artifact not found"}, status_code=404)
        return FileResponse(candidate)

    async def wiki_asset(request: Request) -> Response:
        relative = Path(request.path_params["asset_path"])
        root = config.wiki_assets_root.resolve()
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            return JSONResponse({"error": "asset path is outside WIKI asset root"}, status_code=404)
        if not candidate.is_file():
            return JSONResponse({"error": "asset not found"}, status_code=404)
        return FileResponse(candidate)

    app = Starlette(
        routes=[
            Route("/", homepage),
            Route("/api/dashboard", dashboard),
            Route("/api/pages", save_page, methods=["POST"]),
            Route("/api/pages/{page_type}/{slug}", read_page),
            Route("/api/pages/{page_type}/{slug}/review", review_page, methods=["POST"]),
            Route("/api/index/rebuild", rebuild_index, methods=["POST"]),
            Route("/api/mcp/status", mcp_status),
            Route("/api/mcp/settings", save_mcp_settings, methods=["POST"]),
            Route("/api/pdf/preview", preview_pdf, methods=["POST"]),
            Route("/api/pdf/register-source", register_pdf_source, methods=["POST"]),
            Route("/artifacts/screenshots/{artifact_path:path}", screenshot_artifact),
            Route("/assets/wiki/{asset_path:path}", wiki_asset),
        ]
    )
    app.state.service = service
    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local research WIKI GUI")
    parser.add_argument("--root", default=".", help="project root containing wiki/ and raw/")
    parser.add_argument("--host", default="127.0.0.1", help="local bind host")
    parser.add_argument("--port", default=8780, type=int, help="local bind port")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = AppConfig.from_root(args.root)
    uvicorn.run(create_gui_app(config), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
