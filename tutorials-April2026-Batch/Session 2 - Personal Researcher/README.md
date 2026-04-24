# Personal Researcher Agent 🧠🎙️

This agent automates the entire research process: finding sources, scraping content, analyzing insights with AI, and narrating the results in a premium voice.

## Features
- **🌐 Web Discovery:** Searches the live web for the most relevant information.
- **✂️ Smart Scraping:** Extracts clean text from websites using BeautifulSoup.
- **♊ Gemini Analysis:** Uses Google's Gemini 1.5 Flash to synthesize findings.
- **🗣️ ElevenLabs Voice:** Converts the research report into a natural-sounding audio update.
- **💎 Premium CLI:** Beautiful progress indicators and formatted results.

## Setup
1. **API Keys:**
   - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
   - Get an ElevenLabs API key from [ElevenLabs](https://elevenlabs.io/).
2. **Environment:**
   - Rename `.env.example` to `.env`.
   - Add your keys to the `.env` file.
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script and enter any topic you want to research:
```bash
python personal_researcher.py
```

## How it works (PFAS Framework)
1. **Problem:** You define the research topic.
2. **Find:** The agent searches Google for top sources.
3. **Analyze:** Gemini processes the scraped text and highlights key insights.
4. **Scrape:** Data is extracted and cleaned automatically.
5. **Speech:** The final summary is narrated as a `.mp3` file.
