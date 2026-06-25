# 📞 AnsimCall Guard — Conversation Memory MVP

AI 기반 실시간 보이스피싱 대응 코파일럿입니다.

이 버전은 통화가 한 번에 끝나지 않는다는 점을 반영하여, 10초 단위로 인식된 통화 내용을 계속 누적하고, 누적된 대화 전체를 기반으로 위험도와 대응 문구를 갱신합니다.

## 핵심 기능

- 10~30초 단위 음성 녹음
- Faster-Whisper STT
- STT 보정
- Conversation Memory
- 멀티라벨 보이스피싱 사례 DB
- KoBERT 멀티라벨 연결 구조
- 유사 사례 Top 3 검색
- 누적 위험도 계산
- 대응 문구 추천

## 위험도 계산 방식

```text
최종 위험도
= 현재 구간 위험도 × 0.4
+ 누적 대화 위험도 × 0.4
+ DB 유사 사례 점수 × 0.2
```

## 실행 방법

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 발표용 핵심 설명

AnsimCall Guard는 통화 내용을 10초 단위로 분석하는 데서 끝나지 않고, Conversation Memory에 계속 저장합니다. 이후 현재 구간, 누적 대화, 유사 보이스피싱 사례 점수를 함께 계산해 통화가 진행될수록 위험도를 갱신하고 대응 문구를 추천합니다.
