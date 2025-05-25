# 📦 Required Libraries
import streamlit as st
from gtts import gTTS
from io import BytesIO
import streamlit.components.v1 as components

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

# Sorted vocabulary dictionary (already prepared)
sorted_vocab = dict(sorted(vocab_dict.items()))

# ✅ Step 1: Get current page path dynamically
current_page_path = st.experimental_get_url().split("?")[0]

# ✅ Step 2: Create inline buttons with correct link
st.markdown("### 📘 Click a word to learn")
html = "<div style='display: flex; flex-wrap: wrap; gap: 10px;'>"

for word in sorted_vocab:
    encoded_word = urllib.parse.quote(word)
    html += f"""
    <a href="{current_page_path}?word={encoded_word}" target="_self">
        <button style="
            padding: 10px 16px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f9f9f9;
            cursor: pointer;">{word}</button>
    </a>
    """

html += "</div>"
components.html(html, height=300)

# ✅ Step 3: Handle query param
query_params = st.experimental_get_query_params()
selected_word = query_params.get("word", [None])[0]

# ✅ Step 4: Show TTS and meaning if word selected
if selected_word and selected_word in sorted_vocab:
    meaning, sentence = sorted_vocab[selected_word]

    # Word TTS
    tts_word = gTTS(text=selected_word, lang='en')
    audio_word = BytesIO()
    tts_word.write_to_fp(audio_word)
    audio_word.seek(0)

    # Sentence TTS
    tts_sentence = gTTS(text=sentence, lang='en')
    audio_sentence = BytesIO()
    tts_sentence.write_to_fp(audio_sentence)
    audio_sentence.seek(0)

    st.markdown(f"## ✅ {selected_word}")
    st.markdown(f"**Korean**: {meaning}")
    st.markdown(f"**Example**: _{sentence}_")
    st.markdown("🔈 **Word Pronunciation**")
    st.audio(audio_word, format="audio/mp3")
    st.markdown("🗣️ **Sentence Audio**")
    st.audio(audio_sentence, format="audio/mp3")
