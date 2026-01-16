# 📦 Imports
import streamlit as st
import requests

# ==============================
# 🔐 CONFIG (DO THIS PROPERLY)
# ==============================

# NEVER hardcode API keys
# Set this in Streamlit Secrets or environment variables
# Streamlit Cloud → App → Settings → Secrets
TOGETHER_API_KEY = st.secrets.get("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    st.error("TOGETHER_API_KEY not found in secrets.")
    st.stop()

API_URL = "https://api.together.xyz/v1/chat/completions"

# ==============================
# 🧠 Session Memory
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 🎨 UI
# ==============================

st.title("Chat with Me")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

# ==============================
# 🚀 On User Message
# ==============================

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # ==============================
    # 📡 API Request
    # ==============================

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Llama-3-8b-Instruct",
        "messages": st.session_state.messages,
        "max_tokens": 200,
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # ==============================
    # ❌ HARD ERROR HANDLING
    # ==============================

    if response.status_code != 200:
        st.error(f"API Error {response.status_code}")
        st.code(response.text)
        st.stop()

    response_json = response.json()

    if "choices" not in response_json:
        st.error("Unexpected API response format")
        st.json(response_json)
        st.stop()

    # ==============================
    # ✅ Extract Reply (SAFE)
    # ==============================

    reply = response_json["choices"][0]["message"]["content"]

    # Show assistant reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    # ==============================
    # 📝 Save chat locally
    # ==============================

    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {prompt}\n")
        f.write(f"Assistant: {reply}\n\n")
