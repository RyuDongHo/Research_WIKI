---
type: "source"
slug: "exemplar-cnn"
title: "Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks"
status: "reviewed"
modified_at: "2026-06-12T17:08:22.245062+00:00"
author: "lab-member"
language: "ko"
confidence: "high"
sources:
  - "raw/papers/Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks.pdf"
tags:
  - "self-supervised-learning"
  - "instance-discrimination"
  - "surrogate-classes"
  - "augmentation-invariance"
  - "cnn"
  - "descriptor-matching"
  - "blur-robustness"
  - "equations"
---

# Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks

## Paper
- 저자: Alexey Dosovitskiy, Philipp Fischer, Jost Tobias Springenberg, Martin Riedmiller, Thomas Brox
- PDF 버전: arXiv:1406.6909v2, 2015-06-19
- 주제: 라벨 없이 CNN 표현을 학습하기 위한 surrogate-class 기반 discriminative unsupervised learning
- PDF: `raw/papers/Discriminative Unsupervised Feature Learning with Exemplar Convolutional Neural Networks.pdf`

## Main Claim
무작위로 선택한 이미지 패치 하나를 하나의 `surrogate class`로 보고, 해당 패치에 여러 변환을 적용한 샘플을 같은 클래스로 분류하도록 CNN을 학습하면 라벨 없이도 범용 시각 표현을 얻을 수 있다. 이 표현은 서로 다른 패치를 구별하는 `discriminative` 성질과 학습 시 사용한 변환에 대한 `invariance`를 함께 갖는다.

## Paper Says: Motivation and Previous Work
### 문제
지도 CNN은 분류, 탐지, 분할에서 강하지만 초기 학습에 대규모 라벨 데이터가 필요하다. 또한 분류 라벨로 학습한 특징은 descriptor matching처럼 class-independent한 작업에는 최적이 아닐 수 있다. 저자들은 라벨 없이도 descriptive하고 변형에 robust한 범용 특징을 학습하려 한다. (p.1)

### 기존 비지도 방식과 차이
기존 방식도 invariant feature를 학습했다. 예를 들어 denoising autoencoder는 perturbation이 적용된 입력에서 원본을 복원하고, video slowness 방식은 시간적으로 인접한 frame의 특징이 천천히 변하도록 한다. 하지만 저자들은 이러한 방식이 입력 분포 `p(x)`를 직접 모델링하며, 여러 CNN layer를 jointly train하기 어렵다고 본다. (p.2-3)

Exemplar-CNN은 입력 복원을 요구하지 않는다. 대신 서로 다른 seed patch를 구분하는 discriminative objective를 사용한다. recognition이나 matching에 필요하지 않은 픽셀 세부 복원 의무를 제거하고, 원하는 변형에 대한 invariance를 surrogate-label 구성으로 직접 주입한다. (p.3)

## Paper Says: Surrogate Training Data
### Seed patch sampling
라벨 없는 이미지에서 서로 다른 위치와 scale의 `32x32` patch를 `N`개 뽑는다.

```text
X = {x_1, ..., x_N}
```

물체 또는 물체 일부가 포함된 patch를 선호하기 위해 patch 내부 mean squared gradient magnitude에 비례하여 sampling한다. (p.2)

### Transformation family
변환 family는 `{T_alpha | alpha in A}`로 정의한다. 분류 실험에서는 다음 변환을 조합한다. (p.2)

- translation: patch 크기의 `0.2` 이내 수평 및 수직 이동
- scaling: scale factor `0.7`부터 `1.4`
- rotation: 최대 `20`도 회전
- contrast 1: pixel PCA component별 계수 변화
- contrast 2: HSV saturation과 value 변화
- color: HSV hue 변화
- descriptor matching 확장: blur 추가

각 seed patch `x_i`에 `K`개의 무작위 변환을 적용한다.

```text
T_i = {T_(alpha_i^1), ..., T_(alpha_i^K)}
S_(x_i) = T_i x_i = {T x_i | T in T_i}
```

동일 seed에서 나온 transformed patch 집합 `S_(x_i)`가 하나의 surrogate class가 된다. (p.2)

