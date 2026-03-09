import sounddevice as sd
import numpy as np
import requests
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────
MERCURY_API_KEY = os.getenv("MERCURY_API_KEY")
API_URL         = "https://api.inceptionlabs.ai/v1/chat/completions"
SAMPLE_RATE     = 16000
CHUNK_SECONDS   = 5
DEVICE          = 0
SUMMARY_EVERY   = 3
OUTPUT_NOTES    = True
OUTPUT_MARKDOWN = True
# ──────────────────────────────────────────────────────────

headers = {
    "Authorization": f"Bearer {MERCURY_API_KEY}",
    "Content-Type": "application/json"
}

meeting_time     = datetime.now().strftime("%Y-%m-%d %H%M")
note_title       = f"LiveBrief {meeting_time}"
md_filename      = f"briefs/{meeting_time}.md"
os.makedirs("briefs", exist_ok=True)

transcript_lines = []
current_summary  = ""
chunk_counter    = 0

# ─── MERCURY ──────────────────────────────────────────────
def get_summary(transcript):
    payload = {
        "model": "mercury-2",
        "messages": [
            {
                "role": "system",
                "content": "You are a meeting assistant. Summarise the transcript so far in 2-3 sentences. Focus on decisions, actions, and key numbers."
            },
            {
                "role": "user",
                "content": f"Transcript so far: {transcript}"
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"Error {response.status_code}"

# ─── OUTPUTS ──────────────────────────────────────────────
def save_to_notes():
    transcript_html = "<br>".join(transcript_lines)
    body = f"<b>Transcript:</b><br><br>{transcript_html}<br><br><b>Summary:</b><br><br>{current_summary}"
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
    with open(md_filename, "w") as f:
        f.write(f"# {note_title}\n\n")
        f.write(f"## Summary\n\n{current_summary}\n\n")
        f.write(f"## Transcript\n\n")
        for line in transcript_lines:
            f.write(f"{line}\n\n")

def save_all():
    if OUTPUT_NOTES:    save_to_notes()
    if OUTPUT_MARKDOWN: save_to_markdown()

# ─── MAIN LOOP ────────────────────────────────────────────
print("Loading Whisper...")
whisper = WhisperModel("base")

print(f"\n{'='*50}")
print(f"  LiveBrief — {meeting_time}")
print(f"{'='*50}")
print("🎙  Listening... (Ctrl+C to end)\n")

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

        segments, _ = whisper.transcribe(audio.squeeze(), language="en")
        for segment in segments:
            line = segment.text.strip()
            if line:
                transcript_lines.append(line)
                chunk_counter += 1
                print(f"  {line}")

                if chunk_counter % SUMMARY_EVERY == 0:
                    current_summary = get_summary(" ".join(transcript_lines))
                    print(f"\n  📋 {current_summary}\n")
                    save_all()

except KeyboardInterrupt:
    print("\n\nFinalising brief...")
    if transcript_lines:
        current_summary = get_summary(" ".join(transcript_lines))
    save_all()
    print(f"\n✅ Brief saved:")
    if OUTPUT_NOTES:    print(f"   Notes → '{note_title}'")
    if OUTPUT_MARKDOWN: print(f"   Markdown → {md_filename}")