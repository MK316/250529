import streamlit as st
import pandas as pd
import random
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="관계대명사 배우기", layout="centered")
st.title("📘 관계대명사 배우기")

# --- 드롭다운 선택 ---
st.subheader("1. 학습할 관계대명사를 선택하세요:")
target = st.selectbox("관계대명사 선택", ["who", "which", "that", "where", "when"])

# --- 관계대명사별 설명 및 예문 ---
relative_pronouns = {
    "who": {
        "desc": "사람을 부가하여 설명할 때 사용합니다.",
        "A": "This is the boy.",
        "B": "The boy won the prize.",
        "C": "This is the boy **who won the prize**.",
        "K": "→ 이 소년은 상을 받은 소년이에요."
    },
    "which": {
        "desc": "사물이나 동물을 설명할 때 사용합니다.",
        "A": "She lives in a house.",
        "B": "The house has a red roof.",
        "C": "She lives in a house **which has a red roof**.",
        "K": "→ 그녀는 빨간 지붕이 있는 집에 살아요."
    },
    "that": {
        "desc": "사람과 사물 모두 대신할 수 있으며 who/which 대신에 자주 사용됩니다.",
        "A": "I read the book.",
        "B": "You gave me the book.",
        "C": "I read the book **that you gave me**.",
        "K": "→ 나는 네가 준 책을 읽었어."
    }
}
data = relative_pronouns[target]

st.markdown(f"### 🔹 관계대명사: **{target}**")
st.info(data["desc"])
st.markdown("**🔸 두 문장:**")
st.markdown(f"- A: {data['A']}")
st.markdown(f"- B: {data['B']}")
st.markdown("**🔸 결합된 문장:**")
st.success(f"{data['C']}")
st.caption(data["K"])

