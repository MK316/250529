import matplotlib.pyplot as plt
import random

# ✅ Define your vocabulary here
word_pairs = [
    ("genius", "천재적인"),
    ("incident", "사건"),
    ("path", "길"),
    ("viral", "입소문 난"),
    ("fake", "가짜의"),
]

# 🔀 Shuffle the left and right sides separately
left_words = [pair[0] for pair in word_pairs]
right_words = [pair[1] for pair in word_pairs]
random.shuffle(left_words)
random.shuffle(right_words)

# 🔁 Build a map of correct connections
pair_map = {eng: kor for eng, kor in word_pairs}
connections = [(i, right_words.index(pair_map[word])) for i, word in enumerate(left_words)]

# 🎨 Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, len(word_pairs) + 1)
ax.axis('off')

# ✏️ Draw boxes and text
for i, word in enumerate(left_words):
    ax.text(1, len(word_pairs) - i, word, va='center', ha='left', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
for j, meaning in enumerate(right_words):
    ax.text(9, len(word_pairs) - j, meaning, va='center', ha='right', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="mistyrose"))

# 🔗 Draw dashed lines between matched pairs
for i, j in connections:
    ax.plot([2.5, 7.5], [len(word_pairs)-i, len(word_pairs)-j], color='gray', linestyle='--')

plt.title("🧩 Match the English Words to Their Korean Meanings", fontsize=14)
plt.tight_layout()
plt.show()
