import streamlit as st

st.set_page_config(page_title="관계대명사 배우기", layout="centered")

st.title("📘 관계대명사 (Relative Pronouns)")

# --- 1. 개념 설명 ---
st.subheader("1. 관계대명사란?")
st.write("""
관계대명사는 **두 문장을 연결하여 더 자연스럽고 간결하게 표현**할 수 있게 도와주는 말이에요.  
주로 **사람, 사물, 장소**에 대해 **추가 설명**을 붙일 때 사용합니다.
""")

st.markdown("#### 🔑 대표적인 관계대명사")
st.markdown("""
- **who**: 사람을 설명할 때  
- **which**: 사물이나 동물  
- **that**: 사람과 사물 모두  
- **where**: 장소를 설명할 때
""")

st.markdown("---")

# --- 2. 예문 보기 ---
st.subheader("2. 예문 보기 (도식으로 이해하기)")

examples = [
    {
        "type": "who",
        "A": "This is the boy.",
        "B": "The boy won the prize.",
        "C": "This is the boy **who won the prize**.",
        "K": "→ 이 소년은 상을 받은 소년이에요."
    },
    {
        "type": "that",
        "A": "I read the book.",
        "B": "You gave me the book.",
        "C": "I read the book **that you gave me**.",
        "K": "→ 나는 네가 준 책을 읽었어."
    },
    {
        "type": "which",
        "A": "She lives in a house.",
        "B": "The house has a red roof.",
        "C": "She lives in a house **which has a red roof**.",
        "K": "→ 그녀는 빨간 지붕이 있는 집에 살아요."
    },
    {
        "type": "where",
        "A": "That is the place.",
        "B": "We met at the place.",
        "C": "That is the place **where we met**.",
        "K": "→ 저곳이 우리가 만난 장소예요."
    }
]

for ex in examples:
    st.markdown(f"##### 🔹 관계대명사: **{ex['type']}**")
    st.code(f"{ex['A']}  +  {ex['B']}  ➡️  {ex['C']}")
    st.caption(ex['K'])
    st.markdown("---")

# --- 3. 미니 퀴즈 ---
st.subheader("3. 미니 퀴즈 🎯")

st.markdown("**Fill in the blank below:**")
st.markdown("### ✏️ This is the girl ___ sings well.")

options = ["who", "which", "where", "when"]
answer = "who"

user_choice = st.radio("Choose the correct relative pronoun:", options)

if st.button("Check Answer"):
    if user_choice == answer:
        st.success("✅ 정답입니다! 'who'는 사람을 주어로 설명할 때 사용해요.")
    else:
        st.error("❌ 아쉬워요. 정답은 'who'입니다. 사람을 주어로 받을 때 사용해요.")

# --- 마무리 ---
st.markdown("---")
st.info("관계대명사는 문장을 풍부하게 만들어주는 중요한 도구예요. 자주 연습하며 익숙해지세요!")