## Visual Evidence
### Fig. 1-2: surrogate class가 실제로 무엇인지
![PDF page 2](../assets/exemplar-cnn/page-0002-dpi-144.png)

- Fig. 1은 STL unlabeled dataset에서 샘플링한 다양한 seed patch를 보여준다.
- Fig. 2는 하나의 seed patch에 translation, scale, rotation, contrast, color 변형을 적용한 모습을 보여준다.
- 핵심은 의미 라벨이 아니라 `같은 seed에서 파생되었는가`가 surrogate label을 결정한다는 점이다. (p.2)

### Fig. 3: surrogate class 수가 무조건 많을수록 좋은 것은 아니다
- class 수를 `50`부터 `32000`까지 늘리면 STL-10 분류 성능은 약 `8000` class까지 좋아진다.
- 이후 정체하거나 감소한다. 너무 많은 class를 만들면 서로 매우 비슷하거나 사실상 동일한 patch가 다른 label을 받아 collision이 증가하기 때문이다.
- 그림의 red curve는 surrogate validation error가 class 수 증가와 함께 커지는 것을 보여준다. (p.5)

### Fig. 4-5: sample 수와 transformation ablation
![PDF page 6](../assets/exemplar-cnn/page-0006-dpi-144.png)

- Fig. 4에서 surrogate class당 transformed sample 수 `K`를 늘리면 성능이 증가하고 약 `100`개 부근에서 포화한다.
- Fig. 5에서 rotation과 scaling 제거 영향은 상대적으로 작다. translation, color, contrast 제거 영향은 더 크다.
- 즉 augmentation 목록은 장식이 아니라 학습 표현의 성질을 정하는 설계 변수다. (p.6)

### Fig. 6: invariance를 직접 측정
![PDF page 7](../assets/exemplar-cnn/page-0007-dpi-144.png)

- 위쪽 이미지는 한 patch에 translation, rotation, contrast, saturation, color 변형을 점점 강하게 적용한 모습이다.
- Fig. 6(a)-(c)는 원본 patch와 transformed patch feature 사이 normalized Euclidean distance를 보여준다. 변화가 커져도 feature distance가 천천히 증가할수록 해당 변형에 더 robust하다.
- Fig. 6(d)-(f)는 transformed patch에서의 분류 성능을 보여준다. training augmentation 범위를 강하게 설정하면 해당 변형에 더 robust해진다.
- 다만 contrast 변화가 너무 강하면 성능이 나빠질 수 있다. edge strength 자체가 유용한 정보일 수 있기 때문이다. (p.7-8, Appendix C p.13)

### Fig. 8-11: matching task와 blur
![PDF page 10](../assets/exemplar-cnn/page-0010-dpi-144.png)

![PDF page 11](../assets/exemplar-cnn/page-0011-dpi-144.png)

- Fig. 8은 descriptor matching 성능이 patch 크기와 feature를 뽑는 CNN layer에 따라 달라짐을 보여준다. 저자들은 SIFT에는 patch size `157`, CNN 계열에는 `113`을 사용한다. (p.10)
- Fig. 9 scatter plot에서 Flickr dataset에서는 AlexNet과 Exemplar-CNN이 대체로 SIFT보다 좋지만, Mikolajczyk dataset에서는 supervised AlexNet이 SIFT보다 약한 경우가 있다. Exemplar-CNN-blur는 두 dataset에서 AlexNet보다 우수하다. (p.10)
- Fig. 10에서 일반 CNN은 blur에서 크게 약해진다. blur augmentation으로 학습한 Exemplar-CNN-blur는 blur 조건에서도 SIFT에 근접하거나 우수하다. (p.11)
- Fig. 11에서 Mikolajczyk dataset의 strong blur와 lighting에서는 SIFT가 여전히 강하지만, viewpoint 변화에서는 CNN 특징이 강하다. (p.11)

## Key Equations
![PDF page 3](../assets/exemplar-cnn/page-0003-dpi-144.png)

