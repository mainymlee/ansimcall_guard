import html
import textwrap
import streamlit as st


def inject_dashboard_css():
    st.markdown(textwrap.dedent("""
    <style>
    .block-container {
        padding-top: 2.6rem !important;
        padding-bottom: 3rem !important;
        max-width: 1180px !important;
    }

    [data-testid="stSidebar"] {
        background: #f1f5f9;
        border-right: 1px solid #e5e7eb;
    }

    h1, h2, h3, p {
        margin-top: 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #e5e7eb;
        padding-top: 8px;
        margin-bottom: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 18px;
        border-radius: 14px 14px 0 0;
        font-weight: 800;
    }

    div.stButton > button {
        border-radius: 18px;
        font-weight: 900;
        min-height: 54px;
    }

    div.stButton > button[kind="primary"] {
        background: #2563eb;
        border: 1px solid #2563eb;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.22);
    }

    .ag-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }

    .ag-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .ag-logo {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 27px;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25);
    }

    .ag-title {
        font-size: 22px;
        font-weight: 950;
        color: #0f172a;
        line-height: 1.15;
    }

    .ag-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-top: 4px;
    }

    .ag-status {
        padding: 9px 18px;
        border: 1px solid #e5e7eb;
        background: white;
        border-radius: 999px;
        font-weight: 850;
        color: #334155;
    }

    .ag-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.06);
        margin-bottom: 18px;
    }

    .ag-risk-card {
        background: #fff1f2;
        border: 1px solid #fca5a5;
        border-radius: 22px;
        padding: 30px 28px;
        text-align: center;
        margin-bottom: 18px;
    }

    .ag-risk-level {
        color: #dc2626;
        font-size: 26px;
        font-weight: 950;
    }

    .ag-risk-score {
        color: #dc2626;
        font-size: 64px;
        line-height: 1.05;
        font-weight: 950;
        letter-spacing: -2px;
        margin: 8px 0;
    }

    .ag-risk-desc {
        color: #dc2626;
        font-size: 18px;
        font-weight: 850;
        margin-bottom: 20px;
    }

    .ag-progress-bg {
        width: 92%;
        height: 16px;
        background: #ead7d7;
        border-radius: 999px;
        overflow: hidden;
        margin: 0 auto;
    }

    .ag-progress-fill {
        height: 100%;
        background: #dc2626;
        border-radius: 999px;
    }

    .ag-section-title {
        font-size: 20px;
        font-weight: 950;
        color: #0f172a;
        margin-bottom: 16px;
    }

    .ag-section-label {
        color: #334155;
        font-size: 15px;
        font-weight: 950;
        margin: 20px 0 10px 0;
    }

    .ag-recommend {
        border-left: 4px solid #2563eb;
        padding: 12px 0 12px 18px;
        color: #0f172a;
        font-size: 21px;
        line-height: 1.65;
        font-weight: 900;
        white-space: pre-wrap;
    }

    .ag-memory-box {
        background: #f8fafc;
        border: 1px solid #eef2f7;
        border-radius: 18px;
        padding: 22px;
        color: #0f172a;
        line-height: 1.8;
        font-size: 16px;
        min-height: 96px;
        white-space: pre-wrap;
    }

    .ag-badge-red {
        display: inline-block;
        background: #fee2e2;
        color: #b91c1c;
        border-radius: 999px;
        padding: 8px 14px;
        margin: 5px 6px 5px 0;
        font-weight: 900;
        font-size: 14px;
    }

    .ag-badge-blue {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 8px 14px;
        margin: 5px 6px 5px 0;
        font-weight: 900;
        font-size: 14px;
    }

    .ag-case-row {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: center;
        background: #f8fafc;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        color: #0f172a;
    }

    .ag-case-title {
        font-weight: 850;
    }

    .ag-case-score {
        color: #64748b;
        white-space: nowrap;
        font-weight: 750;
    }

    .ag-muted {
        color: #64748b;
        font-size: 14px;
    }

    .ag-report-btn {
        width: 100%;
        background: #dc2626;
        color: #ffffff;
        border-radius: 18px;
        padding: 19px 18px;
        text-align: center;
        font-size: 18px;
        font-weight: 950;
        box-shadow: 0 14px 28px rgba(220, 38, 38, 0.25);
        margin-bottom: 14px;
    }

    .ag-empty-listen-card {
        height: 270px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
    }

    .ag-ear {
        font-size: 48px;
        margin-bottom: 28px;
    }

    .ag-empty-title {
        font-size: 22px;
        font-weight: 950;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .ag-empty-sub {
        color: #64748b;
        font-size: 15px;
    }
    </style>
    """), unsafe_allow_html=True)


def _md(markup: str):
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


def _safe(value):
    return html.escape(str(value)) if value is not None else ""


def _risk_meta(score):
    try:
        score = int(float(score))
    except Exception:
        score = 0

    if score >= 70:
        return "위험", "보이스피싱이 의심됩니다.", "위험 감지"
    if score >= 40:
        return "주의", "주의가 필요한 통화입니다.", "주의"
    return "안전", "현재까지 큰 위험은 없습니다.", "대기 중"


