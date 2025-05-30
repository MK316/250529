# 📚 Review Quiz App with Levels and Certificate
import streamlit as st
import pandas as pd
import random
import re
from gtts import gTTS
import tempfile
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import requests

# ---------------------
# 🧠 Load Data
# ---------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MK316/250529/refs/heads/main/data/data05.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=[
        "Level_01", "Answer1", "Level_01_Correct", "Level_01_Meaning",
        "Level_02", "Level_02_Focus", "Level_02_Meaning", "Level_02_Options", "Level_02_Answer",
        "Level_03", "Level_03_Meaning"
    ])
    return df.reset_index(drop=True)

df = load_data()

# ---------------------
# 🧾 Certificate Generator
# ---------------------
def generate_certificate(user_name, scores, start_time, end_time):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    try:
        award_url = "https://raw.githubusercontent.com/MK316/250529/main/images/medal2.png"
        response = requests.get(award_url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        c.drawImage(tmp_path, width - 120, height - 150, width=70, height=70, preserveAspectRatio=True)
    except Exception as e:
        print("Failed to load award image:", e)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "Certificate of Completion")
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 140, "This certifies that")
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 170, user_name)
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 200, "has successfully completed all quiz levels.")

    y = height - 250
    for level, score in scores.items():
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, y, f"{level}: {score} / 5 correct")
        y -= 20

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y - 10, f"Start Time: {start_time}")
    c.drawCentredString(width / 2, y - 30, f"End Time: {end_time}")
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, y - 60, "Issued by AI English Quiz App")
    c.save()
    buffer.seek(0)
    return buffer

# ---------------------
# 🚀 Start App
# ---------------------
st.markdown("### 📚 Review Quiz: 총 15 문법 문제")
st.caption("Level 1, 2, 3를 모두 풀면 마지막에 확인서를 다운받을 수 있습니다.")

if st.button("🔄 Quiz 다시 시작하기"):
    st.session_state.clear()
    st.rerun()

if "username" not in st.session_state:
    st.session_state["username"] = ""
if "name_entered" not in st.session_state:
    st.session_state["name_entered"] = False
if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if not st.session_state.name_entered:
    user_name_input = st.text_input("😉 본인 이름을 쓰고 시작하세요 (반드시 영어로 쓰세요):", key="name_input")
    if st.button("Start Quiz") and user_name_input.strip():
        st.session_state.username = user_name_input.strip()
        st.session_state.name_entered = True
        st.session_state.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
    st.stop()

st.markdown(f"**👤 Student:** {st.session_state.username}")
st.markdown(f"**🕒 Start Time:** {st.session_state.start_time}")

if "completed_levels" not in st.session_state:
    st.session_state.completed_levels = set()
if "scores" not in st.session_state:
    st.session_state.scores = {}

level = st.selectbox("레벨을 선택하세요 (3레벨을 모두 끝내야 확인서를 출력할 수 있습니다.):", ["Level 1", "Level 2", "Level 3"])

if "sampled_questions" not in st.session_state:
    st.session_state.sampled_questions = {}
if "shuffled_words" not in st.session_state:
    st.session_state.shuffled_words = {}

if level not in st.session_state.sampled_questions:
    st.session_state.sampled_questions[level] = df.sample(5, random_state=random.randint(0, 999))

user_responses = {}
df_sample = st.session_state.sampled_questions[level]

# ---------------------
# LEVEL 1
# ---------------------
if level == "Level 1":
    st.header("🌀 Level 1: 다음 문장이 맞을까요 틀릴까요?")
    for i, row in df_sample.iterrows():
        st.markdown(f"**Q{i+1}.** {row['Level_01']}")
        st.caption(f"해석: {row['Level_01_Meaning']}")
        user_responses[i] = st.radio("Your answer:", ["Correct", "Incorrect"], key=f"lvl1_{i}")
    if st.button("✅ Submit Level 1 Answers"):
        score = sum(user_responses[i] == row["Answer1"] for i, row in df_sample.iterrows())
        st.success(f"Level 1 Score: {score} / 5")
        st.session_state.completed_levels.add("Level 1")
        st.session_state.scores["Level 1"] = score

