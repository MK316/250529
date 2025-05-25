import streamlit as st
import pandas as pd
import random
import re
import streamlit.components.v1 as components
from gtts import gTTS
import tempfile
import base64



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

# ✅ Highlight the focus word in red
def highlight_focus(sentence, focus):
    if not sentence or not focus:
        return sentence
    try:
        focus = str(focus).strip()
        escaped_focus = re.escape(focus)
        pattern = re.compile(rf'\b({escaped_focus})\b')
        return pattern.sub(r"<span style='color:red; font-weight:bold'>\1</span>", sentence, count=1)
    except:
        return sentence




# 탭 구성
level1, level2, level3 = st.tabs(["🌀 Level 1", "🌀 Level 2", "🌀 Level 3"])

# -------------------------------
# ✅ Level 1: 문장 정답 판단
# -------------------------------


with level1:
    st.subheader("🐥 문장이 맞는지 판단하기 (Level 1)")

    if "tab1_index" not in st.session_state:
        st.session_state.tab1_index = 0
        st.session_state.tab1_score = 0
        st.session_state.show_hint1 = False

    def highlight_focus(sentence, focus):
        if not sentence or not focus:
            return sentence
        try:
            focus = str(focus).strip()
            escaped_focus = re.escape(focus)
            pattern = re.compile(rf'\b({escaped_focus})\b')
            return pattern.sub(r"<span style='color:red; font-weight:bold'>\1</span>", sentence, count=1)
        except:
            return sentence

    row = df.iloc[st.session_state.tab1_index]
    sentence = row['Level_01']
    focus = row['Level_01_Focus']
    correct_sentence = row['Level_01_Correct']
    highlighted = highlight_focus(sentence, focus)

    st.caption(f"🔢 진행 상황: {st.session_state.tab1_index + 1} / {len(df)} 문장")

    st.markdown("**문장:**")
    components.html(f"""
        <div style='font-size:20px; font-family:sans-serif; line-height:1.6em;'>
            {highlighted}
        </div>
    """, height=80)

    st.caption("🐾 해석석: " + row['Level_01_Meaning'])

    # Hint button and audio (only show on click)
    if st.button("💡 Hint 보기 (정답 듣기)"):
        st.session_state.show_hint1 = True

    if st.session_state.get("show_hint1", False):
        def prepare_text_for_tts(text):
            return re.sub(r'\bAI\b', 'A I', text)

        correct_sentence_for_tts = prepare_text_for_tts(correct_sentence)
        tts = gTTS(text=correct_sentence, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_data = open(fp.name, "rb").read()
            b64 = base64.b64encode(audio_data).decode()
            audio_html = f"""
            <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

    choice = st.radio("문장이 맞나요?", ["Correct", "Incorrect"])

    if st.button("정답 확인", key="check1"):
        if choice == row['Answer1']:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸습니다.")
        st.markdown("**📘 올바른 문장:**")
        st.info(correct_sentence)

    if st.button("다음 문장", key="next1"):
        st.session_state.tab1_index = (st.session_state.tab1_index + 1) % len(df)
        st.session_state.show_hint1 = False  # Reset hint flag
        st.rerun()


# -------------------------------
# ✏️ Level 2: 관계대명사 빈칸 채우기
# -------------------------------
with level2:
    st.subheader("🐸 관계대명사 빈칸 채우기 (Level 2)")

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
    st.caption(f"🔢 진행 상황: {st.session_state.tab2_index + 1} / {len(df)} 문장")

    st.markdown(question, unsafe_allow_html=True)
    st.caption("🐾 해석: " + str(row['Level_02_Meaning']))
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
# 🐳 Level 3: 단어 배열 퀴즈
# -------------------------------
with level3:
    st.subheader("🐳 단어 배열 퀴즈 (Level 3)")

    if "tab3_index" not in st.session_state:
        st.session_state.tab3_index = 0
        st.session_state.tab3_selected = []
        st.session_state.tab3_shuffled = []

    if "tab3_trigger" not in st.session_state:
        st.session_state.tab3_trigger = False

    row = df.iloc[st.session_state.tab3_index]
    answer = row['Level_03']
    meaning = row['Level_03_Meaning']

    if not st.session_state.tab3_shuffled:
       words = re.findall(r"\w+(?:'\w+)?[.,!?;]?", answer)


       st.session_state.tab3_shuffled = random.sample(words, len(words))

    st.caption(meaning)

    ## NEw
    st.markdown("### 👉 단어를 클릭하세요:")

# Arrange 5 word buttons per row (left-aligned if fewer than 5)
    words = st.session_state.tab3_shuffled
    for i in range(0, len(words), 5):
        row_words = words[i:i+5]
        cols = st.columns(5)  # Always create 5 columns
        for j, word in enumerate(row_words):
            if word not in st.session_state.tab3_selected:
                if cols[j].button(word, key=f"word_{i+j}"):
                    st.session_state.tab3_selected.append(word)
                    st.session_state["tab3_trigger"] = True
    


    if st.session_state.tab3_trigger:
        st.session_state.tab3_trigger = False
        st.rerun()

    st.markdown("**문장 조립:**")
    st.caption(f"🔢 진행 상황: {st.session_state.tab3_index + 1} / {len(df)} 문장")
    def smart_join(words):
        result = ""
        for i, word in enumerate(words):
            if i > 0 and re.match(r"[.,!?;]", word):
                result += word  # attach punctuation directly
            else:
                if result:  # add space before non-punctuation
                    result += " "
                result += word
        return result
    
    user_input = smart_join(st.session_state.tab3_selected)
    
    st.write(user_input)
    


    # 🔧 정답 비교를 위한 정규화 함수
    def normalize(text):
        return re.sub(r"\s+([.,!?;])", r"\1", text.strip())

    if st.button("정답 확인", key="check3"):
        normalized_user = normalize(user_input)
        normalized_answer = normalize(answer)

        if normalized_user == normalized_answer:
            st.success("🎉 정답입니다!")
        else:
            st.error("❌ 틀렸어요. 다시 시도해 보세요.")
            st.info(f"👉 정답: {answer}")


    if st.button("다음 문장", key="next3"):
        st.session_state.tab3_index = (st.session_state.tab3_index + 1) % len(df)
        st.session_state.tab3_selected = []
        st.session_state.tab3_shuffled = []
        st.rerun()
