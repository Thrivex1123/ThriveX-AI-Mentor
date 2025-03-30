# 🚀 ThriveX AI Mentor
# An AI-powered coach that listens, understands your emotion, and offers real-time support.

import streamlit as st
import openai
import speech_recognition as sr
import os
portaudio19-dev
python3-distutils
# Set Streamlit page config
st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")

# Secret key config
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- HEADER ---
st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# --- MICROPHONE INPUT ---
st.subheader("🎙️ Step 1: Speak into the mic below")

# Audio recording placeholder
r = sr.Recognizer()
audio_text = ""

with st.form("mic_form"):
    record_button = st.form_submit_button("🎤 Record Now")
    if record_button:
        try:
            with sr.Microphone() as source:
                st.info("Listening... please speak clearly")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                audio_text = r.recognize_google(audio)
                st.success(f"🗣️ You said: {audio_text}")
        except Exception as e:
            st.error(f"❌ Could not process audio: {e}")

# --- AI RESPONSE ---
if audio_text:
    st.subheader("💬 Step 2: AI Coaching Response")
    with st.spinner("Thinking..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a motivational mindset coach."},
                    {"role": "user", "content": audio_text}
                ]
            )
            st.markdown(f"🤖 AI: {response.choices[0].message.content}")
        except Exception as e:
            st.error(f"⚠️ Error communicating with AI: {e}")

