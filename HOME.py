import streamlit as st

st.markdown("### 🐣 1학년 2반 English Classroom")
st.caption("Applications are prepared for the class on May 29.")

# Two-column layout for images
col1, col2 = st.columns(2)

with col1:
    url1 = "https://github.com/MK316/250529/raw/main/images/bg01-rose.jpg"
    st.image(url1, caption="Grammar makes meaning clear.", use_container_width=True)

with col2:
    url2 = "https://github.com/MK316/250529/raw/main/images/0529qr.jpg"
    st.image(url2, caption="📲 250529.streamlit.app", width=200)


