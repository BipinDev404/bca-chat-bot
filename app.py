import streamlit as st
import os
from sarvamai import SarvamAI

# 1. UI aur Vibe Set karna
st.set_page_config(page_title="BCA AI Guide", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    .animated-header { background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #84fab0, #8fd3f4); background-size: 400% 400%; animation: gradient 12s ease infinite; -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-size: 3.2rem; font-weight: 800; margin-bottom: 5px; }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .creator-text { text-align: center; color: #ff758c; font-size: 1.3rem; font-weight: 700; letter-spacing: 2.5px; margin-bottom: 30px; animation: glow 2s ease-in-out infinite alternate; }
    @keyframes glow { from { opacity: 0.7; transform: translateY(0px); } to { opacity: 1; transform: translateY(-2px); } }
    .stChatMessage { border-radius: 18px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='animated-header'>BCA Virtual Assistant 🤖</div>", unsafe_allow_html=True)
st.markdown("<div class='creator-text'>✨ Created by Uttam Kashyap ✨</div>", unsafe_allow_html=True)

# 2. API key lena
api_key = os.environ.get("SARVAM_API_KEY")
if not api_key:
    st.error("⚠️ Error: API Key background se nahi aayi.")
    st.stop()

# 3. YAHAN THA WOH ERROR, AB 100% FIX HO GAYA HAI ✅
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. AI ko BCA ki knowledge dena
BCA_CONTEXT = """
Tum ek "BCA Course Expert" AI ho jise Uttam Kashyap ne banaya hai.
Syllabus Overview:
1st Year: C Programming, Math, Digital Electronics.
2nd Year: Java, DBMS, Data Structures.
3rd Year: Python, Web Dev, AI/ML.
Tumhe DSEU (Delhi Skill and Entrepreneurship University) ke admission aur syllabus ki bhi knowledge hai.
"""

# 5. Chat ka Logic
if prompt := st.chat_input("Doubt pucho (e.g. BCA syllabus?)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Soch raha hu...")
        try:
            client = SarvamAI(api_subscription_key=api_key)
            msgs = [{"role": "system", "content": BCA_CONTEXT}]
            msgs.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            response = client.chat.completions(model="sarvam-m", messages=msgs)
            reply = response.choices[0].message.content
            placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            placeholder.error(f"Error aagaya bhai: {e}")
