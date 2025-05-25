import streamlit as st
import pandas as pd
import random

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data01.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=["Level_01", "Answer1", "Level_01_Correct", "Level_01_Meaning"])  # ✅ 핵심 열이 NaN인 행 제거
    return df

df = load_data()

tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

with tab1:
    st.header("📝 Level 1 문장 퀴즈")

    if "current_index" not in st.session_state:
        st.session_state.current_index = random.randint(0, len(df) - 1)
        st.session_state.show_feedback = False
        st.session_state.user_choice = None

    row = df.iloc[st.session_state.current_index]

    sentence = row["Level_01"]
    correct_answer = row["Answer1"]
    correction = row["Level_01_Correct"]
    meaning = row["Level_01_Meaning"]

    st.markdown("**문장을 보고 맞는 문장인지 판단하세요:**")
    st.markdown(f"### \"{sentence}\"")

    user_choice = st.radio("이 문장은 문법적으로 맞나요?", ["Correct", "Incorrect"], key=f"choice_{st.session_state.current_index}")

    if st.button("✅ 정답 확인"):
        st.session_state.show_feedback = True
        st.session_state.user_choice = user_choice

    if st.session_state.show_feedback:
        if st.session_state.user_choice == correct_answer:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸어요.")
            st.markdown("**👉 올바른 문장:**")
            st.info(correction if pd.notna(correction) else "정보 없음")

        st.markdown("**📘 해석:**")
        st.caption(meaning if pd.notna(meaning) else "해석이 제공되지 않았습니다.")

        if st.button("➡️ 다음 문제"):
            st.session_state.current_index = random.randint(0, len(df) - 1)
            st.session_state.show_feedback = False
            st.rerun()
