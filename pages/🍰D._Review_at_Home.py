# streamlit_word_puzzle.py

import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# 💡 Paste your vocab_dict here (as you shared)
vocab_dict = {
    "Artificial Intelligence (AI)": ("인공지능", "This is the path that AI followed."),
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

# --- Select 10 words ---
selected_words = random.sample(list(vocab_dict.keys()), 10)
selected_words = [word.split()[0].lower() for word in selected_words]

# --- Make Grid ---
grid_size = 15
grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

def place_word(grid, word, start_row, start_col, direction):
    if direction == 'across':
        if start_col + len(word) > grid_size:
            return False
        for i in range(len(word)):
            if grid[start_row][start_col + i] not in ('', word[i]):
                return False
        for i in range(len(word)):
            grid[start_row][start_col + i] = word[i]
        return True
    else:
        if start_row + len(word) > grid_size:
            return False
        for i in range(len(word)):
            if grid[start_row + i][start_col] not in ('', word[i]):
                return False
        for i in range(len(word)):
            grid[start_row + i][start_col] = word[i]
        return True

directions = ['across', 'down']
placed_words = []
for word in selected_words:
    placed = False
    for _ in range(100):
        direction = random.choice(directions)
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - 1)
        if place_word(grid, word, row, col, direction):
            placed_words.append((word, direction, row, col))
            placed = True
            break

for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == '':
            grid[i][j] = chr(random.randint(65, 90))

# --- Plot Puzzle ---
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xticks(np.arange(grid_size + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(grid_size + 1) - 0.5, minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
ax.tick_params(which='major', bottom=False, left=False, labelbottom=False, labelleft=False)

grid_array = np.array(grid)
for i in range(grid_size):
    for j in range(grid_size):
        ax.text(j, i, grid_array[i, j], ha='center', va='center', fontsize=12, fontweight='bold')

ax.set_xlim(-0.5, grid_size - 0.5)
ax.set_ylim(grid_size - 0.5, -0.5)
plt.title("🔤 Word Puzzle: Find the Vocabulary!", fontsize=16)
plt.tight_layout()

# --- Streamlit App Layout ---
st.set_page_config(page_title="Word Puzzle", layout="wide")
st.title("🧩 Word Puzzle Quiz")
st.subheader("Find the hidden vocabulary words in the grid below!")

# Convert Matplotlib figure to PNG
buf = io.BytesIO()
fig.savefig(buf, format="png")
buf.seek(0)
image = Image.open(buf)
st.image(image, caption="Can you find all 10 words?", use_column_width=True)

# Show word list
st.markdown("### 🔍 Words to Find")
for word_info in placed_words:
    st.markdown(f"- **{word_info[0].upper()}**")

# Toggle answer key
if st.checkbox("Show Answer Key (for Teachers)"):
    st.markdown("### 🧩 Answer Key")
    for word, direction, row, col in placed_words:
        st.write(f"**{word.upper()}** → {direction.upper()} at row {row + 1}, column {col + 1}")
