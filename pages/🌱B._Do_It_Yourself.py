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
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data05.csv"
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

    row = df.iloc[st.session_state.tab1_index]
    sentence = row['Level_01']
    focus = row['Level_01_Focus']
    correct_sentence = row['Level_01_Correct']
    highlighted = highlight_focus(sentence, focus)

    st.caption(f"🔢 진행 상황: {st.session_state.tab1_index + 1} / {len(df)} 문장")

    components.html(f"""
        <div style='font-size:20px; font-family:sans-serif; line-height:1.6em;'>
            {highlighted}
        </div>
    """, height=80)

    st.caption("🐾 해석: " + row['Level_01_Meaning'])

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

    choice = st.radio("Q: 주어진 문장이 문법에 맞을까요?", ["Correct", "Incorrect"])

    if st.button("정답 확인", key="check1"):
        if choice == row['Answer1']:
            st.success("✅ 정답입니다!")
            st.balloons()
        else:
            st.error("❌ 틀렸습니다.")
        st.markdown("**📘 올바른 문장:**")
        st.info(correct_sentence)

    if st.button("다음 문장", key="next1"):
        st.session_state.tab1_index = (st.session_state.tab1_index + 1) % len(df)
        st.session_state.show_hint1 = False
        st.rerun()

# -------------------------------
# ✏️ Level 2: 관계대명사 빈칸 채우기
# -------------------------------
with level2:
    st.subheader("🐸 관계대명사 빈칸 채우기 (Level 2)")

    import re
    import random

    def make_cloze(sentence, focus):
        if "," in focus:
            parts = [p.strip() for p in focus.split(",")]
            if len(parts) == 2:
                part1, part2 = parts
                sentence = re.sub(rf"\b{re.escape(part1)}\b", "<u>_____</u>", sentence, 1)
                sentence = re.sub(rf"(,\s*){re.escape(part2)}\b", r"\1<u>_____</u>", sentence, 1)
        else:
            sentence = re.sub(rf"\b{re.escape(focus)}\b", "<u>_____</u>", sentence, 1)
        return sentence

    def parse_options(option_str):
        return [opt.strip() for opt in option_str.split(",")]

    def check_answer(user, answer):
        # Accept if the answer matches (strip space and case-insensitive)
        correct_answers = [a.strip().lower() for a in answer.split(",")]
        return user.strip().lower() in correct_answers

    if "tab2_index" not in st.session_state:
        st.session_state.tab2_index = 0
        st.session_state.tab2_feedback = False
        st.session_state.tab2_user_answer = None

    row = df.iloc[st.session_state.tab2_index]
    question = make_cloze(row['Level_02'], row['Level_02_Focus'])
    options = parse_options(row['Level_02_Options'])
    answer = row['Level_02_Answer']

    st.caption(f"🔢 진행 상황: {st.session_state.tab2_index + 1} / {len(df)} 문장")

    import streamlit.components.v1 as components
    components.html(f"""
        <div style='font-size:20px; font-family:sans-serif; line-height:1.6em;'>
            {question}
        </div>
    """, height=80)

    st.caption("🐾 해석: " + str(row['Level_02_Meaning']) if 'Level_02_Meaning' in row else "")

    user_answer = st.radio("Q: 어떤 관계대명사가 들어갈 수 있을까요?", options, key=f"tab2_radio_{st.session_state.tab2_index}")

    if st.button("정답 확인", key="check2"):
        st.session_state.tab2_user_answer = user_answer
        st.session_state.tab2_feedback = True

    if st.session_state.tab2_feedback:
        if check_answer(st.session_state.tab2_user_answer, answer):
            st.success("🎉 정답입니다!")
            st.balloons()
        else:
            st.error(f"❌ 정답은: {answer}")

    if st.button("다음 문장", key="next2"):
        st.session_state.tab2_index = (st.session_state.tab2_index + 1) % len(df)
        st.session_state.tab2_feedback = False
        st.session_state.tab2_user_answer = None
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
        st.session_state.tab3_trigger = False

    st.caption(f"🔢 진행 상황: {st.session_state.tab3_index + 1} / {len(df)} 문장")

    row = df.iloc[st.session_state.tab3_index]
    answer = row['Level_03']
    meaning = row['Level_03_Meaning']

    # ✅ Tokenizer that preserves "wasn't", "Here's", etc.
    def tokenize(text):
        return re.findall(r"\b\w+(?:['’]\w+)?\b|[.,!?;]", text)

    if not st.session_state.tab3_shuffled:
        words = tokenize(answer)
        st.session_state.tab3_shuffled = random.sample(words, len(words))

    st.markdown("---")
    st.markdown("##### 👉 단어를 순서대로 클릭하여 의미에 맞는 문장을 완성해 보세요:")
    st.caption("🐾 해석: " + meaning)

    words = st.session_state.tab3_shuffled
    for i in range(0, len(words), 5):
        row_words = words[i:i+5]
        cols = st.columns(len(row_words))
        for j, word in enumerate(row_words):
            if word not in st.session_state.tab3_selected:
                if cols[j].button(word, key=f"word_{i+j}_{st.session_state.tab3_index}"):
                    st.session_state.tab3_selected.append(word)
                    st.rerun()

    # 🔧 단어 선택 취소
    if st.session_state.tab3_selected:
        if st.button("↩️ 마지막 선택 취소"):
            st.session_state.tab3_selected.pop()
            st.rerun()

    st.markdown("**문장 조립:**")

    def smart_join(words):
        result = ""
        for i, word in enumerate(words):
            if i > 0 and re.match(r"[.,!?;]", word):
                result += word
            else:
                if result:
                    result += " "
                result += word
        return result

    user_input = smart_join(st.session_state.tab3_selected)
    st.write(user_input)

    def normalize(text):
        return re.sub(r"\s+([.,!?;])", r"\1", text.strip())

    # ✅ 정답 확인
    if st.button("정답 확인", key="check3"):
        if normalize(user_input) == normalize(answer):
            st.success("🎉 정답입니다!")
        else:
            st.error("❌ 틀렸어요. 다시 시도해 보세요.")
            st.info(f"👉 정답: {answer}")

    # ✅ 다음 문장
    if st.button("다음 문장", key="next3"):
        st.session_state.tab3_index = (st.session_state.tab3_index + 1) % len(df)
        st.session_state.tab3_selected = []
        st.session_state.tab3_shuffled = []
        st.rerun()
