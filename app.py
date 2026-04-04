import streamlit as st
import urllib.parse
import google.generativeai as genai

# ========= CONFIG =========
WHATSAPP_NUMBER = "917395944527"
GEMINI_API_KEY = "AIzaSyC_3bp0o5I46PGNl_cYer4A5o-kEZVKOx0"

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use safest available model
MODEL_NAME = "gemini-1.5-flash"

try:
    model = genai.GenerativeModel(MODEL_NAME)
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

st.set_page_config(page_title="Durga Psychiatric Centre")

# ========= SESSION =========
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history_text" not in st.session_state:
    st.session_state.history_text = ""

# ========= HEADER =========
st.title("Durga Psychiatric Centre")
st.write("AI Mental Health Assistant")

st.markdown("---")

# ========= SMART FALLBACK =========
def fallback_reply(text):
    text = text.lower()

    if "stress" in text:
        return "It sounds like stress is affecting you. Is it more from personal life or work?"
    elif "family" in text:
        return "Family issues can be emotionally heavy. What exactly is troubling you?"
    elif "angry" in text:
        return "I understand anger can build up. What triggered it?"
    elif "anxiety" in text:
        return "Anxiety can feel intense. When do you notice it the most?"
    elif "depression" in text:
        return "I'm sorry you're feeling this way. How long has this been happening?"
    else:
        return "I'm listening. Can you explain a bit more?"

# ========= GEMINI FUNCTION =========
def get_ai_reply(user_input):

    if not GEMINI_AVAILABLE:
        return fallback_reply(user_input)

    try:
        full_prompt = f"""
You are a compassionate mental health assistant.

Rules:
- Be empathetic
- Ask specific follow-up questions
- Avoid repeating same sentence
- Keep responses short (2-3 lines)

Conversation:
{st.session_state.history_text}

User: {user_input}
"""

        response = model.generate_content(full_prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return fallback_reply(user_input)

    except Exception as e:
        return fallback_reply(user_input)

# ========= INPUT =========
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Tell me what you're feeling:")
    submit = st.form_submit_button("Send")

if submit and user_input:

    reply = get_ai_reply(user_input)

    # Save history
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Assistant", reply))

    st.session_state.history_text += f"\nUser: {user_input}\nAssistant: {reply}"

    st.rerun()

# ========= DISPLAY =========
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")

# ========= FORM =========
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