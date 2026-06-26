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
from dashboard import inject_dashboard_css, render_dashboard, render_waiting_dashboard

st.set_page_config(page_title="안심콜 가드", page_icon="📞", layout="wide")
inject_dashboard_css()


@st.cache_resource
def load_predictor():
    return KoBERTMultiLabelPredictor("models/kobert_multilabel")


predictor = load_predictor()

if "history" not in st.session_state:
    st.session_state.history = []

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []


with st.sidebar:
    st.markdown("## 📞 안심콜 가드")
    st.caption("AI 보이스피싱 탐지 시스템")
    st.divider()

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
        st.success("연결됨")
        st.caption("멀티라벨 KoBERT 모델이 정상적으로 연결되었습니다.")
    else:
        st.warning("KoBERT 모델 없음: DB 기반으로 동작")
        if predictor.error:
            st.caption(predictor.error)

    st.divider()
    if st.button("↻ 통화 메모리 초기화", use_container_width=True, key="reset_memory_btn"):
        st.session_state.history = []
        st.session_state.conversation_memory = []
        st.rerun()


main_tab, text_tab, single_tab, db_tab, train_tab = st.tabs([
    "🎙️ 연속 통화 데모",
    "🧪 단계별 텍스트 데모",
    "📝 단일 텍스트 분석",
    "🗂️ 멀티라벨 DB",
    "🎓 학습 데이터",
])


with main_tab:
    run_recording = st.button(
        f"🎙️ {duration}초 듣고 누적 분석",
        type="primary",
        use_container_width=True,
        key="main_record_btn",
    )

    if run_recording:
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
        result = analyze_call_text(
            current_text=current_text,
            conversation_text=conversation_text,
            predictor=predictor,
        )
        st.session_state.history.append(result)
        st.rerun()

    if st.session_state.history:
        render_dashboard(st.session_state.history[-1])
    else:
        render_waiting_dashboard()


with text_tab:
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
            result = analyze_call_text(
                current_text=script,
                conversation_text=conversation_text,
                predictor=predictor,
            )
            st.session_state.history.append(result)
            st.rerun()

    if st.session_state.history:
        render_dashboard(st.session_state.history[-1])
    else:
        render_waiting_dashboard()


with single_tab:
    st.markdown("한 번의 텍스트를 분석합니다. 이 탭은 메모리를 사용하지 않는 단일 분석입니다.")
    default = "검찰입니다. 고객님 명의 계좌가 범죄에 연루되었습니다. 지금 바로 안전계좌로 300만 원을 이체하셔야 합니다."
    text = st.text_area("통화 내용 입력", default, height=160, key="single_text_input")

    if st.button("단일 분석 시작", type="primary", key="single_analyze_btn"):
        result = analyze_call_text(current_text=text, conversation_text=text, predictor=predictor)
        render_dashboard(result)


with db_tab:
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


with train_tab:
    st.markdown("멀티라벨 사례 DB를 KoBERT 학습용 표 형태로 변환한 결과입니다.")
    rows = export_training_rows()
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "학습용 CSV 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="kobert_multilabel_training.csv",
        mime="text/csv",
        key="download_training_csv_btn",
    )
