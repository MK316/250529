import streamlit as st
import pandas as pd
import random
import re
import streamlit.components.v1 as components

# -------------------------
# 데이터 로드
# -------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data03.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=["Level_01", "Answer1", "Level_01_Correct", "Level_01_Meaning"])
    return df.reset_index(drop=True)

df = load_data()

if df.empty:
    st.error("❌ 사용할 수 있는 데이터가 없습니다.")
    st.stop()

# -------------------------
# Cloze 문장 생성
# -------------------------

import re

def make_cloze(sentence, focus):
    focus = str(focus).strip()

    if "," in focus:
        parts = [p.strip() for p in focus.split(",")]
        new_sentence = sentence
        for part in parts:
            # 관계대명사 뒤에 공백이 없는 경우를 위한 정규식
            pattern = re.compile(rf"({re.escape(part)})(?=\W|\s|$)")
            match = pattern.search(new_sentence)
            if match:
                start = match.start()
                end = match.end()
                next_char = new_sentence[end:end+1]

                # 단어 다음엔 공백 필요
                spacing = "&nbsp;" if next_char not in [",", ".", ";", ":", "!", "?", ""] else ""
                new_sentence = new_sentence[:start] + "<u> _____ </u>" + spacing + new_sentence[end:]
        return new_sentence
    else:
        pattern = re.compile(rf"({re.escape(focus)})(?=\W|\s|$)")
        match = pattern.search(sentence)
        if match:
            start = match.start()
            end = match.end()
            next_char = sentence[end:end+1]
            spacing = "&nbsp;" if next_char not in [",", ".", ";", ":", "!", "?", ""] else ""
            return sentence[:start] + "<u> _____ </u>" + spacing + sentence[end:]
        return sentence



# -------------------------
# 보기를 생성
# -------------------------
def generate_options(correct):
    all_choices = ['that', 'which', 'who', 'where']
    if "," in correct:
        parts = [p.strip() for p in correct.split(",")]
        correct_combo = ", ".join(parts)
        others = []
        while len(others) < 3:
            distractor = ", ".join(random.choices(all_choices, k=2))
            if distractor != correct_combo and distractor not in others:
                others.append(distractor)
        options = others + [correct_combo]
    else:
        options = random.sample([opt for opt in all_choices if opt != correct], 3) + [correct]
    random.shuffle(options)
    return options

# -------------------------
# 포커스 강조 함수
# -------------------------
def highlight_focus(sentence, focus):
    focus = str(focus).strip()
    if not focus or focus.lower() not in sentence.lower():
        return sentence
    try:
        escaped_focus = re.escape(focus)
        pattern = re.compile(rf'\b{escaped_focus}\b' if focus.isalpha() else escaped_focus, re.IGNORECASE)
        return pattern.sub(
            f"<span style='color:red; font-weight:bold'>{focus}</span>", sentence, count=1
        )
    except:
        return sentence

# -------------------------
# 탭 구성
# -------------------------
tab1, tab2, tab3 = st.tabs(["Level 1", "Level 2", "Level 3"])

# -------------------------
# ✅ TAB 1
# -------------------------
with tab1:
    st.header("📝 관계대명사 문장 연습 (Level 1)")
    st.caption("주어진 문장을 보고 맞는 문장인지 판단해 보세요.")
    st.markdown("---")

    if "current_index" not in st.session_state or st.session_state.current_index >= len(df):
        st.session_state.current_index = random.randint(0, len(df) - 1)
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
        else:
            st.error("❌ 틀렸어요.")

        st.markdown("**👉 올바른 문장:**")
        st.info(correction if pd.notna(correction) else "정답 문장이 없습니다.")

        if st.button("➡️ 다음 문제"):
            st.session_state.current_index = random.randint(0, len(df) - 1)
            st.session_state.show_feedback = False
            st.rerun()

# -------------------------
# ✅ TAB 2: Cloze 퀴즈
# -------------------------
with tab2:
    st.header("✏️ 관계대명사 빈칸 퀴즈 (Level 2)")
    st.caption("문장의 빈칸에 들어갈 올바른 관계대명사를 고르세요.")
    st.markdown("---")

    # 새 문제일 때만 보기 생성
    if "tab2_index" not in st.session_state or "tab2_options" not in st.session_state:
        st.session_state.tab2_index = random.randint(0, len(df) - 1)
        row = df.iloc[st.session_state.tab2_index]
        focus = row["Level_02_Focus"].strip()
        st.session_state.tab2_options = generate_options(focus)
        st.session_state.tab2_feedback = False
        st.session_state.tab2_choice = None

    row = df.iloc[st.session_state.tab2_index]
    sentence = row["Level_02"]
    meaning = row["Level_02_Meaning"]
    focus = row["Level_02_Focus"].strip()
    cloze_sentence = make_cloze(sentence, focus)
    options = st.session_state.tab2_options

    st.markdown("#### 📌 문장 (빈칸 채우기):")
    components.html(f"""
        <div style='font-size:20px; font-family:sans-serif; line-height:1.5em;'>
            {cloze_sentence}
        </div>
    """, height=100)

    st.caption(f"📘 해석: {meaning}")

    user_answer = st.radio("어떤 관계대명사가 들어갈까요?", options,
                           key=f"tab2_choice_{st.session_state.tab2_index}")

    if st.button("✅ 정답 확인", key="check_tab2"):
        st.session_state.tab2_feedback = True
        st.session_state.tab2_choice = user_answer

    if st.session_state.tab2_feedback:
        if st.session_state.tab2_choice.replace(" ", "") == focus.replace(" ", ""):
            st.success("🎉 정답입니다!")
        else:
            st.error(f"❌ 아쉽네요. 정답은: {focus}")

        if st.button("➡️ 다음 문제", key="next_tab2"):
            st.session_state.tab2_index = random.randint(0, len(df) - 1)
            new_row = df.iloc[st.session_state.tab2_index]
            st.session_state.tab2_options = generate_options(new_row['Level_02_Focus'].strip())
            st.session_state.tab2_feedback = False
            st.rerun()
