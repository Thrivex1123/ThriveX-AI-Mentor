import streamlit as st
import openai
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import queue
import tempfile
import os
import random

DAILY_AFFIRMATIONS = [
    "You are capable of amazing things.",
    "Today is a fresh start.",
    "You have the power to create change.",
    "You are strong, resilient, and brave.",
    "Every step you take matters."
]

def get_daily_affirmation():
    return random.choice(DAILY_AFFIRMATIONS)

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Emotion detector (mock)
def analyze_emotion(text):
    emotions = ["Calm", "Happy", "Frustrated", "Stressed", "Excited"]
    return np.random.choice(emotions)

# GPT-4 Coach
def ai_mentor_response(user_input, emotion):
    prompt = f"You are an AI mentor helping someone who is feeling {emotion}. Provide motivational and actionable advice for this concern: {user_input}"
    try:
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

# Audio Recorder Class
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recorded_frames = []

    def recv(self, frame):
        self.recorded_frames.append(frame.to_ndarray())
        return frame

# UI
st.title("🚀 ThriveX AI Mentor")
st.write("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

st.subheader("🎙️ Step 1: Speak into the mic below")
ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

# Step 2: Transcribe on button click
if ctx.state.playing and ctx.audio_processor and st.button("✅ Done Recording & Analyze"):
    if ctx.audio_processor.recorded_frames:
        with st.spinner("🎧 Processing your audio..."):
            # Save recorded audio
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio_data = b"".join([frame.tobytes() for frame in ctx.audio_processor.recorded_frames])
            temp_audio.write(audio_data)
            temp_audio.flush()
            audio_path = temp_audio.name

            # Transcribe
            try:
                with open(audio_path, "rb") as f:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f
                    ).text
                st.write(f"🗣️ You said: {transcription}")

                # Emotion
                emotion = analyze_emotion(transcription)
                st.write(f"🧠 Detected Emotion: {emotion}")

                # AI Coach
                reply = ai_mentor_response(transcription, emotion)
                st.write(f"💡 AI Mentor: {reply}")

            except Exception as e:
                st.error(f"Transcription error: {e}")
    else:
        st.warning("🎙️ Please record something first.")
