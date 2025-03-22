import streamlit as st
import numpy as np
import tensorflow as tf
import openai
import soundfile as sf
from datetime import datetime

# Load OpenAI API Key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Placeholder Emotion Analysis Model
def analyze_emotion_from_voice(audio_text):
    emotions = ["Calm", "Happy", "Frustrated", "Stressed", "Excited"]
    return np.random.choice(emotions)

# Transcribe uploaded audio using OpenAI Whisper API (optional)
def transcribe_audio_file(file_path):
    audio_file = open(file_path, "rb")
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        return f"❌ Transcription error: {str(e)}"

# AI Mentor Response
def ai_mentor_response(user_input, emotion):
    prompt = f"You are an AI mentor helping with personal growth. The user is feeling {emotion}. Provide motivation and actionable advice for their concern: {user_input}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a motivational AI coach."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit App UI
st.title("🚀 ThriveX AI Mentor")
st.write("Upload a short voice recording, and ThriveX will analyze your tone and provide motivational advice.")

audio_file = st.file_uploader("🎙️ Upload your voice (WAV/MP3)", type=["wav", "mp3"])

if audio_file is not None:
    # Save uploaded file temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())

    st.audio("temp_audio.wav")

    st.write("🔍 Transcribing and analyzing...")

    user_text = transcribe_audio_file("temp_audio.wav")
    st.write(f"🗣️ You said: {user_text}")

    if user_text:
        detected_emotion = analyze_emotion_from_voice(user_text)
        st.write(f"🧠 Detected Emotion: {detected_emotion}")

        mentor_reply = ai_mentor_response(user_text, detected_emotion)
        st.write(f"💡 AI Mentor: {mentor_reply}")
