import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MERCURY_API_KEY")
API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Simulated transcript chunks — as if someone is speaking in real time
chunks = [
    "Sarah opened the meeting and said the Q3 budget is over by 15%.",
    "Tom suggested cutting the contractor headcount to save costs.",
    "Sarah agreed but said she wants to review the numbers before deciding.",
    "James joined late and asked for a summary of what was discussed.",
    "Tom repeated the budget issue and Sarah explained the contractor proposal.",
    "The team agreed to reconvene on Friday with the updated figures."
]

# This will grow as we add chunks — simulating a live transcript
transcript_so_far = []

for i, chunk in enumerate(chunks):
    transcript_so_far.append(chunk)
    
    # Join all chunks into one block of text
    full_transcript = " ".join(transcript_so_far)
    
    payload = {
        "model": "mercury-2",
        "messages": [
            {
                "role": "system",
                "content": "You are a meeting assistant. Summarise the transcript so far in 2-3 sentences."
            },
            {
                "role": "user",
                "content": f"Transcript so far: '{full_transcript}'"
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        summary = response.json()["choices"][0]["message"]["content"]
        print(f"\n--- After chunk {i+1} ---")
        print(f"New line: {chunk}")
        print(f"Summary: {summary}")
    else:
        print(f"Error {response.status_code}: {response.text}")