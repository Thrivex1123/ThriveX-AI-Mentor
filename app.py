import streamlit as st
import openai
import speech_recognition as sr
import tempfile

st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")
st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# OpenAI key: put in secrets.toml or paste here
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sk-your-key-here"

r = sr.Recognizer()
st.subheader("🎙️ Step 1: Speak or Type")

audio_text = ""

# Upload audio fallback
uploaded_audio = st.file_uploader("📁 Upload a short audio file (.wav)", type=["wav"])
if uploaded_audio:
    with st.spinner("Transcribing audio..."):
        try:
            transcript = openai.Audio.transcribe("whisper-1", uploaded_audio)
            audio_text = transcript["text"]
            st.success(f"🗣️ You said: {audio_text}")
        except Exception as e:
            st.error(f"❌ Could not process audio: {e}")

# Text input fallback
typed_input = st.text_input("✍️ Or type your message here")
if typed_input:
    audio_text = typed_input

if audio_text:
    st.subheader("💬 AI Coaching Response")
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
        except Exception as e:
            st.error(f"⚠️ Error from OpenAI: {e}")
