import streamlit as st
import pandas as pd
import random

# 데이터 로드 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data01.csv"
    df = pd.read_csv(url)
    return df  # ✅ 반드시 return!

df = load_data()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# ------------------------
# ✅ TAB 1: Level 1 퀴즈 앱
# ------------------------
with tab1:
    st.header("📝 Level 1 문장 퀴즈")

    # 문제 인덱스 초기화
    if "current_index" not in st.session_state:
        st.session_state.current_index = random.randint(0, len(df) - 1)
        st.session_state.show_feedback = False
        st.session_state.user_choice = None

    # 현재 행 가져오기
    row = df.iloc[st.session_state.current_index]

    sentence = row["Level_01"]
    correct_answer = row["Answer1"]  # "Correct" or "Incorrect"
    correction = row["Level_01_Correct"]
    meaning = row["Level_01_Meaning"]

    st.markdown("**문장을 보고 맞는 문장인지 판단하세요:**")
    st.markdown(f"### \"{sentence}\"")

    # 사용자 선택
    user_choice = st.radio("이 문장은 문법적으로 맞나요?", ["Correct", "Incorrect"], key=f"choice_{st.session_state.current_index}")

    # 정답 확인 버튼
    if st.button("✅ 정답 확인"):
        st.session_state.show_feedback = True
        st.session_state.user_choice = user_choice

    # 피드백 표시
    if st.session_state.show_feedback:
        if st.session_state.user_choice == correct_answer:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸어요.")
            st.markdown("**👉 올바른 문장:**")
            st.info(correction)

        st.markdown("**📘 해석:**")
        st.caption(meaning)

        # 다음 문제 버튼
        if st.button("➡️ 다음 문제"):
            st.session_state.current_index = random.randint(0, len(df) - 1)
            st.session_state.show_feedback = False
            st.rerun()
