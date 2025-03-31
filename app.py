import streamlit as st
import openai
import speech_recognition as sr
import os

# Optional voice playback (local only)
try:
    from gtts import gTTS
    import tempfile
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")

# --- OPENAI SECRET KEY ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- SESSION STATE FOR HISTORY ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- HEADER ---
st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# --- MICROPHONE INPUT ---
st.subheader("🎙️ Step 1: Speak into the mic below")

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
        {
            "role": "system",
            "content": (
                "You are a compassionate and emotionally intelligent AI coach. "
                "First analyze the user's message for emotional tone (e.g., stress, sadness, motivation, excitement), "
                "then respond with empathy and tailored advice. Keep it uplifting."
            )
        },
        {
            "role": "user",
            "content": audio_text
        }
    ]
)

            ai_message = response.choices[0].message.content
            st.markdown(f"🤖 AI: {ai_message}")

            # Save to history
            st.session_state.history.append(("🗣️ You", audio_text))
            st.session_state.history.append(("🤖 AI", ai_message))

            # Optional: Speak AI response (for local app)
            if pygame_available and st.checkbox("🔊 Read response out loud (local only)"):
                def speak(text):
                    tts = gTTS(text)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        pygame.mixer.init()
                        pygame.mixer.music.load(fp.name)
                        pygame.mixer.music.play()

                speak(ai_message)

        except Exception as e:
            st.error(f"⚠️ Error communicating with AI: {e}")

# --- CHAT HISTORY ---
if st.session_state.history:
    st.subheader("📝 Conversation History")
    for speaker, text in st.session_state.history:
        st.markdown(f"**{speaker}:** {text}")

# --- RETRY BUTTON ---
if st.button("🔁 Try Again"):
    st.experimental_rerun()
