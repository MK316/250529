import streamlit as st
import pandas as pd
import random

# -------------------------
# 1. 데이터 로드 함수
# -------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data01.csv"
    df = pd.read_csv(url)
    
    # 핵심 열에 NaN이 있는 행은 제거
    df = df.dropna(subset=["Level_01", "Answer1", "Level_01_Correct", "Level_01_Meaning"])
    return df

df = load_data()

# -------------------------
# 2. 기본 예외 처리
# -------------------------
if df.empty:
    st.error("❌ 사용할 수 있는 데이터가 없습니다. CSV 파일을 확인하세요.")
    st.stop()

# -------------------------
# 3. 탭 구성
# -------------------------
tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# -------------------------
# ✅ TAB 1: Level 1 퀴즈 앱
# -------------------------
with tab1:
    st.header("📝 Level 1 문장 퀴즈")

    # 초기 세션 상태 설정
    if "current_index" not in st.session_state:
        st.session_state.current_index = random.randint(0, len(df) - 1)
        st.session_state.show_feedback = False
        st.session_state.user_choice = None

    # 현재 row 가져오기 (안전하게)
    try:
        row = df.iloc[st.session_state.current_index]
    except IndexError:
        st.error("❌ 인덱스 오류가 발생했습니다. 다시 시도해 주세요.")
        st.stop()

    # 문제 문항 정보
    sentence = row["Level_01"]
    correct_answer = row["Answer1"]  # "Correct" 또는 "Incorrect"
    correction = row["Level_01_Correct"]
    meaning = row["Level_01_Meaning"]

    # 문장 출력
    st.markdown("**문장을 보고 맞는 문장인지 판단하세요:**")
    st.markdown(f"### \"{sentence}\"")

    # 사용자 선택
    user_choice = st.radio(
        "이 문장은 문법적으로 맞나요?",
        ["Correct", "Incorrect"],
        key=f"choice_{st.session_state.current_index}"
    )

    # 정답 확인
    if st.button("✅ 정답 확인"):
        st.session_state.user_choice = user_choice
        st.session_state.show_feedback = True

    # 피드백 표시
    if st.session_state.show_feedback:
        if st.session_state.user_choice == correct_answer:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸어요.")
            st.markdown("**👉 올바른 문장:**")
            st.info(correction if pd.notna(correction) else "정보 없음")

        st.markdown("**📘 해석:**")
        st.caption(meaning if pd.notna(meaning) else "해석이 제공되지 않았습니다.")

        # 다음 문제로 이동
        if st.button("➡️ 다음 문제"):
            st.session_state.current_index = random.randint(0, len(df) - 1)
            st.session_state.show_feedback = False
            st.rerun()
