import streamlit as st
import openai
import numpy as np
from datetime import datetime

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Analyze Emotion (Mocked for now)
def analyze_emotion(text):
    emotions = ["Calm", "Happy", "Frustrated", "Stressed", "Excited"]
    return np.random.choice(emotions)

# Whisper Transcription from uploaded file
def transcribe_audio_file(audio_file):
    try:
        with st.spinner("🔍 Transcribing audio with Whisper..."):
            response = openai.Audio.transcribe("whisper-1", audio_file)
            return response['text']
    except Exception as e:
        return f"❌ Error: {str(e)}"

# AI Mentor Response
def ai_mentor_response(user_input, emotion):
    prompt = f"You are an AI mentor helping someone who is feeling {emotion}. Provide motivational and actionable advice for this concern: {user_input}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive and motivational AI life coach."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error generating AI response: {str(e)}"

# Streamlit UI
st.title("🚀 ThriveX AI Mentor")
st.write("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# Upload Section
audio_file = st.file_uploader("🎙️ Upload a voice recording (MP3/WAV)", type=["mp3", "wav"])

if audio_file:
    st.audio(audio_file, format="audio/wav")
    transcribed_text = transcribe_audio_file(audio_file)
    st.write(f"🗣️ You said: {transcribed_text}")
    
    if transcribed_text:
        emotion = analyze_emotion(transcribed_text)
        st.write(f"🧠 Detected Emotion: {emotion}")
        
        mentor_reply = ai_mentor_response(transcribed_text, emotion)
        st.write(f"💡 AI Mentor: {mentor_reply}")
