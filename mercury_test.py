import requests
import os
from dotenv import load_dotenv

# Load the .env file so MERCURY_API_KEY is available
load_dotenv()

API_KEY = os.getenv("MERCURY_API_KEY")

if not API_KEY:
    raise ValueError("No MERCURY_API_KEY found — did you create your .env file?")

API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mercury-2",
    "messages": [
        {
            "role": "system",
            "content": "You are a meeting assistant. Summarise conversation transcripts clearly and concisely."
        },
        {
            "role": "user",
            "content": "Transcript: 'Sarah said the Q3 budget is over by 15%. Tom suggested cutting contractors. Sarah wants to review the numbers first.' Summarise in 1-2 sentences."
        }
    ]
}

print("Sending request to Mercury 2...")
response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    summary = data["choices"][0]["message"]["content"]
    print("\n✅ Summary received:")
    print(summary)
else:
    print(f"\n❌ Error {response.status_code}:")
    print(response.text)