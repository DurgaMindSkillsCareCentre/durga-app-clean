import streamlit as st
import urllib.parse
import google.generativeai as genai

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"
genai.configure(api_key="AIzaSyDxCc-S2vj9vBKZnUSLd-O45rij0_Sz0lQ")  # 🔴 ADD YOUR KEY

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Durga Psychiatric Centre", page_icon="🧠")

# ========= SESSION =========
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========= HEADER =========
st.title("🧠 Durga Psychiatric Centre")
st.write("Confidential AI Mental Health Assistant")

st.markdown("---")

# ========= CHAT =========
st.subheader("💬 Talk to our AI Assistant")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Tell me what you're feeling:",
        placeholder="Example: I feel stressed due to work pressure"
    )
    submit = st.form_submit_button("Send")

if submit and user_input:

    prompt = f"""
You are a compassionate mental health assistant.

Rules:
- Be empathetic and supportive
- Ask gentle follow-up questions
- Do NOT diagnose or give medical advice
- Keep answers short (2-3 sentences)
- Encourage professional consultation

User: {user_input}
"""

    response = st.session_state.chat.send_message(prompt)
    reply = response.text

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Assistant", reply))

    st.rerun()

# ========= DISPLAY CHAT =========
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ========= CONSULTATION FORM =========
st.markdown("---")
st.subheader("📅 Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox(
    "Concern",
    ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"]
)

# ========= WHATSAPP BUTTON =========
if name and phone:

    message = f"""Hello, I would like to book a consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

    encoded_message = urllib.parse.quote(message)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"

    st.markdown("### 👉 Continue to WhatsApp")
    st.link_button("🚀 Open WhatsApp", wa_link)

else:
    st.info("Please enter Name and Phone Number to proceed")

# ========= FOOTER =========
st.caption("Your information is confidential.")