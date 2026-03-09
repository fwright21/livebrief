from gtts import gTTS

text = """
Good morning everyone. Thanks for joining. Today we're presenting the initial creative direction for the Nova launch campaign.

We're proposing a three-phase approach. Phase one is awareness, running through April and May. 
Phase two is consideration, June through July. And phase three is conversion, August onwards.

The core message we're building around is: Nova doesn't just fit your life, it leads it.

On budget, we're recommending sixty percent digital, thirty percent out of home, and ten percent print.
The total proposed spend is four hundred thousand pounds.

Key dates to flag — creative sign off is needed by March twenty first. 
Media booking deadline is April first. And the campaign goes live April fourteenth.

Any questions before we move to the creative boards?
"""

print("Generating test audio...")
tts = gTTS(text=text, lang='en', slow=False)
tts.save("client_briefing_mercury.mp3")
print("Saved to client_briefing_mercury.mp3")