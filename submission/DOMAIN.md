# 지식 도메인 정의: 자기지도학습(Self-Supervised Learning) 연구 WIKI

Status: 운영 중 (논문 6편 반영 완료)
Updated: 2026-06-13

## 1. 선정한 지식 도메인

본 WIKI는 **컴퓨터 비전 분야의 자기지도 표현 학습(Self-Supervised Visual Representation Learning)** 연구를 지식 도메인으로 한다. 과제 기본값(CSE-3308 강의 내용) 대신, 실제 연구실 워크플로에서 LLM 에이전트가 논문을 읽고 지식을 축적·재사용하는 **연구용 WIKI**를 구축하는 것을 목표로 선택했다.

선정 이유:

- 강의 자료 정리보다 검증 난도가 높은 실사용 시나리오(논문 PDF 근거 추출, 페이지 단위 인용, 주장과 반례 관리)를 다룰 수 있다.
- 동일 도메인 안에서 논문 간 비교(`comparison`), 연구 주장(`claim`), 열린 질문(`question`)이 자연스럽게 발생하여 WIKI 객체 모델 전체를 실제로 사용하게 된다.
- 연구실 구성원과 AI 에이전트(Codex, Claude Code)가 같은 지식 기반을 공유하는 MCP 협업 구조를 검증할 수 있다.

## 2. 도메인 범위

### 포함 범위

| 하위 주제 | 설명 | 반영된 대표 논문 |
| --- | --- | --- |
| Pretext task 기반 SSL | 데이터 자체에서 학습 신호를 만드는 사전 과제 설계 | Exemplar-CNN, Context Prediction, Jigsaw Puzzle |
| 변환 불변성과 등변성 | 어떤 변환에 불변/등변해야 좋은 표현인가 | Rotation Feature Decoupling |
| 자기증류 계열 | 레이블 없이 teacher-student 구조로 학습 | DINO |
| 잠재 공간 예측 계열 | 픽셀이 아닌 표현 공간에서의 예측 학습 | I-JEPA |

### 제외 범위

- 자연어 처리 분야의 자기지도학습 (BERT 계열 등)
- 지도학습 기반 전이학습 일반론
- 강의 노트, 과제 풀이 등 비연구 콘텐츠

## 3. 지식 객체 모델

도메인 지식은 다음 7가지 페이지 유형으로 구조화한다. 상세 스키마는 `wiki/system/page-schema.md`에 있다.

| 유형 | 역할 | 도메인 내 예시 |
| --- | --- | --- |
| `source` | 한 논문의 근거 중심 정리 (페이지·수식 앵커 포함) | `wiki/sources/exemplar-cnn.md` |
| `concept` | 논문을 가로지르는 재사용 가능한 메커니즘 | `wiki/concepts/instance-discrimination.md` |
| `comparison` | 사용자가 요청한 논문 간 비교 분석 | `wiki/comparisons/pretext-vs-self-distillation.md` |
| `claim` | 사용자 입력 기반 연구 주장과 선행연구 리스크 | `wiki/claims/gradient-guided-patch-efficiency.md` |
| `question` | 열린 연구 질문 관리 | `wiki/questions/gradient-guided-patch-construction.md` |
| `system` | WIKI 운영 문서 | `wiki/system/page-schema.md` |
| `skill` | 재사용 가능한 에이전트 워크플로 | (필요 시 생성) |

## 4. 현재 반영된 지식 현황

반영 완료 논문 6편은 `source` + `concept` 반영을 마쳐 GUI에서 파란색 상태이며, 6편 전체를 묶은 비교 분석으로 비교 배지가 켜져 있다. SimCLR는 다음 반영 대상으로 빨간색(미반영) 상태다.

- **Source 페이지 6편**: Exemplar-CNN(reviewed), Context Prediction, Jigsaw Puzzle Pretext, Rotation Feature Decoupling, DINO, I-JEPA
- **Concept 페이지 8편**: instance discrimination(reviewed), joint embedding prediction, momentum target encoders, self-distillation without labels, self-supervised pretext tasks, shortcut avoidance, spatial context and part reasoning, transformation invariance and equivariance
- **Comparison 페이지 1편**: pretext task 계열 vs 표현 공간 예측·자기증류 계열 (논문 6편 전체 비교, reviewed)
- **Claim 페이지 1편**: gradient 유도 patch 구성의 표본 효율 우위 주장 (검증 계획·선행연구 리스크 포함)
- **Question 페이지 1편**: gradient-guided patch construction (Exemplar-CNN 논의에서 파생된 연구 질문)
- **이미지 근거**: Exemplar-CNN 핵심 figure/table 6장이 `wiki/assets/`에 Git 관리 이미지로 게시되어 본문에 인용됨

## 5. 지식 축적 원칙

- **근거 우선**: 모든 `source` 페이지는 PDF 파일 경로와 페이지/수식 앵커를 메타데이터로 기록한다.
- **출처 추적**: AI가 작성한 페이지는 `draft`로 시작하고, 연구자가 검토 후 `reviewed`로 승격한다.
- **언어 정책**: 한국어 정리가 기본이며 영어 정리는 명시적 요청 시에만 허용한다.
- **재구성 가능성**: Markdown + Git이 canonical이고, SQLite 인덱스는 언제든 재생성 가능한 파생물이다.
- **대화 지식 보존**: Codex/Claude Code와의 연구 토론 중 재사용 가치가 있는 해석은 `wiki_capture_discussion` 도구로 WIKI에 흡수한다.
