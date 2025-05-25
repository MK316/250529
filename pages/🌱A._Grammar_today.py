import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="관계대명사 배우기", layout="centered")
st.markdown("## 📘 관계대명사 배우기")

# --- 드롭다운 선택 ---
target = st.selectbox("✨ 학습할 관계대명사를 선택하세요:", ["who", "which", "that"])

# --- 관계대명사별 설명 및 예문 + 이미지 링크 포함 ---
relative_pronouns = {
    "who": {
        "desc": "사람을 부가하여 설명할 때 사용합니다.",
        "A": "This is a boy.",
        "B": "The boy won the prize.",
        "C": "This is the boy **who won the prize**.",
        "K": "→ 이 소년이 상을 받은 그 소년이에요.",
        "imgA": "https://github.com/MK316/250529/raw/main/images/who-01.jpg",
        "imgB": "https://github.com/MK316/250529/raw/main/images/who-02.jpg",
        "imgC": "https://github.com/MK316/250529/raw/main/images/who-03.jpg"
    },
    "which": {
        "desc": "사물이나 동물을 설명할 때 사용합니다.",
        "A": "She lives in a house.",
        "B": "The house has a red roof.",
        "C": "She lives in a house **which has a red roof**.",
        "K": "→ 그녀는 빨간 지붕이 있는 집에 살아요.",
        "imgA": "https://github.com/MK316/250529/raw/main/images/which-01.jpg",
        "imgB": "https://github.com/MK316/250529/raw/main/images/which-02.jpg",
        "imgC": "https://github.com/MK316/250529/raw/main/images/which-03.jpg"
    },
    "that": {
        "desc": "사람과 사물 모두 대신할 수 있으며 who/which 대신에 자주 사용됩니다.",
        "A": "I read a book.",
        "B": "You gave me the book.",
        "C": "I read the book **that you gave me**.",
        "K": "→ 나는 네가 나에게 준 그 책을 읽었어.",
        "imgA": "https://github.com/MK316/250529/raw/main/images/that-01.jpg",
        "imgB": "https://github.com/MK316/250529/raw/main/images/that-02.jpg",
        "imgC": "https://github.com/MK316/250529/raw/main/images/that-03.jpg"
    }
}

data = relative_pronouns[target]

# --- Display Explanation and Sentences ---
st.markdown(f"### 🔹 관계대명사: **{target}**")
st.info(data["desc"])

st.markdown("**🔸 두 문장 + 결합된 문장:**")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**A:** {data['A']}")
    st.image(data["imgA"], caption="A", width=150)

with col2:
    st.markdown(f"**B:** {data['B']}")
    st.image(data["imgB"], caption="B", width=150)

with col3:
    # st.caption(data["K"])
    st.image(data["imgC"], caption="A+B", width=150)

# st.markdown("**🔸 결합된 문장:**")
st.success(f"🔸 결합된 문장: {data['C']}")
st.caption(data["K"])
st.image(data["imgC"], caption="Combined", width=250)
