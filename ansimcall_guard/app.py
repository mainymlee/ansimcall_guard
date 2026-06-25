from pathlib import Path
from datetime import datetime
import tempfile
import pandas as pd
import streamlit as st

from modules.audio_recorder import list_input_devices, record_audio
from modules.stt_engine import transcribe_audio
from modules.analysis_engine import analyze_call_text
from modules.kobert_multilabel import KoBERTMultiLabelPredictor
from modules.case_db import export_training_rows, load_cases

st.set_page_config(page_title="안심콜 가드 Memory MVP", page_icon="📞", layout="wide")

@st.cache_resource
def load_predictor():
    return KoBERTMultiLabelPredictor("models/kobert_multilabel")

predictor = load_predictor()

if "history" not in st.session_state:
    st.session_state.history = []

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []

st.title("📞 안심콜 가드 — Conversation Memory MVP")
st.caption("통화 내용을 10초 단위로 누적하면서 위험도와 대응 문구를 계속 갱신합니다.")

with st.sidebar:
    st.header("설정")
    duration = st.slider("녹음 시간", 10, 30, 10)
    model_size = st.selectbox("Whisper 모델", ["tiny", "base", "small"], index=2)

    devices = list_input_devices()
    labels = ["기본 마이크"] + [f"{d['id']} - {d['name']}" for d in devices]
    chosen = st.selectbox("입력 장치", labels)
    device = None if chosen == "기본 마이크" else int(chosen.split(" - ")[0])

    st.divider()
    st.subheader("KoBERT 상태")
    if predictor.available:
        st.success("멀티라벨 KoBERT 연결됨")
    else:
        st.warning("KoBERT 모델 없음: DB 기반으로 동작")
        if predictor.error:
            st.caption(predictor.error)

    st.divider()
    if st.button("통화 메모리 초기화"):
        st.session_state.history = []
        st.session_state.conversation_memory = []
        st.rerun()

def render_result(result):
    c1, c2 = st.columns([1, 2])

    with c1:
        level = result["risk_level"]
        if level == "위험":
            st.error(f"🚨 {level}")
        elif level == "경고":
            st.warning(f"⚠️ {level}")
        elif level == "주의":
            st.info(f"🔎 {level}")
        else:
            st.success(f"✅ {level}")

        st.metric("최종 누적 위험도", f"{result['risk_score']}점")
        st.caption("현재 구간 + 누적 대화 + 유사 사례를 함께 반영합니다.")

        st.write("**점수 구성**")
        st.write(f"- 현재 구간 점수: {result['current_score']}점")
        st.write(f"- 누적 대화 점수: {result['memory_score']}점")
        st.write(f"- DB 유사 사례 점수: {result['db_similarity_score']}점")

        st.write("**최종 탐지 라벨**")
        if result["final_labels"]:
            for label in result["final_labels"]:
                st.write(f"- {label}")
        else:
            st.write("- 없음")

    with c2:
        st.markdown("### 👂 방금 들은 말")
        st.write(result["current_text"] or "(인식된 문장 없음)")

        st.markdown("### 🧠 지금까지 누적된 통화 내용")
        st.text_area("Conversation Memory", result["conversation_text"], height=180, disabled=True, label_visibility="collapsed")

        if result["fuzzy_terms"]:
            st.markdown("### 🔧 STT 보정 키워드")
            st.write(", ".join(result["fuzzy_terms"]))

        st.markdown("### 💬 지금 이렇게 말해보세요")
        for i, rec in enumerate(result["recommendations"], 1):
            st.success(f"{i}. {rec['say']}")
            st.caption(f"출처: {rec['source']} · 이유: {rec['why']}")

    st.markdown("---")
    st.markdown("## 📌 유사 사례 Top 3")
    for case in result["similar_cases"]:
        with st.expander(f"{case['title']} / 유사도 {case['similarity']}%"):
            st.write(f"**사례 요약:** {case['case_summary']}")
            st.write(f"**위험 이유:** {case['warning_reason']}")
            st.write(f"**라벨:** {', '.join(case['multi_labels'])}")
            st.write("**대응 문구:**")
            for r in case["recommended_response"]:
                st.write(f"- {r}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎙️ 연속 통화 데모", "🧪 단계별 텍스트 데모", "📝 단일 텍스트 분석", "🗂️ 멀티라벨 DB", "🎓 학습 데이터"])

