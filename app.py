 import streamlit as st
import os
import time
import json
from sarvamai import SarvamAI

# ------------------ UI SETUP ------------------
st.set_page_config(page_title="BCA AI Guide", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    .animated-header {
        background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #84fab0, #8fd3f4);
        background-size: 400% 400%;
        animation: gradient 12s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .creator-text {
        text-align: center;
        color: #ff758c;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='animated-header'>BCA Virtual Assistant 🤖</div>", unsafe_allow_html=True)
st.markdown("<div class='creator-text'>Created by Uttam Kashyap , Bipin Yadav</div>", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Settings")

    tone = st.selectbox("Response Style", ["Simple", "Detailed", "Exam Ready"])

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if st.session_state.get("messages"):
        st.download_button(
            "📥 Download Chat",
            data=json.dumps(st.session_state.messages, indent=2),
            file_name="chat_history.json",
            mime="application/json"
        )

# ------------------ API KEY ------------------
api_key = os.environ.get("SARVAM_API_KEY")

if not api_key:
    st.error("⚠️ API Key missing. Please set SARVAM_API_KEY.")
    st.stop()

# ------------------ SESSION MEMORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Limit chat memory
MAX_MESSAGES = 20
if len(st.session_state.messages) > MAX_MESSAGES:
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

# ------------------ DISPLAY CHAT ------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------ QUICK BUTTONS ------------------
st.markdown("### 🚀 Quick Start")

col1, col2, col3 = st.columns(3)

if col1.button("C Programming"):
    st.session_state.messages.append({"role": "user", "content": "C programming basics sikhao"})
    st.rerun()

if col2.button("DBMS"):
    st.session_state.messages.append({"role": "user", "content": "DBMS simple me samjhao"})
    st.rerun()

if col3.button("Career Guide"):
    st.session_state.messages.append({"role": "user", "content": "BCA ke baad kya career options hai?"})
    st.rerun()

# ------------------ AI CONTEXT (HINGLISH) ------------------
BCA_CONTEXT = f"""
Tum ek smart, friendly aur thoda cool "BCA Guide AI" ho.

Style: {tone}

Tone Instructions:
- Hinglish me baat karo (Hindi + English mix)
- Bilkul natural student jaisa feel ho
- Kabhi kabhi thoda fun/sarcastic tone bhi use karo
- Simple language use karo, boring mat bano

Teaching Style:
- Step-by-step samjhao
- Real-life examples do
- Coding examples bhi do
- Beginner ho toh basics se start karo
- Advanced ho toh deep explain karo

Subjects:
1st Year:
- C Programming (loops, pointers, arrays)
- Mathematics
- Digital Electronics

2nd Year:
- Java
- Data Structures
- DBMS

3rd Year:
- Python
- Web Development
- AI/ML basics

Extra Behavior:
- Career guidance bhi do
- Student ko motivate karo
- Kabhi kabhi "Pro Tip:" bhi do

IMPORTANT:
- Har answer Hinglish me hi hona chahiye
- English heavy mat karo
- Friendly teacher + senior jaisa behave karo
"""

# ------------------ CHAT INPUT ------------------
if prompt := st.chat_input("Apna doubt pucho..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:
            with st.spinner("🤖 Soch raha hu..."):

                client = SarvamAI(api_subscription_key=api_key)

                msgs = [{"role": "system", "content": BCA_CONTEXT}]
                msgs.extend(st.session_state.messages)

                response = client.chat.completions(
                    model="sarvam-m",
                    messages=msgs
                )

                reply = response.choices[0].message.content

            # Typing animation
            full_text = ""
            for word in reply.split():
                full_text += word + " "
                placeholder.markdown(full_text)
                time.sleep(0.02)

            # Save response
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception:
            placeholder.error("⚠️ Kuch problem ho gaya, dobara try karo.")
