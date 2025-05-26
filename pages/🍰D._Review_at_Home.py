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



# Define the crossword words and layout
puzzle_words = {
    1: {"word": "major", "clue": "주요한", "direction": "down", "row": 0, "col": 0},
    2: {"word": "genius", "clue": "천재", "direction": "across", "row": 0, "col": 2},
    3: {"word": "incident", "clue": "사건", "direction": "across", "row": 0, "col": 5},
    4: {"word": "viral", "clue": "바이럴", "direction": "down", "row": 1, "col": 4},
    5: {"word": "portrait", "clue": "초상화", "direction": "across", "row": 4, "col": 0},
    6: {"word": "fake", "clue": "가짜의", "direction": "across", "row": 6, "col": 2},
    7: {"word": "path", "clue": "길", "direction": "across", "row": 8, "col": 1},
}

grid_size = 12
grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
cell_ids = [["" for _ in range(grid_size)] for _ in range(grid_size)]
clue_numbers = [["" for _ in range(grid_size)] for _ in range(grid_size)]

# Fill grid and record positions
for number, data in puzzle_words.items():
    word = data["word"].upper()
    row, col = data["row"], data["col"]
    direction = data["direction"]
    for i, letter in enumerate(word):
        r, c = (row, col + i) if direction == "across" else (row + i, col)
        grid[r][c] = letter
        cell_ids[r][c] = f"{number}_{i}"
    clue_numbers[row][col] = str(number)

# Streamlit layout
st.set_page_config(page_title="Crossword Puzzle", layout="centered")
st.title("🧩 Crossword Puzzle")
st.caption("Enter English words based on the Korean clues.")

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Draw the puzzle grid
for i in range(grid_size):
    cols = st.columns(grid_size)
    for j in range(grid_size):
        cell_id = cell_ids[i][j]
        if cell_id:
            with cols[j]:
                st.text_input(
                    label=clue_numbers[i][j] if clue_numbers[i][j] else " ",
                    key=cell_id,
                    max_chars=1,
                    label_visibility="visible" if clue_numbers[i][j] else "hidden",
                )
                st.session_state.answers[cell_id] = st.session_state.get(cell_id, "")
        else:
            cols[j].markdown(" ")

# Display clues
st.markdown("### 📌 Clues")
st.markdown("#### Across:")
for number, data in puzzle_words.items():
    if data["direction"] == "across":
        st.write(f"**{number}.** {data['clue']}")

st.markdown("#### Down:")
for number, data in puzzle_words.items():
    if data["direction"] == "down":
        st.write(f"**{number}.** {data['clue']}")

# Answer checking logic
if st.button("Check Answers"):
    correct = 0
    total = 0
    for number, data in puzzle_words.items():
        word = data["word"].upper()
        row, col = data["row"], data["col"]
        direction = data["direction"]
        user_word = ""
        for i in range(len(word)):
            r, c = (row, col + i) if direction == "across" else (row + i, col)
            cell_id = cell_ids[r][c]
            user_input = st.session_state.answers.get(cell_id, "").upper()
            user_word += user_input
        total += 1
        if user_word == word:
            correct += 1
    st.success(f"✅ {correct} out of {total} correct!")
