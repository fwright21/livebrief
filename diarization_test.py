import os
import torch
import subprocess
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from faster_whisper import WhisperModel

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
AUDIO_FILE = "client_briefing_mercury.mp3"
WAV_FILE = "client_briefing_mercury.wav"

# Convert MP3 to WAV first — avoids pyannote MP3 warnings
if not os.path.exists(WAV_FILE):
    print("Converting to WAV...")
    subprocess.run(["ffmpeg", "-i", AUDIO_FILE, "-ar", "16000", "-ac", "1", WAV_FILE])

# --- STEP 1: DIARIZATION ---
print("Loading diarization pipeline...")
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

print(f"Running diarization...")
diarization = diarization_pipeline(WAV_FILE)

speaker_segments = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    speaker_segments.append((turn.start, turn.end, speaker))

# Free memory before loading Whisper
del diarization_pipeline
torch.cuda.empty_cache() if torch.cuda.is_available() else None

# --- STEP 2: TRANSCRIPTION ---
print("Loading Whisper medium...")
whisper_model = WhisperModel("medium")

print("Transcribing...")
segments, info = whisper_model.transcribe(WAV_FILE)
whisper_segments = list(segments)

# --- STEP 3: ALIGN ---
def get_speaker(start, end, speaker_segments):
    best_speaker = "Unknown"
    best_overlap = 0
    for seg_start, seg_end, speaker in speaker_segments:
        overlap = min(end, seg_end) - max(start, seg_start)
        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = speaker
    return best_speaker

print(f"\nDetected language: {info.language}")
print("\n--- TRANSCRIPT WITH SPEAKERS ---\n")

for segment in whisper_segments:
    speaker = get_speaker(segment.start, segment.end, speaker_segments)
    print(f"{speaker}: {segment.text.strip()}")