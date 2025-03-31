import streamlit as st
import openai
import speech_recognition as sr
import tempfile

# Streamlit config
st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")
st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotion, and offers real-time support.")

# API key
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-openai-key-here"

# Mic input with Whisper
r = sr.Recognizer()
audio_text = ""

with st.form("mic_form"):
    record_button = st.form_submit_button("🎤 Record Now")
    if record_button:
        try:
            with sr.Microphone() as source:
                st.info("🎧 Listening... please speak clearly")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    wav_data = audio.get_wav_data()
                    temp_audio_file.write(wav_data)
                    temp_audio_path = temp_audio_file.name

            with open(temp_audio_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                audio_text = transcript["text"]
                st.success(f"🗣️ You said: {audio_text}")

        except Exception as e:
            st.error(f"❌ Could not process audio: {e}")

# AI Response
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
