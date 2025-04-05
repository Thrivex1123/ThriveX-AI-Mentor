import streamlit as st
import openai
import speech_recognition as sr
import os
import tempfile

st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# Step 1: File or Text input
st.subheader("🎙️ Step 1: Speak or Type")
audio_file = st.file_uploader("📁 Upload a short audio file (.wav)", type=["wav"])
text_input = st.text_input("✍️ Or type your message here")

# Step 2: Process input
audio_text = ""

if audio_file:
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    with sr.AudioFile(tmp_path) as source:
        audio = r.record(source)
        try:
            audio_text = r.recognize_google(audio)
            st.success(f"🗣️ You said: {audio_text}")
        except Exception as e:
            st.error(f"❌ Could not process audio: {e}")

elif text_input:
    audio_text = text_input

# Step 3: Get AI Response
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
                            "Always respond with empathy, warmth, and encouragement. "
                            "Recognize the user’s emotional state and help them feel heard and safe."
                        )
                    },
                    {"role": "user", "content": audio_text}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(f"🤖 **AI:** {reply}")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Step 4: Calendly
st.markdown("---")
st.markdown("💙 Need to talk to someone real?")
st.markdown("[📅 Book a 1-on-1 session with the ThriveX team](https://calendly.com/your-link)")


