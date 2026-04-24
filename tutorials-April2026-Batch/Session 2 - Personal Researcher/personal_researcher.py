import os
import requests
from bs4 import BeautifulSoup
from google import genai
from elevenlabs.client import ElevenLabs
import wikipedia
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Initialize Rich Console for premium output
console = Console()

def setup_apis():
    """Load API keys from .env file or environment variables."""
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not gemini_key or not eleven_key:
        console.print("[bold red]Error:[/] API keys missing. Please check your .env file.")
        return None, None
    
    # Configure Gemini with the new GENAI client
    client = genai.Client(api_key=gemini_key)
    
    # Configure ElevenLabs
    eleven_client = ElevenLabs(api_key=eleven_key)
    
    return client, eleven_client

def scrape_content(topic):
    """Search Wikipedia for the topic and extract the content."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Searching Wikipedia for '{topic}'...", total=None)
        try:
            # 1. Search for best matches
            search_results = wikipedia.search(topic)
            if not search_results:
                console.print(f"[bold red]Error:[/] Topic '{topic}' not found on Wikipedia.")
                return None
            
            # 2. Extract content from the top match
            page = wikipedia.page(search_results[0], auto_suggest=False)
            return f"--- Source: {page.url} ---\n{page.content[:15000]}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple options, take the first one
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return f"--- Source: {page.url} ---\n{page.content[:15000]}"
        except Exception as e:
            console.print(f"[bold red]Wikipedia Error:[/] {e}")
            return None

def analyze_with_gemini(client, research_data, topic):
    """Use Gemini to summarize the scraped data."""
    prompt = f"""
    You are a professional research analyst. 
    Below is raw data scraped from the web regarding the topic: '{topic}'.
    
    RESEARCH DATA:
    {research_data}
    
    TASK:
    1. Summarize the key findings in 3-4 concise points.
    2. Provide a 'Final Verdict' or 'Takeaway'.
    3. Keep the summary engaging and conversational, as it will be read aloud.
    4. Limit the total response to about 150-200 words.
    """
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]Analyzing insights with Gemini..."),
        transient=True,
    ) as progress:
        progress.add_task(description="Analyzing...", total=None)
        # Using the new google-genai client
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text

def speak_results(eleven_client, text):
    """Convert summarized text to speech using ElevenLabs."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]Synthesizing custom voice..."),
        transient=True,
    ) as progress:
        progress.add_task(description="Speaking...", total=None)
        try:
            # Update to ElevenLabs v2.43.0+ API
            # Switched to 'Alice' (Free Pre-made Voice)
            audio = eleven_client.text_to_speech.convert(
                text=text,
                voice_id="Xb7hH8MSUJpSbSDYk0k2", # Alice Voice ID
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            
            # Save to file
            output_file = "research_summary.mp3"
            with open(output_file, "wb") as f:
                # The response object in new SDK is a generator for the audio data
                for chunk in audio:
                    f.write(chunk)
            
            return output_file
        except Exception as e:
            console.print(f"[bold red]Voice Error:[/] {e}")
            return None

def main():
    console.print(Panel.fit(
        "[bold cyan]🚀 Personal Researcher Agent[/]\n[italic]Powered by Gemini & ElevenLabs[/]",
        border_style="magenta"
    ))
    
    client, eleven_client = setup_apis()
    if not client:
        return

    topic = console.input("[bold yellow]Enter your research topic:[/] ")
    
    if not topic:
        console.print("[red]Topic cannot be empty![/]")
        return

    # 1. Scrape
    data = scrape_content(topic)
    if not data:
        console.print("[red]No data found for this topic.[/]")
        return
    
    # 2. Analyze
    summary = analyze_with_gemini(client, data, topic)
    
    console.print(Panel(Markdown(summary), title="Research Summary", border_style="green"))
    
    # 3. Speak
    audio_file = speak_results(eleven_client, summary)
    
    if audio_file:
        console.print(f"[bold green]Success![/] Voice summary saved to [underline]{audio_file}[/]")
        console.print("[italic]You can now play the file to hear your personal researcher's report.[/]")

if __name__ == "__main__":
    main()