### Eq. 1: surrogate-class classification objective
```text
L(X) = sum_(x_i in X) sum_(T in T_i) l(i, T x_i)
```

- `x_i`: i번째 seed patch
- `T x_i`: seed patch에 변환을 적용한 sample
- `i`: 의미 class가 아니라 seed patch의 identity
- 역할: 서로 다른 seed patch는 구별하고, 같은 seed에서 나온 transformed sample은 같은 label로 예측하게 한다. (p.2)

### Eq. 2: multinomial negative log likelihood
```text
l(i, T x_i) = M(e_i, f(T x_i))
M(y, f) = -<y, log f> = -sum_k y_k log f_k
```

일반적인 softmax cross-entropy 분류 loss다. 특별한 loss를 새로 만들지 않고 surrogate label을 구성하는 방식으로 비지도 학습 문제를 만든다. (p.3)

### Eq. 3: transformation sampling을 무한히 늘린 이상적 목적함수
```text
L_hat(X) = sum_(x_i in X) E_alpha[l(i, T_alpha x_i)]
```

실제 구현은 class당 유한한 `K`개 변형을 sampling하지만, 분석에서는 transformation distribution 전체에 대한 expectation으로 본다. Fig. 4에서 `K`가 약 `100`이면 성능이 포화하는 현상은 이 목적함수를 충분히 근사한다는 실험적 근거다. (p.3, p.5-6)

### Eq. 4-6: loss decomposition
표기:

```text
g(x): CNN penultimate-layer feature
W: final-layer weight matrix
h(x) = W g(x): softmax 이전 logit
f(x) = softmax(h(x))
g_bar_i = E_alpha[g(T_alpha x_i)]
```

softmax는 다음과 같다.

```text
softmax(z) = exp(z) / ||exp(z)||_1
```

저자들은 Eq. 3을 다음 두 부분으로 분해한다. (p.3)

```text
sum_i [-<e_i, W g_bar_i> + log ||exp(W g_bar_i)||_1]
+
sum_i [E_alpha[log ||exp(h(T_alpha x_i))||_1]
       - log ||exp(W g_bar_i)||_1]
```

- 첫 번째 합: 평균 transformed representation `g_bar_i`를 올바른 surrogate class로 분류하는 multinomial logistic regression 문제다. 즉 seed identity를 구별하는 `discrimination` 항이다.
- 두 번째 합: transformed sample의 logit이 평균 representation의 logit에서 크게 흩어지지 않게 하는 항이다. 즉 transformation에 대한 안정성을 유도하는 regularizer로 해석된다.

### Eq. 7: Jensen inequality 기반 non-negative regularizer
```text
E_alpha[log ||exp(h(T_alpha x_i))||_1]
- log ||exp(W g_bar_i)||_1 >= 0
```

`log-sum-exp`의 convexity와 Jensen inequality 때문에 두 번째 항은 음수가 될 수 없다. transformed representation이 invariant해지면 이 항은 최소값에 가까워진다. (p.3, Appendix A p.12)

엄밀한 보충: Appendix A의 Proposition 2에 따르면 equality 조건은 transformed logits의 차이가 `span(1)`에 속하는 경우다. softmax는 모든 logit에 같은 상수를 더해도 동일하므로, 이는 softmax prediction 관점의 invariance와 일치한다. (p.12)

## Implementation
### Classification networks
- small ablation network: `64c5-64c5-128f`
- larger network: `64c5-128c5-256c5-512f`
- largest network: `92c5-256c5-512c5-1024f`
- `NcF`: `F x F` filter를 `N`개 가진 convolutional layer
- `Nf`: unit `N`개인 fully connected layer
- 첫 두 convolutional layer 뒤 `2x2` max-pooling
- fully connected layer에 dropout
- Caffe 기반 학습 (p.4, Appendix B p.12)

### Training
- SGD momentum: `0.9`
- 초기 learning rate: `0.01`
- validation error 개선이 멈추면 learning rate를 `1/3`로 줄이고 수렴까지 반복
- Titan GPU 학습 시간: small network 약 `1.5`일, larger network 약 `4`일, largest network 약 `9`일 (Appendix B p.12)

