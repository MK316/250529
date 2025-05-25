import streamlit as st

st.set_page_config(page_title="관계대명사 배우기", layout="centered")

st.title("📘 관계대명사 (Relative Pronouns)")

# --- 설명 ---
st.header("1. 관계대명사란?")
st.write("""
관계대명사는 **두 문장을 연결하여 더 자연스럽고 간결하게 표현**할 수 있게 도와주는 말이에요.  
주로 **사람, 사물, 장소** 등에 대해 **추가 설명**을 붙일 때 사용합니다.
""")

st.markdown("### 대표적인 관계대명사:")
st.markdown("""
- **who**: 사람을 설명할 때  
- **which**: 사물이나 동물을 설명할 때  
- **that**: 사람과 사물 모두 가능  
- **where**: 장소를 설명할 때  
""")

# --- 예문 ---
st.header("2. 예문 보기")

examples = {
    "This is the boy **who** won the prize.": "→ 이 소년은 상을 받은 소년이에요.",
    "I read the book **that** you gave me.": "→ 나는 네가 준 책을 읽었어.",
    "She lives in a house **which** has a red roof.": "→ 그녀는 빨간 지붕이 있는 집에 살아요.",
    "That is the place **where** we met.": "→ 저곳이 우리가 만난 장소예요."
}

for en, kr in examples.items():
    st.markdown(f"- {en}")
    st.caption(f"  {kr}")

# --- 간단 퀴즈 ---
st.header("3. 미니 퀴즈 🎯")
question = "Choose the correct relative pronoun: \n\nThis is the girl ___ sings well."
options = ["who", "which", "where", "when"]
answer = "who"

user_choice = st.radio("Fill in the blank:", options)

if st.button("Check Answer"):
    if user_choice == answer:
        st.success("정답입니다! 🎉")
    else:
        st.error("아쉬워요. 다시 생각해 보세요!")

# --- 마무리 ---
st.markdown("---")
st.info("관계대명사는 문장을 더 풍부하게 만들 수 있는 중요한 도구예요. 차근차근 연습해 보세요!")

