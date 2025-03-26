import streamlit as st
import openai
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from textblob import TextBlob
import tempfile
import os
import random
git add runtime.txt
git commit -m "Set Python version for Streamlit compatibility"
git push
# 🎯 DAILY AFFIRMATIONS
DAILY_AFFIRMATIONS = [
    "You are capable of amazing things.",
    "Today is a fresh start.",
    "You have the power to create change.",
    "You are strong, resilient, and brave.",
    "Every step you take matters.",
    "You are growing through what you're going through.",
    "Your potential is limitless.",
]

def get_daily_affirmation():
    return random.choice(DAILY_AFFIRMATIONS)

# 🎧 AUDIO PROCESSOR
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recorded_frames = []

    def recv(self, frame):
        self.recorded_frames.append(frame.to_ndarray())
        return frame

# 💬 EMOTION DETECTOR using TextBlob
def analyze_emotion(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.5:
        return "Excited"
    elif polarity > 0:
        return "Happy"
    elif polarity == 0:
        return "Calm"
    elif polarity > -0.5:
        return "Frustrated"
    else:
        return "Stressed"

# 🤖 AI MENTOR RESPONSE using GPT-4
def ai_mentor_response(user_input, emotion):
    prompt = f"You are an AI mentor helping someone who is feeling {emotion}. Provide motivational and actionable advice for this concern: {user_input}"
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a supportive and motivational AI life coach."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🚀 STREAMLIT APP UI
st.set_page_config(page_title="ThriveX AI Mentor", page_icon="🚀")

st.title("🚀 ThriveX AI Mentor")
st.write("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# 🌞 DAILY AFFIRMATION
if st.button("🌄 Get Today's Affirmation"):
    st.success(f"🌞 Daily Affirmation: *{get_daily_affirmation()}*")

# 🎙️ AUDIO RECORDING
st.subheader("🎤 Step 1: Speak into the mic below")
ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

# 🧠 TRANSCRIBE, EMOTION + GPT ADVICE
if ctx.state.playing and ctx.audio_processor and st.button("✅ Done Recording & Analyze"):
    if ctx.audio_processor.recorded_frames:
        with st.spinner("🎧 Processing your audio..."):
            # Save audio to temporary file
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio_data = b"".join([frame.tobytes() for frame in ctx.audio_processor.recorded_frames])
            temp_audio.write(audio_data)
            temp_audio.flush()
            audio_path = temp_audio.name

            try:
                # Transcribe using OpenAI Whisper
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                with open(audio_path, "rb") as f:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f
                    ).text

                st.write(f"🗣️ You said: `{transcription}`")

                # Detect emotion
                emotion = analyze_emotion(transcription)
                st.write(f"🧠 Detected Emotion: `{emotion}`")

                # Get AI Mentor's response
                reply = ai_mentor_response(transcription, emotion)
                st.write(f"💡 AI Mentor: {reply}")

            except Exception as e:
                st.error(f"❌ Transcription error: {e}")
    else:
        st.warning("🎙️ Please record something first.")
