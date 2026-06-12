---
type: "claim"
slug: "gradient-guided-patch-efficiency"
title: "Gradient 유도 Patch 구성의 표본 효율 우위 주장"
status: "draft"
modified_at: "2026-06-12T17:08:20.601587+00:00"
author: "lab-member"
language: "ko"
confidence: "medium"
sources:
  - "raw/papers/Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks.pdf"
  - "raw/papers/Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture.pdf"
tags:
  - "claim"
  - "gradient-guided"
  - "patch-construction"
  - "sample-efficiency"
---

# Claim: Gradient 유도 Patch 구성은 고정 증강 Pretext보다 표본 효율이 높다

## 주장

사용자 입력 기반 연구 주장. 학습 중 손실 gradient가 큰 영역을 우선 선택해 patch를 구성하는 self-supervised 학습은, Exemplar-CNN처럼 고정 분포에서 무작위 증강을 뽑는 방식보다 동일 연산 예산에서 더 높은 표본 효율을 낸다.

## 근거

- Exemplar-CNN은 "considerable gradient" 기준으로 seed patch를 한 번 선별하는 정적 버전을 이미 사용했다 (p.2-3). 이 선별을 학습 중 동적으로 갱신하는 것이 주장의 핵심 확장이다.
- I-JEPA는 target 블록 선택 전략(크기, 위치 분포)이 표현 품질을 좌우함을 보였다 (p.6 ablation). 선택 전략 자체가 학습 신호 품질을 결정한다는 간접 근거다.
- 관련 질문 페이지: [[gradient-guided-patch-construction]] — crop 샘플링 가중과 patch 생성 유도의 구분, ablation 설계를 관리한다.

## 선행연구 리스크

- Hard example mining과 curriculum 계열(예: hard negative mining, RHO-LOSS)이 지도학습에서 같은 직관을 이미 검증했다. self-supervised patch 구성으로의 이전이 신규성의 경계다.
- Adversarial augmentation 계열(예: AutoAugment 계열의 학습된 증강 정책)과의 차별점을 명시해야 한다. 본 주장은 증강 정책이 아니라 patch 공간 구성을 gradient로 유도한다는 점에서 다르다.

## 검증 계획

1. Exemplar-CNN 재현 baseline 대비 gradient 가중 crop 샘플링의 STL-10 선형 평가 비교.
2. 동일 연산 예산(보는 patch 수 고정)에서 표본 효율 곡선 비교.
3. gradient 갱신 주기(매 step, 매 epoch)에 따른 안정성-효율 trade-off ablation.

## 상태

- 신뢰도: medium — 정적 선별의 효과는 문헌 근거가 있으나 동적 갱신의 이득은 미검증.
- 다음 행동: baseline 재현 후 novelty review 워크플로로 선행연구 충돌 재검사.
