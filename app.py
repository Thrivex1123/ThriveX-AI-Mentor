import streamlit as st
import openai
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import queue
import tempfile
import os

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
            # Save recortemp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav_

