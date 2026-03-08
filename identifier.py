from shazam import identify
import sounddevice
import asyncio
import numpy
import scipy
import json
import time
import os

# --- VARIBLES ---

lastSong = "None"

# Settings
sampleRate = 44100
sampleSize = 20 # Sample size in seconds

def sync(sz:int = sampleSize, sr:int = sampleRate, path:str = "CHANGEME"):
    global lastSong

    data =asyncio.run(identify(path=path))
    os.remove(path)

    if data:
        print(f"""
        --- SONG FOUND ---
        Title: {data["title"]}
        Artist: {data["artist"]}
        Album: {data["album"]}
        Released: {data["released"]}
        Link: {data["link"]["spotify"]}
        """)
        if lastSong == data["title"]:
            print("Song already identified!")
            return None
        else:
            lastSong = data["title"]
            return data
    else:
        print("Sorry, song not found!")
        return None

def record(sz:int = sampleSize, sr:int = sampleRate, internet:bool = True):
    global lastSong

    # --- RECORD ---
    print("\nRecording...")
    audioData = sounddevice.rec(
        frames=int(sz*sr),
        samplerate=sr,
        channels=1,
        dtype="int16"
    )
    sounddevice.wait()
    scipy.io.wavfile.write("temp.wav", sampleRate, audioData)
    print("Saved audio file!")

    _, data = scipy.io.wavfile.read("temp.wav")
    print(numpy.abs(data).mean())
    if numpy.abs(data).mean() < 3500:
        print("Clip too quiet, skipping!")
        return None

    if internet:

        # --- INDENTIFY ---
        data = asyncio.run(identify())

        os.remove("temp.wav")

        if data:
            print(f"""
            --- SONG FOUND ---
            Title: {data["title"]}
            Artist: {data["artist"]}
            Album: {data["album"]}
            Released: {data["released"]}
            Link: {data["link"]["spotify"]}
            """)
            if lastSong == data["title"]:
                print("Song already identified!")
                return None
            else:
                lastSong = data["title"]
                return data
        else:
            print("Sorry, song not found!")
            return None

    else:
        filename = f"offline_{int(time.time())}.wav"
        os.rename("temp.wav", f"offline/{filename}")
        print("Offline, song saved to queue!")
        return None