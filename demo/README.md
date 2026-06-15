# Demo: 실사용 렌더링 화면

![Research WIKI dashboard](./demo.png)

`demo.png`는 이 도구로 실제 운영 중인 지식베이스(컴퓨터 비전 자기지도학습 논문 7편)를 GUI에서 렌더링한 화면입니다. 내용 텍스트를 공유하지 않고도 도구가 실제로 동작함을 보여줍니다.

화면에서 확인할 수 있는 것:

- **논문 반영 상태**: 빨강 = 아직 WIKI에 반영 안 된 논문(SimCLR), 파랑 = `source`+`concept` 반영 완료 + `비교 분석 완료` 배지
- **요약 카드**: 로컬 PDF 7건, 반영 완료 6건, WIKI 페이지 19건, 검토 대기 초안 수
- **WIKI 페이지 유형별 카운트**: source 6 / concept 8 / comparison 1 / claim 1 / question 1 / system 2
- **작업 패널**: WIKI 편집 폼과 PDF 읽기 설정

화면을 직접 재생성하려면 GUI 실행 후 다음을 실행합니다:

```powershell
python scripts\capture_gui.py demo
```
