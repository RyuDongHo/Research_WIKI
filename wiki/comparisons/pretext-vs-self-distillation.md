---
type: "comparison"
slug: "pretext-vs-self-distillation"
title: "Pretext Task 계열 vs 표현 공간 예측·자기증류 계열"
status: "draft"
modified_at: "2026-06-12T17:08:19.900025+00:00"
author: "lab-member"
language: "ko"
confidence: "medium"
sources:
  - "raw/papers/Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks.pdf"
  - "raw/papers/Unsupervised Visual Representation Learning by Context Prediction.pdf"
  - "raw/papers/Unsupervised Learning of Visual Representations by Solving Jigsaw Puzzles.pdf"
  - "raw/papers/Self-Supervised Representation Learning by Rotation Feature Decoupling.pdf"
  - "raw/papers/Emerging Properties in Self-Supervised Vision Transformers.pdf"
  - "raw/papers/Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture.pdf"
tags:
  - "comparison"
  - "self-supervised-learning"
  - "pretext-task"
  - "self-distillation"
  - "jepa"
---

# Pretext Task 계열 vs 표현 공간 예측·자기증류 계열 비교

## 비교 목적

사용자 요청에 따라, 반영된 논문 6편을 학습 신호의 출처 기준으로 두 계열로 나누어 비교한다. 설계 공간의 양 끝을 정리해 다음 연구 질문([[gradient-guided-patch-construction]])의 위치를 잡는 것이 목적이다.

## 계열 구분

| 계열 | 논문 | 학습 신호 |
| --- | --- | --- |
| Pretext task 계열 | Exemplar-CNN, Context Prediction, Jigsaw Puzzle, Rotation Feature Decoupling | 사람이 설계한 사전 과제의 정답 (인스턴스 분류, 상대 위치, 퍼즐 순열, 회전 각도) |
| 표현 공간 예측·자기증류 계열 | DINO, I-JEPA | 다른 view 또는 다른 encoder가 만든 표현 자체 |

## 축별 비교

### 1. 학습 신호의 출처

- Pretext 계열은 입력 변환에서 기계적으로 정답을 만든다. 신호가 명시적이고 해석 가능하지만, 과제 풀이에 필요한 정보만 남기는 지름길 학습 위험이 있다 (Context Prediction의 색수차 지름길, p.4 참고).
- DINO는 student-teacher 출력 분포 일치, I-JEPA는 target encoder 표현 예측을 신호로 쓴다. 신호가 표현 공간 안에 있어 과제 설계 부담이 없지만, collapse 방지 장치(momentum teacher, centering, 예측기 비대칭)가 필수다. [[momentum-target-encoders]], [[self-distillation-without-labels]] 참고.

### 2. 불변성과 등변성의 처리

- Exemplar-CNN은 같은 patch의 모든 증강에 같은 클래스를 부여해 변환 불변성을 직접 강제한다. Rotation Feature Decoupling은 회전 예측(등변)과 인스턴스 일치(불변)를 분리해 두 성질을 공존시킨다. [[transformation-invariance-and-equivariance]] 참고.
- DINO는 multi-crop 증강 일치로 불변성을 암묵적으로 얻고, I-JEPA는 증강 불변성 대신 공간 예측 구조로 의미를 학습해 hand-crafted 증강 의존을 줄인다.

### 3. 공간 구조 활용

- Context Prediction과 Jigsaw는 patch 간 상대 배치를 과제로 만들어 부분-전체 구조를 명시적으로 학습한다. [[spatial-context-and-part-reasoning]] 참고.
- I-JEPA는 같은 발상을 표현 공간 예측으로 옮긴 후속 형태로 읽을 수 있다. masked target 블록의 표현을 context 블록에서 예측하는 구조는 Jigsaw의 순열 분류보다 학습 신호가 조밀하다.

### 4. 한계 비교

- Pretext 계열: 과제 난이도와 표현 품질의 상관이 보장되지 않고, 지름길 차단 장치(채널 드롭, 색 보정, 퍼즐 순열 선별)가 과제마다 새로 필요하다. [[shortcut-avoidance-in-self-supervision]] 참고.
- 자기증류·예측 계열: 대규모 배치, ViT 백본, momentum 스케줄 등 학습 안정화 비용이 크고, 신호가 암묵적이라 실패 원인 분석이 어렵다.

## 종합

설계 흐름은 "사람이 정답을 설계"에서 "모델이 만든 표현을 정답으로 사용"으로 이동했다. 다만 Pretext 계열의 명시적 신호는 데이터가 적거나 도메인이 특수한 연구실 환경에서 여전히 유효하며, Exemplar-CNN식 인스턴스 구분([[instance-discrimination]])은 contrastive 계열의 직계 조상으로 양쪽을 잇는 다리 역할을 한다. 다음 단계 질문은 gradient 신호로 patch 구성을 유도할 때 두 계열의 장점을 결합할 수 있는가이다.

## 근거 앵커

- Exemplar-CNN: 분류 목적식 Eq.1-2 (p.3), 증강 불변성 논의 (p.2-3)
- Context Prediction: 색수차 지름길과 완화 (p.4)
- Jigsaw: 순열 선별과 지름길 차단 (p.5-6)
- Rotation Feature Decoupling: 회전 예측과 인스턴스 일치 분리 목적식 (p.3-4)
- DINO: momentum teacher와 centering의 collapse 방지 (p.4-5)
- I-JEPA: 표현 공간 예측 구조와 증강 불변성 비교 (p.2-3, p.6)
