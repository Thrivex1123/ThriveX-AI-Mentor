import streamlit as st
import openai

# 🌟 Page Setup
st.set_page_config(page_title="ThriveX AI Mentor", layout="centered")
st.title("🚀 ThriveX AI Mentor")
st.markdown("An AI-powered coach that listens, understands your emotions, and offers real-time support with empathy.")

# 🔐 OpenAI Key Setup
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sk-your-key-here"

# 🎤 Input Section
st.subheader("🎙️ Step 1: Speak or Type Your Heart")

audio_text = ""

# 📁 Audio Upload
uploaded_audio = st.file_uploader("📁 Upload a short voice note (.wav)", type=["wav"])
if uploaded_audio:
    with st.spinner("✨ Listening closely..."):
        try:
            transcript = openai.Audio.transcribe("whisper-1", uploaded_audio)
            audio_text = transcript["text"]
            st.success(f"🗣️ You said: {audio_text}")
        except Exception as e:
            st.error(f"❌ Audio issue: {e}")

# ✍️ Text Input
typed_input = st.text_input("✍️ Or type how you’re feeling right now")
if typed_input:
    audio_text = typed_input

# 💬 AI Response
if audio_text:
    st.subheader("💬 ThriveX Coaching Response")
    with st.spinner("🤖 Thinking with heart..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are ThriveX, an emotionally intelligent and human-like AI mentor. "
                            "You speak like a kind friend who truly listens. "
                            "You respond to emotions with warmth, connection, and gentle encouragement. "
                            "Be natural, heartfelt, and supportive. Avoid robotic or clinical responses. "
                            "When someone is down, lift them up. When they’re excited, celebrate with them. Be there."
                        )
                    },
                    {
                        "role": "user",
                        "content": audio_text
                    }
                ]
            )
            ai_message = response.choices[0].message.content
            st.markdown(f"🤖 **ThriveX says:**\n\n{ai_message}")
        except Exception as e:
            st.error(f"⚠️ Error from AI: {e}")

# 📅 Schedule Button
st.markdown("---")
st.subheader("📬 Need a real human too?")
st.markdown("You're never alone. If you ever want to connect personally, I'm here.")

if st.button("📅 Schedule a time with me"):
    st.markdown("[🗓️ Click here to book a session](https://calendly.com/your-link-here) 💙")

