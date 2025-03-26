import streamlit as st
import openai
import random
from textblob import TextBlob
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
st-gsheets-connection
# ---------- SETTINGS ----------
st.set_page_config(page_title="ThriveX AI Mentor", page_icon="🚀")

# ---------- DAILY AFFIRMATIONS ----------
AFFIRMATIONS = [
    "You are capable of amazing things.",
    "Today is a fresh start.",
    "You have the power to create change.",
    "You are strong, resilient, and brave.",
    "Every step you take matters.",
    "You are growing through what you're going through.",
    "Your potential is limitless.",
]

def get_affirmation():
    return random.choice(AFFIRMATIONS)

# ---------- EMOTION DETECTOR ----------
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

# ---------- AI MENTOR ----------
def get_ai_response(prompt, emotion):
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a supportive and motivational AI life coach."},
                {"role": "user", "content": f"I'm feeling {emotion}. {prompt}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# ---------- GOOGLE SHEETS LOGGING ----------
def log_to_gsheet(data):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gsheets_creds"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("ThriveX Logs").sheet1
        sheet.append_row(data)
    except Exception as e:
        st.error(f"Google Sheets Logging Failed: {e}")

# ---------- UI ----------
st.title("🚀 ThriveX AI Mentor")
st.write("An AI-powered coach that understands how you feel and gives real-time support.")

if st.button("🌞 Show Daily Affirmation"):
    st.success(get_affirmation())

st.subheader("💬 What's on your mind?")
user_input = st.text_area("Type your thoughts or concerns here", height=150)

if st.button("🧠 Analyze & Get Advice"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            emotion = analyze_emotion(user_input)
            response = get_ai_response(user_input, emotion)

            st.write(f"🧠 Detected Emotion: `{emotion}`")
            st.write(f"💡 AI Mentor: {response}")

            # Log to GSheet
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_gsheet([now, user_input, emotion, response])
