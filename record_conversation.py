import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

SAMPLE_RATE = 16000
DURATION = 30  # seconds — enough for a short back and forth

print("Recording for 30 seconds...")
print("Have a conversation — or play both roles yourself.")
print("Starting in 3 seconds...")

import time
time.sleep(3)

print("🔴 Recording...")
audio = sd.rec(
    frames=DURATION * SAMPLE_RATE,
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)
sd.wait()

wav.write("conversation_test.wav", SAMPLE_RATE, audio)
print("✅ Saved to conversation_test.wav")