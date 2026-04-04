import streamlit as st
import urllib.parse

WHATSAPP_NUMBER = "917395944527"

st.set_page_config(page_title="Durga Psychiatric Centre", page_icon="🧠")

st.title("🧠 Durga Psychiatric Centre")
st.write("Confidential Mental Health Support")

st.markdown("---")

# FORM
name = st.text_input("Name")
phone = st.text_input("Phone Number")
issue = st.selectbox("Concern", ["Stress", "Anxiety", "Depression", "Relationship", "Addiction", "Other"])

if st.button("Continue to WhatsApp"):

    if not name or not phone:
        st.error("Please fill all details")
    else:
        message = f"Hello, I would like to book a consultation.\n\nName: {name}\nPhone: {phone}\nConcern: {issue}"

        encoded = urllib.parse.quote(message)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

        st.success("Click below to continue")
        st.link_button("👉 Open WhatsApp", wa_link)