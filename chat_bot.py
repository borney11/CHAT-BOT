import streamlit as st
import requests

# ==============================
# 🔐 OPENROUTER API KEY
# ==============================
# WARNING: Hardcoded for simplicity (NOT for production)
OPENROUTER_API_KEY = "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"

# ==============================
# 🌐 OPENROUTER API URL
# ==============================
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ==============================
# 🧠 SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 🎨 UI
# ==============================
st.title("💬 OpenRouter Chat")

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
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # REQUIRED by OpenRouter
        "X-Title": "Streamlit Chat App",          # REQUIRED by OpenRouter
    }

    payload = {
        # ✅ This model works on OpenRouter for most accounts
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": st.session_state.messages,
        "max_tokens": 256,
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # ==============================
    # ❌ ERROR HANDLING
    # ==============================
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

    # Assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