with tab1:
    st.markdown("TTS 또는 직접 말하기로 상대방 대사를 재생하고, 10초 단위로 계속 누적 분석합니다.")

    if st.button(f"🎙️ {duration}초 듣고 누적 분석", type="primary"):
        wav_path = Path(tempfile.gettempdir()) / f"ansimcall_{datetime.now().strftime('%H%M%S')}.wav"

        with st.spinner(f"{duration}초 동안 녹음 중입니다..."):
            try:
                record_audio(str(wav_path), duration=duration, samplerate=16000, device=device)
            except Exception as e:
                st.error(f"녹음 오류: {e}")
                st.stop()

        st.audio(str(wav_path))

        with st.spinner("Whisper STT 변환 중입니다..."):
            try:
                current_text = transcribe_audio(str(wav_path), model_size=model_size)
            except Exception as e:
                st.error(f"STT 오류: {e}")
                st.stop()

        if current_text:
            st.session_state.conversation_memory.append(current_text)

        conversation_text = "\n".join(st.session_state.conversation_memory[-10:])
        result = analyze_call_text(current_text=current_text, conversation_text=conversation_text, predictor=predictor)
        st.session_state.history.append(result)
        render_result(result)

    st.markdown("## 🧾 누적 대화 기록")
    if st.session_state.conversation_memory:
        for i, chunk in enumerate(st.session_state.conversation_memory, 1):
            st.write(f"**{i}.** {chunk}")
    else:
        st.write("아직 누적된 대화가 없습니다.")

with tab2:
    st.markdown("발표 데모용입니다. 아래 대사를 하나씩 누르면 통화가 이어지는 것처럼 누적 분석됩니다.")
    demo_steps = [
        "안녕하세요. 서울중앙지검 수사관입니다.",
        "고객님 명의 계좌가 범죄에 연루되었습니다.",
        "지금 바로 안전계좌로 300만 원을 이체하셔야 합니다.",
        "다른 사람에게 알리면 수사에 불이익이 생길 수 있습니다. 전화 끊지 마세요.",
    ]

    for idx, script in enumerate(demo_steps, 1):
        if st.button(f"{idx}단계 추가: {script}", key=f"step_{idx}"):
            st.session_state.conversation_memory.append(script)
            conversation_text = "\n".join(st.session_state.conversation_memory[-10:])
            result = analyze_call_text(current_text=script, conversation_text=conversation_text, predictor=predictor)
            st.session_state.history.append(result)
            render_result(result)

    st.markdown("### 현재 누적 통화")
    st.text_area("memory", "\n".join(st.session_state.conversation_memory), height=160, disabled=True, label_visibility="collapsed")

with tab3:
    st.markdown("한 번의 텍스트를 분석합니다. 이 탭은 메모리를 사용하지 않는 단일 분석입니다.")
    default = "검찰입니다. 고객님 명의 계좌가 범죄에 연루되었습니다. 지금 바로 안전계좌로 300만 원을 이체하셔야 합니다."
    text = st.text_area("통화 내용 입력", default, height=160)

    if st.button("단일 분석 시작", type="primary"):
        result = analyze_call_text(text, conversation_text=text, predictor=predictor)
        render_result(result)

with tab4:
    st.markdown("하나의 DB가 KoBERT 학습, 유사 사례 검색, 위험도 계산, 대응 문구 추천에 모두 사용됩니다.")
    cases = load_cases()
    rows = []
    for c in cases:
        rows.append({
            "case_id": c["case_id"],
            "title": c["title"],
            "is_phishing": c["is_phishing"],
            "multi_labels": ", ".join(c["multi_labels"]),
            "risk_score": c["risk_score"],
            "keywords": ", ".join(c["keywords"]),
            "warning_reason": c["warning_reason"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with st.expander("원본 JSON 보기"):
        st.json(cases)

with tab5:
    st.markdown("멀티라벨 사례 DB를 KoBERT 학습용 표 형태로 변환한 결과입니다.")
    rows = export_training_rows()
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.download_button("학습용 CSV 다운로드", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="kobert_multilabel_training.csv", mime="text/csv")
