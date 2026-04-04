import streamlit as st
import urllib.parse
import google.generativeai as genai

WHATSAPP_NUMBER = "917395944527"
GEMINI_API_KEY = "AIzaSyC_3bp0o5I46PGNl_cYer4A5o-kEZVKOx0"

genai.configure(api_key=GEMINI_API_KEY)

# Try model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    model = None

st.set_page_config(page_title="Durga Psychiatric Centre")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ---------- CHAT ----------
def fallback_reply(text):
    text = text.lower()
    if "angry" in text:
        return "I understand you're feeling angry. What triggered it?"
    elif "stress" in text:
        return "Stress can be overwhelming. Is it work or personal life?"
    elif "anxiety" in text:
        return "Anxiety can feel intense. When do you feel it most?"
    elif "depression" in text:
        return "I'm sorry you're feeling this way. How long has this been happening?"
    return "I'm here to listen. Can you tell me more?"

def get_ai_reply(user_input):
    if model is None:
        return fallback_reply(user_input)

    try:
        prompt = f"""
You are a compassionate mental health assistant.
Be empathetic, short, and ask follow-up questions.

User: {user_input}
"""
        response = model.generate_content(prompt)
        return response.text
    except:
        return fallback_reply(user_input)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submit = st.form_submit_button("Send")

if submit and user_input:
    st.session_state.messages.append(("You", user_input))
    reply = get_ai_reply(user_input)
    st.session_state.messages.append(("Assistant", reply))
    st.rerun()

for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ---------- FORM ----------
st.markdown("---")
st.subheader("Book a Consultation")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox("Concern", ["Stress","Anxiety","Depression","Other"])

message = f"""Hello, I need consultation.

Name: {name}
Phone: {phone}
Concern: {issue}
"""

wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(message)}"

st.link_button("Open WhatsApp", wa_link)

st.caption("Your information is confidential.")