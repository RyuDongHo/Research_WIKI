"""Local PDF extraction for client-side research reasoning workflows."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from importlib.util import find_spec
from pathlib import Path
import re

from .config import AppConfig
from .models import CONTENT_LANGUAGES

PAGE_PART_PATTERN = re.compile(r"(?P<start>\d+)(?:-(?P<end>\d+))?")


@dataclass(frozen=True)
class PdfPageText:
    page_number: int
    text: str
    reflection_language: str


@dataclass(frozen=True)
class ScreenshotArtifact:
    page_number: int
    image_path: Path
    text: str
    reflection_language: str


def parse_page_range(spec: str | None, *, total_pages: int) -> tuple[int, ...]:
    """Parse 1-based page selections such as ``1-3,5``."""

    if total_pages < 1:
        raise ValueError("PDF must contain at least one page")
    if spec is None or not spec.strip():
        return tuple(range(1, total_pages + 1))

    pages: set[int] = set()
    for raw_part in spec.split(","):
        part = raw_part.strip()
        match = PAGE_PART_PATTERN.fullmatch(part)
        if match is None:
            raise ValueError(f"invalid page-range segment: {part or '<empty>'}")
        start = int(match.group("start"))
        end = int(match.group("end") or start)
        if start < 1 or end < 1:
            raise ValueError("page numbers must be positive")
        if start > end:
            raise ValueError(f"page range must be ascending: {part}")
        if end > total_pages:
            raise ValueError(f"page range exceeds PDF page count ({total_pages}): {part}")
        pages.update(range(start, end + 1))
    return tuple(sorted(pages))


def validate_reflection_language(language: str) -> str:
    if language not in CONTENT_LANGUAGES:
        raise ValueError(f"reflection_language must be one of: {', '.join(sorted(CONTENT_LANGUAGES))}")
    return language


class PdfExtractor:
    """Extract text and screenshot artifacts from local PDF files."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.config.ensure_workspace_layout()

    def page_count(self, pdf_path: str | Path) -> int:
        path = self._validate_pdf_path(pdf_path)
        if self._has_pymupdf():
            import fitz  # type: ignore

            with fitz.open(path) as document:
                return len(document)
        if self._has_pypdf():
            from pypdf import PdfReader  # type: ignore

            return len(PdfReader(str(path)).pages)
        raise RuntimeError("PDF text extraction requires PyMuPDF (`pymupdf`) or `pypdf`")

    def extract_text(
        self,
        pdf_path: str | Path,
        *,
        pages: str | None = None,
        reflection_language: str = "ko",
    ) -> tuple[PdfPageText, ...]:
        path = self._validate_pdf_path(pdf_path)
        language = validate_reflection_language(reflection_language)
        if self._has_pymupdf():
            return self._extract_text_with_pymupdf(path, pages, language)
        if self._has_pypdf():
            return self._extract_text_with_pypdf(path, pages, language)
        raise RuntimeError("PDF text extraction requires PyMuPDF (`pymupdf`) or `pypdf`")

    def render_screenshots(
        self,
        pdf_path: str | Path,
        *,
        pages: str | None = None,
        dpi: int = 144,
        reflection_language: str = "ko",
    ) -> tuple[ScreenshotArtifact, ...]:
        path = self._validate_pdf_path(pdf_path)
        language = validate_reflection_language(reflection_language)
        if dpi < 72 or dpi > 600:
            raise ValueError("dpi must be between 72 and 600")
        if not self._has_pymupdf():
            raise RuntimeError("Screenshot extraction requires PyMuPDF (`pymupdf`)")

        import fitz  # type: ignore

        output_root = self._screenshot_output_root(path)
        output_root.mkdir(parents=True, exist_ok=True)
        artifacts = []
        with fitz.open(path) as document:
            selected_pages = parse_page_range(pages, total_pages=len(document))
            for page_number in selected_pages:
                page = document[page_number - 1]
                image_path = output_root / f"page-{page_number:04d}.png"
                page.get_pixmap(dpi=dpi, alpha=False).save(image_path)
                artifacts.append(
                    ScreenshotArtifact(
                        page_number=page_number,
                        image_path=image_path,
                        text=page.get_text("text"),
                        reflection_language=language,
                    )
                )
        return tuple(artifacts)

    def _extract_text_with_pymupdf(
        self,
        path: Path,
        pages: str | None,
        reflection_language: str,
    ) -> tuple[PdfPageText, ...]:
        import fitz  # type: ignore

        chunks = []
        with fitz.open(path) as document:
            selected_pages = parse_page_range(pages, total_pages=len(document))
            for page_number in selected_pages:
                chunks.append(
                    PdfPageText(
                        page_number=page_number,
                        text=document[page_number - 1].get_text("text"),
                        reflection_language=reflection_language,
                    )
                )
        return tuple(chunks)

    def _extract_text_with_pypdf(
        self,
        path: Path,
        pages: str | None,
        reflection_language: str,
    ) -> tuple[PdfPageText, ...]:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        selected_pages = parse_page_range(pages, total_pages=len(reader.pages))
        return tuple(
            PdfPageText(
                page_number=page_number,
                text=reader.pages[page_number - 1].extract_text() or "",
                reflection_language=reflection_language,
            )
            for page_number in selected_pages
        )

    def _screenshot_output_root(self, path: Path) -> Path:
        safe_stem = re.sub(r"[^a-zA-Z0-9._-]+", "-", path.stem).strip("-") or "paper"
        path_digest = sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:12]
        return self.config.screenshots_root / f"{safe_stem}-{path_digest}"

    @staticmethod
    def _validate_pdf_path(pdf_path: str | Path) -> Path:
        path = Path(pdf_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"PDF file not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"local PDF path must end with .pdf: {path}")
        return path

    @staticmethod
    def _has_pymupdf() -> bool:
        return find_spec("fitz") is not None

    @staticmethod
    def _has_pypdf() -> bool:
        return find_spec("pypdf") is not None
