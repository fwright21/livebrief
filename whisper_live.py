import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# Settings
SAMPLE_RATE = 16000  # Whisper expects 16khz audio
CHUNK_SECONDS = 5    # Record 5 seconds at a time
DEVICE = 0           # MacBook Pro Microphone

print("Loading Whisper model...")
model = WhisperModel("base")

print("\nLivebrief is listening... (press Ctrl+C to stop)\n")

try:
    while True:
        # Record a chunk of audio from the mic
        audio = sd.rec(
            frames=CHUNK_SECONDS * SAMPLE_RATE,
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=DEVICE
        )
        sd.wait()  # Wait until the chunk is finished recording

        # Whisper expects a 1D numpy array — squeeze removes the extra dimension
        audio_data = audio.squeeze()

        # Transcribe the chunk
        segments, info = model.transcribe(audio_data, language="en")

        for segment in segments:
            print(f"[{segment.start:.1f}s] {segment.text}")

except KeyboardInterrupt:
    print("\nStopped.")