def _keyword_list(result):
    keywords = (
        result.get("detected_keywords")
        or result.get("keywords")
        or result.get("matched_keywords")
        or []
    )

    if not keywords:
        for case in result.get("similar_cases", [])[:2]:
            for keyword in case.get("keywords", []):
                keywords.append(keyword)

    seen = set()
    cleaned = []
    for keyword in keywords:
        keyword = str(keyword).strip()
        if keyword and keyword not in seen:
            seen.add(keyword)
            cleaned.append(keyword)

    return cleaned[:8]


def _open_card():
    _md('<div class="ag-card">')


def _close_div():
    _md('</div>')


def _section_label(text):
    _md(f'<div class="ag-section-label">{_safe(text)}</div>')


def _badges(items, color):
    if not items:
        _md('<div class="ag-muted">없음</div>')
        return

    klass = "ag-badge-red" if color == "red" else "ag-badge-blue"
    html_badges = "".join(
        f'<span class="{klass}">{_safe(item)}</span>' for item in items[:8]
    )
    _md(html_badges)


def _memory_box(text):
    _md(f'<div class="ag-memory-box">{_safe(text)}</div>')


def _case_rows(cases):
    if not cases:
        _md('<div class="ag-muted">유사 사례 없음</div>')
        return

    rows = []
    for case in cases[:3]:
        title = _safe(case.get("title", "유사 사례"))
        sim = _safe(case.get("similarity", "-"))
        rows.append(
            f'<div class="ag-case-row">'
            f'<span class="ag-case-title">{title}</span>'
            f'<span class="ag-case-score">유사도 {sim}%</span>'
            f'</div>'
        )
    _md("".join(rows))


def render_waiting_dashboard():
    left, right = st.columns([1, 1.55], gap="large")

    with left:
        _md("""
        <div class="ag-header-row">
            <div class="ag-brand">
                <div class="ag-logo">📞</div>
                <div>
                    <div class="ag-title">안심콜 가드</div>
                    <div class="ag-subtitle">AI 보이스피싱 탐지 시스템</div>
                </div>
            </div>
            <div class="ag-status">대기 중</div>
        </div>

        <div class="ag-card ag-empty-listen-card">
            <div class="ag-ear">👂</div>
            <div class="ag-empty-title">통화를 듣고 있습니다</div>
            <div class="ag-empty-sub">위험한 말이 들리면 바로 알려드려요</div>
        </div>
        """)

    with right:
        _md("""
        <div class="ag-card">
            <div class="ag-section-title">💬 지금까지 누적된 통화 내용</div>
            <div class="ag-memory-box">아직 누적된 통화 내용이 없습니다.</div>
        </div>
        """)


def render_dashboard(result):
    score = result.get("risk_score", 0)
    try:
        score_int = int(float(score))
    except Exception:
        score_int = 0

    risk_text, risk_desc, status_text = _risk_meta(score_int)

    conversation_text = result.get("conversation_text", "") or "아직 누적된 통화 내용이 없습니다."
    current_text = result.get("current_text", "") or "방금 인식된 문장이 없습니다."

    recommendations = result.get("recommendations", [])
    if recommendations:
        first_rec = recommendations[0].get("say", "")
    else:
        first_rec = "전화로는 송금하지 않겠습니다. 공식 번호로 다시 확인하겠습니다."

    labels = result.get("final_labels", []) or []
    similar_cases = result.get("similar_cases", []) or []
    keywords = _keyword_list(result)

    left, right = st.columns([1, 1.55], gap="large")

    with left:
        _md(f"""
        <div class="ag-header-row">
            <div class="ag-brand">
                <div class="ag-logo">📞</div>
                <div>
                    <div class="ag-title">안심콜 가드</div>
                    <div class="ag-subtitle">AI 보이스피싱 탐지 시스템</div>
                </div>
            </div>
            <div class="ag-status">{_safe(status_text)}</div>
        </div>

        <div class="ag-risk-card">
            <div class="ag-risk-level">⚠️ {risk_text}</div>
            <div class="ag-risk-score">{score_int}점</div>
            <div class="ag-risk-desc">{risk_desc}</div>
            <div class="ag-progress-bg">
                <div class="ag-progress-fill" style="width:{max(0, min(score_int, 100))}%;"></div>
            </div>
        </div>

        <div class="ag-card">
            <div class="ag-section-title">💬 이렇게 말해보세요</div>
            <div class="ag-recommend">"{_safe(first_rec)}"</div>
        </div>

        <div class="ag-report-btn">🚫 전화 끊고 신고하기</div>
        """)

        with st.expander("› 자세히 보기"):
            st.write("**점수 구성**")
            st.write(f"- 현재 구간 점수: {result.get('current_score', 0)}점")
            st.write(f"- 누적 대화 점수: {result.get('memory_score', 0)}점")
            st.write(f"- DB 유사 사례 점수: {result.get('db_similarity_score', 0)}점")

    with right:
        _md('<div class="ag-card">')
        _md('<div class="ag-section-title">💬 지금까지 누적된 통화 내용</div>')
        _memory_box(conversation_text)
        _close_div()

        _md('<div class="ag-card">')

        _section_label("의심되는 말")
        if keywords:
            _badges(keywords, "red")
        else:
            _md('<div class="ag-muted">의심 키워드 없음</div>')

        _section_label("탐지된 유형")
        _badges(labels, "blue")

        _section_label("비슷한 사례")
        _case_rows(similar_cases)

        _section_label("방금 들은 말")
        _memory_box(current_text)

        _close_div()
