---
type: "concept"
slug: "instance-discrimination"
title: "Instance Discrimination"
status: "reviewed"
modified_at: "2026-06-12T17:08:23.149094+00:00"
author: "lab-member"
language: "ko"
confidence: "high"
sources:
  - "raw/papers/Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks.pdf"
  - "raw/papers/Self-Supervised Representation Learning by Rotation Feature Decoupling.pdf"
tags:
  - "self-supervised-learning"
  - "instance-discrimination"
  - "contrastive-learning"
  - "invariance"
---

# Instance Discrimination

## 정의
각 이미지 또는 패치를 개별 instance로 보고, 서로 다른 instance는 구분하면서 같은 instance의 허용된 변형은 가까운 표현으로 만드는 자기지도 학습 관점이다.

## 논문 연결
- Exemplar-CNN은 seed patch마다 surrogate class를 부여하여 이 아이디어를 직접 구현한다.
- Rotation Feature Decoupling은 non-parametric NCE instance classification을 rotation-unrelated feature에 적용한다.

## 핵심 쟁점
instance discrimination은 강한 구별 능력을 만들지만, augmentation으로 무엇을 같은 instance로 볼지 결정해야 한다. 변환 정보를 완전히 제거하면 방향이나 자세가 중요한 downstream task에 불리할 수 있다.

## 연구 질문
- instance identity와 semantic identity 사이의 간극을 어떻게 줄일 것인가?
- 어떤 변환은 불변으로 만들고 어떤 변환은 별도 feature로 보존할 것인가?
