import sounddevice as sd
import numpy as np
import requests
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

# --- CONFIG ---
# Change OUTPUT_FORMAT to "markdown" to save as .md file instead of Apple Notes
OUTPUT_FORMAT = "notes"  # options: "notes" or "markdown"

API_KEY = os.getenv("MERCURY_API_KEY")
API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"
SAMPLE_RATE = 16000
CHUNK_SECONDS = 5
DEVICE = 0
SUMMARY_EVERY = 3  # update summary every N chunks

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- OUTPUT SETUP ---
meeting_time = datetime.now().strftime("%Y-%m-%d %H:%M")
note_title = f"LiveBrief {meeting_time}"
transcript_lines = []
current_summary = ""

def get_summary(transcript_so_far):
    payload = {
        "model": "mercury-2",
        "messages": [
            {
                "role": "system",
                "content": "You are a meeting assistant. Summarise the transcript so far in 2-3 sentences. Focus on decisions, actions, and key numbers."
            },
            {
                "role": "user",
                "content": f"Transcript so far: {transcript_so_far}"
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

def build_note_body():
    transcript_html = "<br>".join(transcript_lines)
    body = f"<b>Transcript:</b><br><br>{transcript_html}<br><br><b>Summary:</b><br><br>{current_summary}"
    return body

def save_to_notes():
    body = build_note_body()
    body = body.replace('"', '\\"')
    script = f"""
    tell application "Notes"
        set noteTitle to "{note_title}"
        set noteBody to "{body}"
        set matchingNotes to (notes whose name is noteTitle)
        if length of matchingNotes > 0 then
            set body of item 1 of matchingNotes to noteBody
        else
            make new note at folder "Notes" with properties {{name:noteTitle, body:noteBody}}
        end if
    end tell
    """
    subprocess.run(['osascript', '-e', script])

def save_to_markdown():
    filename = f"livebrief_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    body = build_note_body()
    with open(filename, 'w') as f:
        f.write(f"# {note_title}\n\n{body}")

def save_output():
    if OUTPUT_FORMAT == "notes":
        save_to_notes()
    elif OUTPUT_FORMAT == "markdown":
        save_to_markdown()

# --- MAIN LOOP ---
print("Loading Whisper model...")
model = WhisperModel("base")
print(f"\nLiveBrief is listening... (press Ctrl+C to stop)")
print(f"Output format: {OUTPUT_FORMAT}\n")

chunk_counter = 0

try:
    while True:
        audio = sd.rec(
            frames=CHUNK_SECONDS * SAMPLE_RATE,
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=DEVICE
        )
        sd.wait()

        audio_data = audio.squeeze()
        segments, _ = model.transcribe(audio_data, language="en")

        for segment in segments:
            line = segment.text.strip()
            if line:
                transcript_lines.append(line)
                chunk_counter += 1
                print(f"[caption] {line}")

                if chunk_counter % SUMMARY_EVERY == 0:
                    full_transcript = " ".join(transcript_lines)
                    current_summary = get_summary(full_transcript)
                    print(f"\n[summary] {current_summary}\n")
                    save_output()

except KeyboardInterrupt:
    print("\n\nFinalising brief...")
    if transcript_lines:
        full_transcript = " ".join(transcript_lines)
        current_summary = get_summary(full_transcript)
        save_output()
    print(f"Brief saved — '{note_title}'")