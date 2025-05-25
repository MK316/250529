# 📦 Required Libraries
import streamlit as st
from gtts import gTTS
from io import BytesIO
import streamlit.components.v1 as components
import urllib.parse

# 🔡 Vocabulary Dictionary: word → (Korean meaning, example sentence)
vocab_dict = {
    "Artificial Intelligence (AI)": ("인공지능", "This is the path that 'AI' followed."),
    "artists": ("예술가들", "The AI, which mimics the style of the other artists, created the picture."),
    "artworks": ("작품들", "The show had artworks that moved!"),
    "built": ("지었다", "They built a machine that mimics artists."),
    "consider": ("여기다, 고려하다", "We can see AI platforms and art that some viewers consider more impressive."),
    "contemporary": ("현대의", "An incident occurred that thrilled the contemporary art scene."),
    "creativity": ("창의성", "Look at the mechanism of AI creativity, which is programmed to work in a similar way to human creativity."),
    "developed": ("개발했다", "We are the engineers who developed that AI system."),
    "fake": ("가짜의", "The image, which went viral, was fake."),
    "followed": ("따랐다", "This is the path that AI followed."),
    "genius": ("천재적인", "The idea, which came from a cat video, was genius."),
    "impressive": ("인상적인", "We can see AI platforms and art that some viewers consider more impressive."),
    "incident": ("사건", "An incident occurred that thrilled the contemporary art scene."),
    "insist": ("주장하다", "There are those who insist that AI is more than a tool."),
    "machine": ("기계", "The machine learns by itself, which is done through a machine learning."),
    "major": ("주요한", "This pattern of AI creation is much like the path which is taken by major artists."),
    "mechanism": ("기계 장치, 구조", "Look at the mechanism of AI creativity, which is programmed to work in a similar way to human creativity."),
    "mimics": ("흉내내다", "They built a machine that mimics artists."),
    "occurred": ("발생했다", "An incident occurred that thrilled the contemporary art scene."),
    "path": ("길", "This is the path that AI followed."),
    "platforms": ("플랫폼들", "We can see AI platforms and art that some viewers consider more impressive."),
    "portrait": ("초상화", "A portrait that is created by AI was sold for nearly half a million dollars."),
    "presented": ("제시했다", "They presented a video that showed the AI's production process."),
    "production": ("생산", "They presented a video that showed the AI's production process."),
    "programmed": ("프로그래밍된", "Look at the mechanism of AI creativity, which is programmed to work in a similar way to human creativity."),
    "tech": ("기술", "The style, which feels old, is made by new tech."),
    "thrilled": ("전율하게 하다", "An incident occurred that thrilled the contemporary art scene."),
    "viral": ("입소문 난", "The image, which went viral, was fake."),
}

sorted_vocab = dict(sorted(vocab_dict.items()))

st.set_page_config(page_title="Words in Context", layout="wide")
st.title("🎧 Vocabulary Practice with Audio and Meaning")

# --- Simulate inline layout using columns (6 per row) ---
cols_per_row = 5
row = st.columns(cols_per_row)
col_index = 0

for word in sorted_vocab.keys():
    if row[col_index].button(word):
        st.session_state.selected_word = word
    col_index += 1
    if col_index == cols_per_row:
        row = st.columns(cols_per_row)
        col_index = 0

# --- Display selected word info ---
if "selected_word" in st.session_state:
    word = st.session_state.selected_word
    meaning, sentence = sorted_vocab[word]

    # Generate TTS for word
    tts_word = gTTS(text=word, lang='en')
    audio_word = BytesIO()
    tts_word.write_to_fp(audio_word)
    audio_word.seek(0)

    # Generate TTS for sentence
    tts_sentence = gTTS(text=sentence, lang='en')
    audio_sentence = BytesIO()
    tts_sentence.write_to_fp(audio_sentence)
    audio_sentence.seek(0)

    st.markdown(f"## ✅ {word}")
    st.markdown(f"**Korean**: {meaning}")
    st.markdown(f"**Example**: _{sentence}_")
    st.markdown("🔈 **Word Pronunciation**")
    st.audio(audio_word, format="audio/mp3")
    st.markdown("🗣️ **Sentence Audio**")
    st.audio(audio_sentence, format="audio/mp3")
    st.audio(audio_sentence, format="audio/mp3")
