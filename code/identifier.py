from CONFIG import SETTINGS
from shazam import identify
import displayManager
import sounddevice
import asyncio
import numpy
import scipy
import json
import time
import sql
import os

# --- VARIBLES ---

lastSong = {}
songPlaying = False

# Settings
sampleRate = SETTINGS["IDENTIFIACTION"]["sample rate"]
sampleSize = SETTINGS["IDENTIFIACTION"]["sample size"]

baseDir = os.path.dirname(os.path.abspath(__file__))
offlinePath = os.path.join(baseDir, "offline")

def sync(sz:int = sampleSize, sr:int = sampleRate, path:str = "CHANGEME"):
    global lastSong
    global songPlaying

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
        if len(lastSong) > 0:
            if lastSong["title"] == data["title"]:
                print("Song already identified!")
                songPlaying = True
                return None
            else:
                songPlaying = True
                lastSong = data
                return data
        else:
            songPlaying = True
            lastSong = data
            return data
    else:
        print("Sorry, song not found!")
        songPlaying = False
        lastSong = {}
        return None

def record(sz:int = sampleSize, sr:int = sampleRate, internet:bool = True):
    global lastSong
    global songPlaying

    # --- RECORD ---
    print("\nRecording...")
    
    if internet:
        displayManager.update(asyncio.run(sql.get(6)), "Listening")

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
    if numpy.abs(data).mean() < SETTINGS["IDENTIFIACTION"]["noise threshold"]:
        print("Clip too quiet, skipping!")
        songPlaying = False
        lastSong = {}
        return None

    if internet:

        # --- IDENTIFY ---#
        displayManager.update(asyncio.run(sql.get(6)), "Identifying")
        data = asyncio.run(identify())

        os.remove("temp.wav")

        if data:
            songPlaying = True
            print(f"""
            --- SONG FOUND ---
            Title: {data["title"]}
            Artist: {data["artist"]}
            Album: {data["album"]}
            Released: {data["released"]}
            Link: {data["link"]["spotify"]}
            """)
            if len(lastSong) > 0:
                if lastSong["title"] == data["title"]:
                    print("Song already identified!")
                    songPlaying = True
                    return None
                else:
                    lastSong = data
                    songPlaying = True
                    return data
            else:
                lastSong = data
                songPlaying = True
                return data
        else:
            songPlaying = False
            lastSong = {}
            return None

    else:
        lastSong = {}
        filename = f"offline_{int(time.time())}.wav"
        os.rename("temp.wav", f"{offlinePath}/{filename}")
        print("Offline, song saved to queue!")
        
        return None