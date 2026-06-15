"""Configurable MCP capability catalog shared by the server and local GUI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .config import AppConfig


@dataclass(frozen=True)
class McpCapability:
    """Describe one MCP primitive that can be enabled at server startup."""

    kind: str
    name: str
    description: str
    target: str = ""

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.name}"


CAPABILITIES = (
    McpCapability("resource", "wiki_index", "검색 가능한 전체 WIKI 인덱스를 반환합니다.", "wiki://index"),
    McpCapability("resource", "wiki_papers", "로컬 PDF의 WIKI 반영 상태를 반환합니다.", "wiki://papers"),
    McpCapability("resource", "wiki_page", "하나의 canonical WIKI 페이지를 반환합니다.", "wiki://page/{page_type}/{slug}"),
    McpCapability("tool", "wiki_search", "canonical WIKI 내용을 검색합니다."),
    McpCapability("tool", "wiki_read_page", "하나의 canonical Markdown 페이지를 구조화하여 읽습니다."),
    McpCapability("tool", "wiki_save_page", "Git 관리 Markdown 페이지를 생성하거나 수정합니다."),
    McpCapability("tool", "wiki_create_research_page", "사용자 주도 claim 또는 question 페이지를 생성합니다."),
    McpCapability("tool", "wiki_capture_discussion", "대화 중 재사용 가치가 있다고 판단한 연구 지식을 적절한 WIKI 페이지에 추가합니다."),
    McpCapability("tool", "wiki_review_page", "draft 페이지를 reviewed 상태로 승격합니다."),
    McpCapability("tool", "wiki_list_revisions", "한 WIKI 페이지의 Git revision 목록을 반환합니다."),
    McpCapability("tool", "wiki_restore_revision", "이전 Git revision의 WIKI 페이지를 복원합니다."),
    McpCapability("tool", "wiki_rebuild_index", "Markdown 원본에서 SQLite 검색 인덱스를 다시 만듭니다."),
    McpCapability("tool", "pdf_extract_text", "선택한 PDF 페이지에서 원문 텍스트를 추출합니다."),
    McpCapability("tool", "pdf_render_screenshots", "선택한 PDF 페이지를 PNG와 텍스트 artifact로 변환합니다."),
    McpCapability("tool", "wiki_publish_pdf_screenshots", "선택한 PDF 페이지를 Git 관리 WIKI 이미지로 저장하고 Markdown 삽입 문법을 반환합니다."),
    McpCapability("tool", "prepare_comparison_workflow", "선택한 source를 비교하기 위한 client-side 작업을 준비합니다."),
    McpCapability("prompt", "paper_ingest_workflow", "PDF 읽기와 source 및 concept 반영 절차를 안내합니다."),
    McpCapability("prompt", "claim_refinement_workflow", "claim fitness 검토 절차를 안내합니다."),
    McpCapability("prompt", "novelty_review_workflow", "claim novelty 검토 절차를 안내합니다."),
)


class McpSettingsStore:
    """Read and write startup-time MCP capability toggles."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.capabilities = CAPABILITIES
        self._known = {capability.key: capability for capability in self.capabilities}

    def is_enabled(self, kind: str, name: str) -> bool:
        """Return whether a capability should be registered on server startup."""

        return self.read()[f"{kind}:{name}"]

    def read(self) -> dict[str, bool]:
        """Return validated settings with defaults for omitted capabilities."""

        settings = {key: True for key in self._known}
        path = self.config.mcp_settings_path
        if not path.is_file():
            return settings
        payload = json.loads(path.read_text(encoding="utf-8"))
        configured = payload.get("capabilities", {})
        if not isinstance(configured, dict):
            raise ValueError("mcp-settings.json capabilities must be an object")
        self._validate(configured)
        settings.update(configured)
        return settings

    def save(self, configured: dict[str, Any]) -> dict[str, bool]:
        """Persist capability toggles while preserving default values."""

        if not isinstance(configured, dict):
            raise ValueError("capabilities must be an object")
        self._validate(configured)
        settings = self.read()
        settings.update(configured)
        payload = {"schema_version": 1, "capabilities": settings}
        path = self.config.mcp_settings_path
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return settings

    def status(self) -> dict[str, Any]:
        """Return GUI-ready catalog status for the next MCP server start."""

        settings = self.read()
        capabilities = [
            {
                **asdict(capability),
                "key": capability.key,
                "enabled": settings[capability.key],
            }
            for capability in self.capabilities
        ]
        return {
            "server": {
                "name": "Research WIKI MCP",
                "settings_path": str(self.config.mcp_settings_path),
                "transports": ["stdio", "streamable-http"],
                "apply_policy": "next-server-start",
            },
            "counts": {
                "total": len(capabilities),
                "enabled": sum(1 for capability in capabilities if capability["enabled"]),
                "disabled": sum(1 for capability in capabilities if not capability["enabled"]),
            },
            "capabilities": capabilities,
        }

    def _validate(self, configured: dict[str, Any]) -> None:
        unknown = sorted(set(configured) - set(self._known))
        if unknown:
            raise ValueError(f"unknown MCP capabilities: {', '.join(unknown)}")
        invalid = sorted(key for key, value in configured.items() if not isinstance(value, bool))
        if invalid:
            raise ValueError(f"MCP capability values must be boolean: {', '.join(invalid)}")
