# LiveBrief

A local meeting tool that captions and summarises conversations in real time.

## What it does
As someone speaks, captions appear instantly and a summary updates live — so by the time the meeting ends, your brief is already done. Built to test the speed of Mercury 2 by Inception Labs.

## Why I built it
This was a learning project to explore:
- Mercury 2 (Inception Labs) — a fast diffusion-based language model, used here for live summarisation
- faster-whisper — local speech-to-text running entirely on device
- Python audio pipelines — microphone capture, chunking, and real-time processing
- Apple Notes automation — using osascript to write structured output to Notes
- Markdown output — clean files ready for a future RAG pipeline

## Stack
- faster-whisper — speech to text, runs locally
- Mercury 2 API — live summarisation
- sounddevice — microphone capture
- osascript — Apple Notes integration
- Python — backend logic

## Output
Each meeting produces:
- An Apple Note with transcript and summary
- A markdown file in /briefs ready for RAG ingestion

## How to run
cp .env.example .env
pip install -r requirements.txt
python livebrief_main.py

## Status
Work in progress. Next steps:
- RAG pipeline to query across past meetings
- Speaker diarization (tested, deprioritised for speed)