### Test-time classification pipeline
- top softmax를 제외한 layer response를 convolutionally 계산
- STL-10과 CIFAR-10: 4-quadrant max-pooling
- Caltech-101과 Caltech-256: `1 + 4 + 16 = 21` cell spatial pyramid max-pooling
- pooled feature 위에 one-vs-all linear SVM 학습 (p.4)

### Matching-specific network
`Exemplar-CNN-blur`는 일반 분류용 네트워크를 그대로 쓰지 않는다.

- architecture: `64c7s2-128c5-256c5-512f`
- 첫 convolutional layer에 더 큰 filter와 stride `2` 사용
- STL보다 일반 자연 이미지 분포에 가까운 Flickr unlabeled image로 학습
- blur strength를 변화시키는 augmentation 추가
- feature map을 SIFT와 비교하기 위해 `4x4` spatial size로 max-pooling (p.8)

## Experiments: Classification
### Datasets
- surrogate training data: 주로 STL-10 unlabeled subset `100,000` images
- downstream evaluation: STL-10, CIFAR-10, Caltech-101, Caltech-256
- CIFAR-10, Caltech 평가는 STL unlabeled data에서 학습한 feature의 transfer 성능도 포함한다. (p.4)

### Main results: Table 1
가장 큰 `92c5-256c5-512c5-1024f` 모델은 다음 결과를 기록한다. (p.5)

| Dataset | Accuracy |
| --- | ---: |
| STL-10 | `74.2 +/- 0.4` |
| CIFAR-10(400) | `76.6 +/- 0.2` |
| CIFAR-10 | `84.3` |
| Caltech-101 | `87.1 +/- 0.7` |
| Caltech-256(30) | `53.6 +/- 0.2` |

저자들은 당시 비교한 unsupervised baseline보다 모든 dataset에서 높은 결과라고 보고한다. supervised state of the art와는 직접 비교 대상이 아니며, 분류에서는 supervised feature가 여전히 더 강한 dataset이 있다.

### Detailed findings
- surrogate class 수: small network는 약 `8000`에서 최적. 너무 많으면 유사 patch collision 증가. (Fig. 3, p.5)
- transformed sample 수: class당 약 `100`에서 성능 포화. (Fig. 4, p.6)
- transformation importance: translation, color, contrast가 rotation과 scaling보다 중요. Caltech-101에서는 정렬된 이미지 특성 때문에 color와 contrast가 더 중요. (Fig. 5, p.6)
- clustering: 비슷하거나 noisy한 cluster를 정리하면 STL 성능이 최대 `2.4%` 증가. largest network는 STL-10 `75.4 +/- 0.3`, CIFAR-10(400) `77.4 +/- 0.2`, Caltech-256 `53.7 +/- 0.6`. (Table 2, p.6)
- architecture: layer 수와 width를 늘리면 대체로 좋아지지만 단순히 깊게 쌓는다고 항상 개선되지는 않는다. (Table 4, p.8)

## Experiments: Descriptor Matching
### Why matching matters
분류 label은 recognition에는 도움이 되지만 interest-point matching에는 불필요하거나 방해가 될 수 있다. matching은 object class가 아니라 같은 local structure인지가 중요하기 때문이다. (p.8)

### Compared descriptors
- SIFT
- ImageNet 지도학습 AlexNet convolutional feature
- Exemplar-CNN-orig
- blur augmentation을 추가한 Exemplar-CNN-blur (p.8)

### Datasets and metric
- Mikolajczyk dataset: 실제 촬영 조건 변화가 포함된 `40` image pairs
- Flickr 기반 synthetic dataset: `16` base images에 `6`가지 transformation을 여러 강도로 적용한 `384` image pairs
- MSER region detector로 patch 추출
- descriptor Euclidean distance로 greedy matching
- target ellipse와 ground-truth ellipse의 IoU가 `0.5` 이상이면 true positive
- precision-recall curve의 area인 average precision(AP)을 metric으로 사용 (p.8-9)

