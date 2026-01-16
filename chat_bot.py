import streamlit as st
import requests

# ==============================
# 🔐 API KEY (FROM SECRETS)
# ==============================
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

API_URL = "https://api.together.xyz/v1/chat/completions"

# ==============================
# 🧠 SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 🎨 UI
# ==============================
st.title("💬 Together AI Chat")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your mess_
