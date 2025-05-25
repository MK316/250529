import streamlit as st
import pandas as pd
import random

# Load CSV data
@st.cache_data
def load_data():
    # 로컬 또는 GitHub 경로로 교체 가능
    url="https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data01.csv"
    df = pd.read_csv(url)  # 실제 파일 경로로 수정
    return df

df = load_data()

# 탭 구조 만들기
tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# ------------------------
# ✅ TAB 1: Level 1 퀴즈 앱
# ------------------------
with tab1:
    st.header("📝 Level 1 문장 퀴즈")

    # 무작위로 하나의 행 선택
    random_row = df.sample(1).iloc[0]

    sentence = random_row["Level_01"]
    correct_answer = random_row["Answer1"]  # "Correct" or "Incorrect"
    correction = random_row["Level_01_Correct"]
    meaning = random_row["Level_01_Meaning"]

    # 문제 표시
    st.markdown(f"**문장을 보고 맞는 문장인지 판단하세요:**")
    st.markdown(f"### \"{sentence}\"")

    user_choice = st.radio("이 문장은 문법적으로 맞나요?", ["Correct", "Incorrect"])

    if st.button("정답 확인"):
        if user_choice == correct_answer:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸어요.")
            st.markdown("**👉 올바른 문장:**")
            st.info(correction)

        st.markdown("**📘 해석:**")
        st.caption(meaning)
