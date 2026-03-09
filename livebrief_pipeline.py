import requests
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

API_KEY = os.getenv("MERCURY_API_KEY")
API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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

# Load Whisper and transcribe the audio file into segments
print("Loading Whisper model...")
model = WhisperModel("base")

print("Transcribing audio...")
segments, info = model.transcribe("client_briefing_mercury.mp3")
print(f"Detected language: {info.language}\n")

# This is the core LiveBrief loop
# We accumulate segments and update the summary every 3 chunks
transcript_so_far = []
chunk_counter = 0
SUMMARY_EVERY = 3  # update summary every 3 segments

print("=" * 50)
print("LIVEBRIEF RUNNING")
print("=" * 50)

for segment in segments:
    # Add the new segment to our growing transcript
    transcript_so_far.append(segment.text)
    chunk_counter += 1

    print(f"\n[{segment.start:.1f}s] {segment.text}")

    # Every 3 chunks, send the full transcript to Mercury for a summary
    if chunk_counter % SUMMARY_EVERY == 0:
        full_transcript = " ".join(transcript_so_far)
        summary = get_summary(full_transcript)
        print(f"\n--- LIVE SUMMARY (after {chunk_counter} chunks) ---")
        print(summary)
        print("-" * 50)

# Final summary at the end
print("\n\n===== FINAL BRIEF =====")
full_transcript = " ".join(transcript_so_far)
summary = get_summary(full_transcript)
print(summary)
print("=" * 50)