import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

class PersonalResearcher:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')
        print("🤖 Personal Researcher Initialized (Free Voice Mode)...")

    def scrape_wikipedia(self, topic):
        search_query = topic.strip().replace(" ", "_").title()
        url = f"https://en.wikipedia.org/wiki/{search_query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return "Error: Topic not found on Wikipedia."
            soup = BeautifulSoup(response.content, 'html.parser')
            content_div = soup.find(id="mw-content-text")
            paragraphs = content_div.find_all('p') if content_div else []
            text_data = []
            for p in paragraphs:
                txt = p.get_text().strip()
                if len(txt) > 60: text_data.append(txt)
                if len(text_data) >= 5: break
            return "\n".join(text_data) if text_data else "No content found."
        except Exception as e:
            return f"Error: {e}"

    def analyze_findings(self, raw_data, topic):
        prompt = f"Summarize this info about '{topic}' into a 100-word engaging script: {raw_data}"
        response = self.model.generate_content(prompt)
        return response.text

    def speak_results(self, text):
        print("🎙️ Generating free voice (gTTS)...")
        tts = gTTS(text=text, lang='en')
        output_file = "research_result.mp3"
        tts.save(output_file)
        print(f"✅ Saved to: {output_file}")
        return output_file

    def run(self, topic):
        raw_data = self.scrape_wikipedia(topic)
        summary = self.analyze_findings(raw_data, topic)
        print(f"\n📝 SUMMARY:\n{summary}\n")
        self.speak_results(summary)

if __name__ == "__main__":
    researcher = PersonalResearcher()
    topic = input("Enter a research topic: ")
    if topic: researcher.run(topic)
