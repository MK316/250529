# Streamlit Homework Quiz App with Levels and Certificate

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

# ---------------------
# 🧠 Load Data
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

# ---------------------
# 🧾 Certificate Generator
# ---------------------
def generate_certificate(user_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "Certificate of Completion")

    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 140, f"This certifies that")
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 170, user_name)
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 200, "has successfully completed all quiz levels.")

    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, height - 240, "Issued by AI English Quiz App")

    c.save()
    buffer.seek(0)
    return buffer

# ---------------------
# 🚀 Start App
# ---------------------
st.title("📚 Homework Quiz: Level 1 to 3")

# ✅ User input
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "name_entered" not in st.session_state:
    st.session_state["name_entered"] = False

if not st.session_state.name_entered:
    user_name_input = st.text_input("Enter your name to begin:", key="name_input")
    if st.button("Start Quiz") and user_name_input.strip():
        st.session_state.username = user_name_input.strip()
        st.session_state.name_entered = True
        st.rerun()
    st.stop()

st.markdown(f"**👤 Student:** {st.session_state.username}")

# ✅ Track completed levels
if "completed_levels" not in st.session_state:
    st.session_state.completed_levels = set()

# ✅ Select level
level = st.selectbox("Select a quiz level:", ["Level 1", "Level 2", "Level 3"])

# ✅ Sample 5 questions from each level
df_sample = df.sample(5, random_state=random.randint(0, 999))

# ---------------------
# LEVEL 1
# ---------------------
if level == "Level 1":
    st.header("🌀 Level 1: Correct or Incorrect")
    for i, row in df_sample.iterrows():
        sentence = row['Level_01']
        focus = row['Level_01_Focus']
        meaning = row['Level_01_Meaning']
        answer = row['Answer1']

        st.markdown(f"**Q{i+1}.** {sentence}")
        st.caption(f"해석: {meaning}")
        user_answer = st.radio(f"Is the sentence grammatically correct?", ["Correct", "Incorrect"], key=f"lvl1_{i}")
        if user_answer == answer:
            st.success("Correct")
        else:
            st.error("Wrong")

    if st.button("✅ Mark Level 1 as Completed"):
        st.session_state.completed_levels.add("Level 1")

# ---------------------
# LEVEL 2
# ---------------------
elif level == "Level 2":
    st.header("🌀 Level 2: Fill in the Relative Pronoun")
    for i, row in df_sample.iterrows():
        sentence = row['Level_02']
        focus = row['Level_02_Focus']
        meaning = row['Level_02_Meaning']
        cloze = re.sub(rf"\b{re.escape(focus)}\b", "_____", sentence, 1)

        st.markdown(f"**Q{i+1}.** {cloze}")
        st.caption(f"해석: {meaning}")
        user_answer = st.text_input("Type the missing word:", key=f"lvl2_{i}")
        if user_answer.strip() == focus.strip():
            st.success("Correct")
        else:
            st.error(f"Wrong. Answer: {focus}")

    if st.button("✅ Mark Level 2 as Completed"):
        st.session_state.completed_levels.add("Level 2")

# ---------------------
# LEVEL 3
# ---------------------
elif level == "Level 3":
    st.header("🌀 Level 3: Word Order Quiz")
    for i, row in df_sample.iterrows():
        sentence = row['Level_03']
        meaning = row['Level_03_Meaning']
        words = re.findall(r"\w+(?:'\w+)?[.,!?;]?", sentence)

        shuffled = random.sample(words, len(words))

        st.markdown(f"**Q{i+1}.** Arrange the sentence:")
        st.caption(f"해석: {meaning}")
        st.write(" → ", "  ".join(shuffled))
        user_answer = st.text_input("Type your sentence:", key=f"lvl3_{i}")

        def normalize(text):
            return re.sub(r"\s+([.,!?;])", r"\1", text.strip())

        if normalize(user_answer) == normalize(sentence):
            st.success("Correct")
        else:
            st.error(f"Wrong. Answer: {sentence}")

    if st.button("✅ Mark Level 3 as Completed"):
        st.session_state.completed_levels.add("Level 3")

# ---------------------
# 🎉 Certificate Download
# ---------------------
if {"Level 1", "Level 2", "Level 3"}.issubset(st.session_state.completed_levels):
    st.success("🎉 All levels completed!")
    cert_file = generate_certificate(st.session_state.username)
    st.download_button("📄 Download Certificate", cert_file, file_name="certificate.pdf")
