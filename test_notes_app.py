import subprocess

script = """
tell application "Notes"
    make new note at folder "Notes" with properties {name:"LiveBrief Test", body:"If you can see this, it works!"}
end tell
"""

subprocess.run(['osascript', '-e', script])
print("Done — check your Notes app")