### Main observation
일반 CNN feature는 blur에 취약하다. 하지만 blur augmentation을 추가한 Exemplar-CNN-blur는 blur 조건에서 훨씬 안정적이며, 대부분의 image pair에서 SIFT를 앞선다. 이 결과는 `어떤 augmentation을 사용했는가`가 모델이 학습할 robustness를 직접 결정한다는 논문의 가장 실용적인 증거다. (Fig. 9-11, p.10-11)

## Interpretation
### What is genuinely new
이 논문의 핵심은 단순히 augmentation을 사용했다는 것이 아니다. 의미 라벨이 없는 상태에서 seed patch identity를 surrogate label로 바꾸어 일반적인 CNN classification pipeline을 그대로 사용할 수 있게 만든 점이 중요하다.

```text
기존 reconstruction 중심 비지도 학습:
perturbed input -> representation -> input reconstruction

Exemplar-CNN:
seed patch identity + transformations -> surrogate classification
```

### Modern perspective
이 논문은 이후 instance discrimination 계열의 초기 형태로 읽을 수 있다. 같은 instance의 augmentation view를 묶고 다른 instance를 구별한다는 관점이 이미 드러난다. 다만 후대 contrastive learning처럼 explicit pairwise contrastive objective를 사용하는 것은 아니며, surrogate-class softmax classification을 사용한다.

### Augmentation is a task specification
augmentation은 단순한 dataset expansion이 아니다. 학습 표현이 무엇을 무시해야 하는지 정하는 task specification이다. blur matching을 원한다면 blur를 넣어야 하고, 색이 중요한 downstream task라면 color invariance를 무작정 강제하면 안 된다.

## Limitations
- surrogate class 수가 지나치게 많으면 유사 patch collision 때문에 학습 문제가 모순적으로 변한다. (p.5)
- transformation이 content identity를 바꾸지 않는다는 가정이 필요하다. 예를 들어 color invariance는 black panther와 puma 구분처럼 색이 중요한 task에 불리할 수 있다. (p.3-4)
- transformation list는 사람이 고른다. 학습되는 invariance는 이 선택에 제한된다.
- 분류에서는 지도학습 feature가 여전히 더 강할 수 있다.
- CNN descriptor는 blur에 자동으로 robust하지 않으며 matching task용 augmentation과 architecture 조정이 필요하다. (p.8-11)

## Open Questions
- seed patch collision을 clustering보다 더 일반적인 방식으로 줄일 수 있는가?
- downstream task별로 필요한 invariance와 보존해야 할 equivariance를 자동으로 선택할 수 있는가?
- surrogate-class softmax를 modern contrastive 또는 non-contrastive objective와 비교하면 어떤 정보가 유지되거나 사라지는가?
- blur처럼 예상 가능한 변형 외에 deployment 환경에서 중요한 nuisance를 어떻게 발견할 것인가?
- 여러 transformation policy로 학습한 feature를 결합하면 task-specific robustness를 더 안정적으로 선택할 수 있는가?

## Evidence Anchors
- p.1: 문제 정의, surrogate class 개요, classification 및 matching 주장
- p.2: Fig. 1-2, seed sampling, transformation family, Eq. 1
- p.3: Eq. 2-7, discriminative objective와 invariance regularizer 해석
- p.4-5: classification protocol, Table 1, Fig. 3
- p.6: Table 2, Fig. 4-5, transformation ablation
- p.7-8: Fig. 6-7, invariance 측정, Table 3-4, matching 동기
- p.8-9: Exemplar-CNN-blur, matching dataset, AP metric
- p.10-11: Fig. 8-11, SIFT, AlexNet, Exemplar-CNN 비교
- p.12: 결론, Appendix A log-sum-exp convexity와 Proposition 1-2
- p.13: Appendix C normalized Euclidean distance 기반 invariance 측정 상세

## Related WIKI Pages
- [Instance Discrimination](../concepts/instance-discrimination.md)
- [Transformation Invariance and Equivariance](../concepts/transformation-invariance-and-equivariance.md)
- [Self-Supervised Pretext Tasks](../concepts/self-supervised-pretext-tasks.md)
