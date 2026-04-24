import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from google import genai
from elevenlabs.client import ElevenLabs
import wikipedia
from dotenv import load_dotenv
import time

# Page Configuration
st.set_page_config(
    page_title="AI Personal Researcher",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Functions
def setup_apis():
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not gemini_key or not eleven_key:
        st.error("API keys missing! Please update your .env file.")
        return None, None
    
    client = genai.Client(api_key=gemini_key)
    eleven_client = ElevenLabs(api_key=eleven_key)
    return client, eleven_client

def scrape_content(topic):
    with st.status(f"🔍 Searching Wikipedia for '{topic}'...", expanded=False) as status:
        try:
            # 1. Search for the best matches
            search_results = wikipedia.search(topic)
            if not search_results:
                st.error(f"Topic '{topic}' not found on Wikipedia.")
                return None
            
            # 2. Get the content of the top match
            # Using search_results[0] is more accurate than direct page()
            page = wikipedia.page(search_results[0], auto_suggest=False)
            status.update(label=f"Found: {page.title}", state="complete", expanded=False)
            return f"--- Source: {page.url} ---\n{page.content[:15000]}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple options, take the first one
            page = wikipedia.page(e.options[0], auto_suggest=False)
            status.update(label=f"Handled disambiguation: {page.title}", state="complete", expanded=False)
            return f"--- Source: {page.url} ---\n{page.content[:15000]}"
        except Exception as e:
            st.error(f"Wikipedia Error: {e}")
            return None

def analyze_with_gemini(client, research_data, topic):
    prompt = f"""
    You are a professional research analyst. 
    Below is raw data scraped from the web regarding the topic: '{topic}'.
    
    RESEARCH DATA:
    {research_data}
    
    TASK:
    1. Summarize the key findings in 3-4 concise points.
    2. Provide a 'Final Verdict' or 'Takeaway'.
    3. Keep the summary engaging and conversational.
    4. Limit the total response to about 150 words.
    """
    
    with st.spinner("🧠 Analyzing insights with Gemini..."):
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text

def speak_results(eleven_client, text):
    with st.spinner("🗣️ Synthesizing custom voice..."):
        try:
            # Update to ElevenLabs v2.43.0+ API
            # Switched to 'Alice' (Free Pre-made Voice)
            audio = eleven_client.text_to_speech.convert(
                text=text,
                voice_id="Xb7hH8MSUJpSbSDYk0k2", # Alice Voice ID
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            
            output_file = "research_summary.mp3"
            with open(output_file, "wb") as f:
                # The response object in new SDK is a generator for the audio data
                for chunk in audio:
                    f.write(chunk)
            
            return output_file
        except Exception as e:
            st.error(f"Voice Error: {e}")
            return None

# UI Header
st.title("🚀 Personal Researcher Agent")
st.markdown("*Automated Research & Voice Synthesis*")

# API Setup
client, eleven_client = setup_apis()

if client:
    topic = st.text_input("What would you like to research today?", placeholder="e.g. Future of Quantum Computing")
    
    if st.button("Start Research"):
        if not topic:
            st.warning("Please enter a topic!")
        else:
            # 1. Scrape
            data = scrape_content(topic)
            
            if data:
                # 2. Analyze
                summary = analyze_with_gemini(client, data, topic)
                
                st.subheader("📋 Research Summary")
                st.markdown(summary)
                
                # 3. Speak
                audio_file = speak_results(eleven_client, summary)
                
                if audio_file:
                    st.subheader("🎧 Voice Report")
                    with open(audio_file, "rb") as f:
                        st.audio(f.read(), format="audio/mp3")
                    st.success("Research complete! You can listen to the report above.")
                    st.download_button("Download Report Audio", data=open(audio_file, "rb"), file_name="research_report.mp3")
            else:
                st.error("No data found for this topic.")

# Sidebar info
st.sidebar.title("About")
st.sidebar.info("""
This tool uses the **PFAS Framework**:
1. **Problem:** Define topic.
2. **Find:** Search the web.
3. **Analyze:** Gemini 1.5 Flash.
4. **Scrape:** BeautifulSoup.
5. **Speech:** ElevenLabs.
""")