# ---------------------
# LEVEL 2
# ---------------------
elif level == "Level 2":
    st.header("🌀 Level 2: 관계대명사 넣기")

    def make_cloze(sentence, focus):
        if "," in focus:
            parts = [f.strip() for f in focus.split(",")]
            for part in parts:
                # Replace only the first match of each part (even if preceded by punctuation)
                sentence = re.sub(rf"(\W)?\b{re.escape(part)}\b", lambda m: f"{m.group(1) if m.group(1) else ''}_____", sentence, 1)
        else:
            sentence = re.sub(rf"\b{re.escape(focus.strip())}\b", "_____", sentence, 1)
        return sentence

    for i, row in df_sample.iterrows():
        sentence = make_cloze(row['Level_02'], row['Level_02_Focus'])
        options = [opt.strip() for opt in row["Level_02_Options"].split(",")]
        st.markdown(f"**Q{i+1}.** {sentence}")
        st.caption(f"해석: {row['Level_02_Meaning']}")
        user_responses[i] = st.radio("Choose:", options, key=f"lvl2_{i}")

    if st.button("✅ Submit Level 2 Answers"):
        score = 0
        for i, row in df_sample.iterrows():
            correct_answers = [ans.strip() for ans in row["Level_02_Answer"].split(",")]
            if user_responses[i].strip() in correct_answers:
                score += 1
        st.success(f"Level 2 Score: {score} / 5")
        st.session_state.completed_levels.add("Level 2")
        st.session_state.scores["Level 2"] = score


# ---------------------
# LEVEL 3
# ---------------------
elif level == "Level 3":
    st.header("🌀 Level 3: 단어 순서로 문장 만들기")

    def tokenize(sentence):
        return re.findall(r"\b\w+(?:['’]\w+)?\b|[.,!?;]", sentence)

    for i, row in df_sample.iterrows():
        sentence = row["Level_03"]
        key = f"lvl3_shuffled_{i}"
        if key not in st.session_state.shuffled_words:
            tokens = tokenize(sentence)
            st.session_state.shuffled_words[key] = random.sample(tokens, len(tokens))
        shuffled = st.session_state.shuffled_words[key]
        st.markdown(f"**Q{i+1}.** Arrange the sentence:")
        st.caption(f"해석: {row['Level_03_Meaning']}")
        st.write(" →", "  ".join(shuffled))
        user_responses[i] = st.text_input("Type your sentence:", key=f"lvl3_{i}")

    def normalize(text):
        return re.sub(r"\s+([.,!?;])", r"\1", text.strip())

    if st.button("✅ Submit Level 3 Answers"):
        score = 0
        for i, row in df_sample.iterrows():
            if normalize(user_responses[i]) == normalize(row["Level_03"]):
                score += 1
        st.success(f"Level 3 Score: {score} / 5")
        st.session_state.completed_levels.add("Level 3")
        st.session_state.scores["Level 3"] = score

# ---------------------
# 🔊 Completion Audio + Certificate
# ---------------------
def play_audio_summary(name, scores):
    message = f"{name}, congratulations! You have completed all levels. "
    for level, score in scores.items():
        message += f"{level} score is {score} out of 5. "
    tts = gTTS(message, lang='en')
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

# ---------------------
# ✅ Certificate Display
# ---------------------
if {"Level 1", "Level 2", "Level 3"}.issubset(st.session_state.completed_levels):
    st.success("🎉 All levels completed!")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cert = generate_certificate(
        st.session_state.username,
        st.session_state.scores,
        st.session_state.start_time,
        end_time
    )
    st.markdown("#### ▶ Summary Audio")
    play_audio_summary(st.session_state.username, st.session_state.scores)
    st.download_button("💙 확인서 다운받기 💙", cert, file_name="certificate.pdf")
