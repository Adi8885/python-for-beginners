import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Logic Functions ---
def scrape_wikipedia(topic):
    search_query = topic.strip().replace(" ", "_").title()
    url = f"https://en.wikipedia.org/wiki/{search_query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find(id="mw-content-text")
        paragraphs = content_div.find_all('p') if content_div else []
        full_text = []
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:
                full_text.append(text)
            if len(full_text) >= 5: break
        return "\n".join(full_text) if full_text else None
    except:
        return None

def analyze_findings(raw_data, topic):
    model = genai.GenerativeModel('gemini-flash-latest')
    prompt = f"Summarize this info about '{topic}' into a 100-word engaging script: {raw_data}"
    response = model.generate_content(prompt)
    return response.text

def speak_results(text):
    """Uses gTTS for completely free voice synthesis"""
    tts = gTTS(text=text, lang='en', slow=False)
    output_file = "research_result.mp3"
    tts.save(output_file)
    return output_file

# --- Streamlit UI ---
st.set_page_config(page_title="Free AI Researcher", page_icon="🤖")

st.title("🤖 AI Personal Researcher (Free Version)")
st.write("Discover and Listen to any topic without API limits.")

if not GEMINI_API_KEY:
    st.warning("⚠️ Gemini API Key missing in .env file!")

topic = st.text_input("Enter a research topic:", placeholder="e.g. Solar Energy")

if st.button("Start Research"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        with st.status("Analyzing...", expanded=True) as status:
            raw_data = scrape_wikipedia(topic)
            if not raw_data:
                st.error("Could not find info on Wikipedia.")
            else:
                summary = analyze_findings(raw_data, topic)
                audio_file = speak_results(summary)
                
                status.update(label="Complete!", state="complete")
                st.subheader("📝 Summary")
                st.info(summary)
                
                st.subheader("🔊 Audio")
                with open(audio_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
