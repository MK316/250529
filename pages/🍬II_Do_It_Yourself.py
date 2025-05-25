import streamlit as st
import pandas as pd
import random
import re
import streamlit.components.v1 as components


# ---------------------
# 🧠 퀴즈 앱 통합 (Level 1~3)
# ---------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data03.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=[
        "Level_01", "Answer1", "Level_01_Correct", "Level_01_Meaning",
        "Level_02", "Level_02_Focus", "Level_02_Meaning",
        "Level_03", "Level_03_Meaning"
    ])
    return df.reset_index(drop=True)

df = load_data()

# 탭 구성
level1, level2, level3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# -------------------------------
# ✅ Level 1: 문장 정답 판단
# -------------------------------
with level1:
    st.subheader("✅ 문장이 맞는지 판단하기")
    if "tab1_index" not in st.session_state:
        st.session_state.tab1_index = 0
        st.session_state.tab1_score = 0

    row = df.iloc[st.session_state.tab1_index]
    st.markdown(f"**문장:** {row['Level_01']}")
    st.caption(row['Level_01_Meaning'])
    choice = st.radio("문장이 맞나요?", ["Correct", "Incorrect"])

    if st.button("정답 확인", key="check1"):
        if choice == row['Answer1']:
            st.success("정답입니다!")
            st.session_state.tab1_score += 1
        else:
            st.error("틀렸습니다.")
            st.info(f"👉 올바른 문장: {row['Level_01_Correct']}")

    if st.button("다음 문장", key="next1"):
        st.session_state.tab1_index = (st.session_state.tab1_index + 1) % len(df)
        st.rerun()

# -------------------------------
# ✏️ Level 2: 관계대명사 빈칸 채우기
# -------------------------------
with level2:
    st.subheader("✏️ 관계대명사 빈칸 채우기")

    def make_cloze(sentence, focus):
        parts = [p.strip() for p in focus.split(",")] if "," in focus else [focus.strip()]
        for p in parts:
            sentence = re.sub(rf"\b{re.escape(p)}\b", "<u>_____</u>", sentence, 1)
        return sentence

    def generate_options(correct):
        base = ['that', 'which', 'who', 'where']
        if "," in correct:
            correct = ", ".join([c.strip() for c in correct.split(",")])
            distractors = []
            while len(distractors) < 3:
                combo = ", ".join(random.choices(base, k=2))
                if combo != correct and combo not in distractors:
                    distractors.append(combo)
            return random.sample(distractors + [correct], 4)
        else:
            distractors = [x for x in base if x != correct]
            return random.sample(distractors, 3) + [correct]

    if "tab2_index" not in st.session_state:
        st.session_state.tab2_index = 0

    row = df.iloc[st.session_state.tab2_index]
    question = make_cloze(row['Level_02'], row['Level_02_Focus'])
    options = generate_options(row['Level_02_Focus'])

    st.markdown("**문장:**")
    st.markdown(question, unsafe_allow_html=True)
    st.caption(row['Level_02_Meaning'])
    user_answer = st.radio("어떤 관계대명사가 들어갈까요?", options)

    if st.button("정답 확인", key="check2"):
        if user_answer.replace(" ", "") == row['Level_02_Focus'].replace(" ", ""):
            st.success("🎉 정답입니다!")
        else:
            st.error(f"❌ 정답은: {row['Level_02_Focus']}")

    if st.button("다음 문장", key="next2"):
        st.session_state.tab2_index = (st.session_state.tab2_index + 1) % len(df)
        st.rerun()

# -------------------------------
# 🧩 Level 3: 단어 배열 퀴즈
# -------------------------------
with level3:
    st.subheader("🧩 단어 배열 퀴즈")

    if "tab3_index" not in st.session_state:
        st.session_state.tab3_index = 0
        st.session_state.tab3_selected = []
        st.session_state.tab3_shuffled = []
        st.session_state.tab3_trigger = False

    row = df.iloc[st.session_state.tab3_index]
    answer = row['Level_03']
    meaning = row['Level_03_Meaning']

    if not st.session_state.tab3_shuffled:
       words = re.findall(r"\w+|[^\w\s]", answer)
       st.session_state.tab3_shuffled = random.sample(words, len(words))

    st.caption(meaning)
    cols = st.columns(len(st.session_state.tab3_shuffled))
    for i, word in enumerate(st.session_state.tab3_shuffled):
        if word not in st.session_state.tab3_selected:
            if cols[i].button(word, key=f"word_{i}"):
                st.session_state.tab3_selected.append(word)
                st.session_state.tab3_trigger = True

    if st.session_state.tab3_trigger:
        st.session_state.tab3_trigger = False
        st.rerun()

    st.markdown("**문장 조립:**")
    st.write(" ".join(st.session_state.tab3_selected))

    if st.button("정답 확인", key="check3"):
        if " ".join(st.session_state.tab3_selected) == answer:
            st.success("🎉 정답입니다!")
        else:
            st.error("❌ 틀렸어요. 다시 시도해 보세요.")

    if st.button("다음 문장", key="next3"):
        st.session_state.tab3_index = (st.session_state.tab3_index + 1) % len(df)
        st.session_state.tab3_selected = []
        st.session_state.tab3_shuffled = []
        st.rerun()
