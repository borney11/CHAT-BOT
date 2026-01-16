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

prompt = st.chat_input("Type your message...")

# ==============================
# 🚀 CHAT LOGIC
# ==============================
if prompt:
    # User message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Llama-3-8b-Instruct",
        "messages": st.session_state.messages,
        "max_tokens": 256,
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"API Error {response.status_code}")
        st.code(response.text)
        st.stop()

    data = response.json()

    if "choices" not in data:
        st.error("Unexpected API response")
        st.json(data)
        st.stop()

    reply = data["choices"][0]["message"]["content"]

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
