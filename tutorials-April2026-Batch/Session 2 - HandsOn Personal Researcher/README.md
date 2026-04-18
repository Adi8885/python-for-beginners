# 🤖 Personal Researcher Agent

A multi-modal AI agent that takes a research topic, scrapes the web for data, summarizes it using Gemini AI, and speaks the results using ElevenLabs.

## 🚀 Features
- **Web Scraping**: Uses `BeautifulSoup` and `requests` to fetch data from Wikipedia.
- **AI Analysis**: Uses Google's `Gemini 1.5 Flash` to summarize raw data into an engaging script.
- **Voice Synthesis**: Uses `ElevenLabs` for high-quality, human-like voice output.

## 🛠️ Prerequisites
- Python 3.9 or higher
- [Google Gemini API Key](https://aistudio.google.com/)
- [ElevenLabs API Key](https://elevenlabs.io/)

## 📦 Installation
1. Navigate to the project directory:
   ```bash
   cd "Session 2 - HandsOn Personal Researcher"
   ```

2. Install the required dependencies:
   ```bash
   pip install beautifulsoup4 requests google-generativeai elevenlabs python-dotenv streamlit
   ```

3. Configure your API Keys:
   - Open the `.env` file.
   - Replace `your_gemini_api_key_here` with your Google Gemini API key.
   - Replace `your_elevenlabs_api_key_here` with your ElevenLabs API key.

## 🏃 How to Run

### Option A: Modern Web UI (Recommended)
Run the Streamlit application:
```bash
streamlit run app.py
```

### Option B: Command Line (Simple)
Run the basic Python script:
```bash
python researcher.py
```

1. Enter a topic when prompted (e.g., "Artificial Intelligence", "Mars Exploration").
2. The agent will scrape Wikipedia, generate a summary, and save the voice output as `research_result.mp3`.

## 📁 Project Structure
- `app.py`: The modern Streamlit web interface.
- `researcher.py`: The basic command-line script.
- `.env`: Environment variables for API keys.
- `README.md`: Documentation.
