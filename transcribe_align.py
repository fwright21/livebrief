from dotenv import load_dotenv
load_dotenv()
import json
from faster_whisper import WhisperModel

with open("speaker_segments.json") as f:
    speaker_segments = json.load(f)

def get_speaker(start, end):
    best_speaker = "Unknown"
    best_overlap = 0
    for seg in speaker_segments:
        overlap = min(end, seg["end"]) - max(start, seg["start"])
        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = seg["speaker"]
    return best_speaker

print("Loading Whisper medium...")
model = WhisperModel("medium")

print("Transcribing...")
segments, info = model.transcribe("conversation_test.wav")

print(f"Detected language: {info.language}")
print("\n--- TRANSCRIPT WITH SPEAKERS ---\n")

for segment in segments:
    speaker = get_speaker(segment.start, segment.end)
    print(f"{speaker}: {segment.text.strip()}")