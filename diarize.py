import os
import json
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

print("Loading diarization pipeline...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

print("Running diarization...")
diarization = pipeline("conversation_test.wav")

segments = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    segments.append({"start": turn.start, "end": turn.end, "speaker": speaker})

with open("speaker_segments.json", "w") as f:
    json.dump(segments, f)

print(f"Saved {len(segments)} speaker segments to speaker_segments.json")