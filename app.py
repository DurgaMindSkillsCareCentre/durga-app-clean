import streamlit as st
import urllib.parse
import google.generativeai as genai

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"

#  DIRECT API KEY (as requested)
GEMINI_API_KEY = "AIzaSyDxCc-S2vj9vBKZnUSLd-O45rij0_Sz0lQ"

genai.configure(api_key=GEMINI_API_KEY)

#  Use stable model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.set_page_config(page_title="Durga Psychiatric Centre", page_icon="")

# ========= SESSION =========
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========= HEADER =========
st.title(" Durga Psychiatric Centre")
st.write("Confidential AI Mental Health Assistant")

st.markdown("---")

# ========= CHAT =========
st.subheader(" Talk to our AI Assistant")

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

    try:
        response = st.session_state.chat.send_message(prompt)
        reply = response.text if hasattr(response, "text") else "I'm here to listen. Can you tell me more?"
    except Exception:
        reply = " AI service temporarily unavailable. Please try again."

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Assistant", reply))

    st.rerun()

# ========= DISPLAY =========
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ========= FORM =========
st.markdown("---")
st.subheader(" Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox(
    "Concern",
    ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"]
)

# ========= WHATSAPP =========
if st.button(" Open WhatsApp"):

    if not name or not phone:
        st.error("Please enter Name and Phone Number")
    else:
        message = f"""Hello, I would like to book a consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

        encoded = urllib.parse.quote(message)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

        st.success("Tap below to open WhatsApp")
        st.link_button(" Open WhatsApp Chat", wa_link)

# ========= FOOTER =========
st.caption("Your information is confidential.")