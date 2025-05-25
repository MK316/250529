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
    },
    "where": {
        "desc": "장소를 설명할 때 사용합니다.",
        "A": "That is the place.",
        "B": "We met at the place.",
        "C": "That is the place **where we met**.",
        "K": "→ 저곳이 우리가 만난 장소예요."
    },
    "when": {
        "desc": "시간을 설명할 때 사용합니다.",
        "A": "I remember the day.",
        "B": "We met on that day.",
        "C": "I remember the day **when we met**.",
        "K": "→ 나는 우리가 만났던 날을 기억해요."
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
tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# -------------------------
# ✅ TAB 1
# -------------------------
with tab1:
    st.header("🐣 관계대명사 문장 연습 (Level 1)")
    st.caption("주어진 문장을 보고 맞는 문장인지 판단해 보세요.")
    st.markdown("---")

    if "completed_tab1" not in st.session_state:
        st.session_state.completed_tab1 = set()

    remaining_tab1 = [i for i in range(len(df)) if i not in st.session_state.completed_tab1]

    if not remaining_tab1:
        st.success("🎉 모든 문제를 완료했습니다!")
        st.stop()

    st.markdown(f"**남은 문제 수: {len(remaining_tab1)}**")

    if "current_index" not in st.session_state or st.session_state.current_index not in remaining_tab1:
        st.session_state.current_index = random.choice(remaining_tab1)
        st.session_state.show_feedback = False
        st.session_state.user_choice = None

    row = df.iloc[st.session_state.current_index]
    sentence = str(row["Level_01"])
    correct_answer = row["Answer1"]
    correction = row["Level_01_Correct"]
    meaning = row["Level_01_Meaning"]
    focus = str(row.get("Level_01_Focus", "")).strip()

    highlighted_sentence = highlight_focus(sentence, focus)

    st.markdown("#### 📌 문장:")
    components.html(f"""
    <div style='font-size:22px; font-family:sans-serif; line-height:1.5em;'>
        {highlighted_sentence}
    </div>
    """, height=120)

    st.caption(f"📘 해석: {meaning}")
    st.markdown("---")

    user_choice = st.radio("이 문장은 문법적으로 맞나요?", ["Correct", "Incorrect"],
                           key=f"choice_{st.session_state.current_index}")

    if st.button("✅ 정답 확인"):
        st.session_state.user_choice = user_choice
        st.session_state.show_feedback = True

    if st.session_state.show_feedback:
        if st.session_state.user_choice == correct_answer:
            st.success("✅ 정답입니다!")
            st.session_state.completed_tab1.add(st.session_state.current_index)
        else:
            st.error("❌ 틀렸어요.")

        st.markdown("**👉 올바른 문장:**")
        st.info(correction if pd.notna(correction) else "정답 문장이 없습니다.")

        if st.button("➡️ 다음 문제"):
            remaining_tab1 = [i for i in range(len(df)) if i not in st.session_state.completed_tab1]
            if remaining_tab1:
                st.session_state.current_index = random.choice(remaining_tab1)
                st.session_state.show_feedback = False
                st.rerun()

# -------------------------
# ✅ TAB 2: Cloze 퀴즈 with 복습
# -------------------------
with tab2:
    st.header("🐸 관계대명사 빈칸 퀴즈 (Level 2)")
    st.caption("문장의 빈칸에 들어갈 올바른 관계대명사를 고르세요.")
    st.markdown("---")

    if "tab2_correct_ids" not in st.session_state:
        st.session_state.tab2_correct_ids = set()

    all_tab2_ids = list(range(len(df)))
    unanswered_tab2_ids = [i for i in all_tab2_ids if i not in st.session_state.tab2_correct_ids]

    st.markdown(f"**남은 문제 수: {len(unanswered_tab2_ids)}**")

    if not unanswered_tab2_ids:
        st.success("🎉 모든 문제를 완료했습니다!")
        st.stop()

    if "tab2_index" not in st.session_state or st.session_state.tab2_index not in unanswered_tab2_ids:
        if st.session_state.tab2_wrong_ids:
            st.session_state.tab2_index = random.choice(list(st.session_state.tab2_wrong_ids))
        else:
            st.session_state.tab2_index = random.choice(unanswered_tab2_ids)

    row = df.iloc[st.session_state.tab2_index]
    sentence = row["Level_02"]
    meaning = row["Level_02_Meaning"]
    focus = row["Level_02_Focus"].strip()

    if "tab2_options" not in st.session_state:
        st.session_state.tab2_options = generate_options(focus)
        st.session_state.tab2_feedback = False
        st.session_state.tab2_choice = None

    cloze_sentence = make_cloze(sentence, focus)
    options = st.session_state.tab2_options

    st.markdown("#### 📌 문장 (빈칸 채우기):")
    components.html(f"""
        <div style='font-size:20px; font-family:sans-serif; line-height:1.5em;'>
            {cloze_sentence}
        </div>
    """, height=100)

    st.caption(f"📘 해석: {meaning}")

    user_answer = st.radio("빈 칸에 어떤 관계대명사가 들어가는 게 가장 좋을까요?", options,
                           key=f"tab2_choice_{st.session_state.tab2_index}")

    if st.button("✅ 정답 확인", key="check_tab2"):
        st.session_state.tab2_feedback = True
        st.session_state.tab2_choice = user_answer

    if st.session_state.tab2_feedback:
        if st.session_state.tab2_choice.replace(" ", "") == focus.replace(" ", ""):
            st.success("🎉 정답입니다!")
            st.session_state.tab2_correct_ids.add(st.session_state.tab2_index)
            st.session_state.tab2_wrong_ids.discard(st.session_state.tab2_index)
        else:
            st.error(f"❌ 아쉽네요. 정답은: {focus}")
            st.session_state.tab2_wrong_ids.add(st.session_state.tab2_index)

        if st.button("➡️ 다음 문제", key="next_tab2"):
            unanswered_tab2_ids = [i for i in range(len(df)) if i not in st.session_state.tab2_correct_ids]
            if unanswered_tab2_ids:
                if st.session_state.tab2_wrong_ids:
                    st.session_state.tab2_index = random.choice(list(st.session_state.tab2_wrong_ids))
                else:
                    st.session_state.tab2_index = random.choice(unanswered_tab2_ids)
                new_row = df.iloc[st.session_state.tab2_index]
                st.session_state.tab2_options = generate_options(new_row['Level_02_Focus'].strip())
                st.session_state.tab2_feedback = False
                st.rerun()
