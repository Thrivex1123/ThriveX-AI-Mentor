import streamlit as st
import numpy as np
import speech_recognition as sr
import librosa
import tensorflow as tf
import openai
import soundfile as sf
import audioread
from datetime import datetime

# Securely load API Key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Placeholder: Emotion analysis logic from voice
def analyze_emotion_from_voice(audio_text):
    emotions = ["Calm", "Happy", "Frustrated", "Stressed", "Excited"]
    return np.random.choice(emotions)

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

def transcribe_audio():
    with sr.Microphone() as source:
        st.write("🎤 Speak now, ThriveX is listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        st.write("⚠️ API unavailable")
        return ""

# AI Mentor Response using OpenAI GPT
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

# Streamlit UI
st.title("🚀 ThriveX AI Mentor - Voice Emotion Analysis & Coaching")
st.write("An AI-powered mentor that analyzes your voice and emotions, and gives real-time coaching advice.")

# Start Voice Analysis
if st.button("🎙️ Start Voice Analysis & Coaching"):
    user_text = transcribe_audio()
    if user_text:
        detected_emotion = analyze_emotion_from_voice(user_text)
        st.write(f"🧠 AI detected emotion: {detected_emotion}")
        mentor_advice = ai_mentor_response(user_text, detected_emotion)
        st.write(f"💡 AI Mentor: {mentor_advice}")
