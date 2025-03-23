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

# Mock emotion detector
def analyze_emotion(text):
    emotions = ["Calm", "Happy", "Frustrated", "Stressed", "Excited"]
    return np.random.choice(emotions)

# GPT-4 AI Mentor
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

# Mic audio recorder (webrtc)
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recorded_frames = []
    
    def recv(self, frame):
        self.recorded_frames.append(frame.to_ndarray())
        return frame

# UI
st.title("🚀 ThriveX AI Mentor")
st.write("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

st.subheader("🎙️ Speak into the mic")

ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx.audio_processor and ctx.audio_processor.recorded_frames:
    st.success("✅ Audio captured!")

    # Save audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_data = b"".join([frame.tobytes() for frame in ctx.audio_processor.recorded_frames])
    temp_audio.write(audio_data)
    temp_audio.flush()
    audio_path = temp_audio.name

    st.audio(audio_path)

    try:
        with st.spinner("🔍 Transcribing with Whisper..."):
            with open(audio_path, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                ).text
        st.write(f"🗣️ You said: {transcription}")

        # Emotion + AI
        emotion = analyze_emotion(transcription)
        st.write(f"🧠 Detected Emotion: {emotion}")
        response = ai_mentor_response(transcription, emotion)
        st.write(f"💡 AI Mentor: {response}")

    except Exception as e:
        st.error(f"Transcription error: {e}")

