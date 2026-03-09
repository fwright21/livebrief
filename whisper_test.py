from faster_whisper import WhisperModel

# Load the model — "base" is a good balance of speed and accuracy
# first run will download the model (~150mb), subsequent runs use the cache
print("Loading Whisper model...")
model = WhisperModel("base")

# Point this at any audio file on your Mac
#AUDIO_FILE = "/Users/francescawright/Downloads/cartesia_audio_2026-03-08T20_56_32+01_00.wav"
AUDIO_FILE = "client_briefing_mercury.mp3"

print(f"Transcribing {AUDIO_FILE}...")
segments, info = model.transcribe(AUDIO_FILE)

print(f"\nDetected language: {info.language}")
print("\nTranscript:")
for segment in segments:
    print(f"[{segment.start:.1f}s -> {segment.end:.1f}s] {segment.text}")