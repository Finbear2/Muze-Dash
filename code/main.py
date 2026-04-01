"""
████████████████████ ████████ █████████████████    _____            _        
█░▒▓██       ███▓▒░█ █░░░░░░█ █░░░░░░░░░░░░░░░█   / ____|          | |       
█░▓█            █▓▒█ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |     __ _ _ __ | |_ ___  
█▓█              █▓█ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |    / _` | '_ \| __/ _ \ 
██      ████      ██ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |___| (_| | | | | || (_) |
██      ████      ██ █░░░░░░█ █████████████████   \_____\__,_|_| |_|\__\___/ 
█▓█              █▓█ █░░░░░░█                    
█▒▓█            █▓░█ █░░░░░░█ █████████████████  Version 0.1
█░░▓██        ██▓░▒█ █░░░░░░█ ██             ██  @Finbear2 2026   
████████████████████ ████████ █████████████████  
"""



#
#  _                     _      
# (_)_ __  _ __  ___ _ _| |_ ___
# | | '  \| '_ \/ _ \ '_|  _(_-<
# |_|_|_|_| .__/\___/_|  \__/__/
#         |_|                   

import asyncio
import random
import time
import os

# Import other modules
from CONFIG import SETTINGS
import displayManager
import identifier
import deezer
import funcs
import sql



#  _      _ _      
# (_)_ _ (_) |_ ___
# | | ' \| |  _(_-<
# |_|_||_|_|\__/__/

# Print logo cause vibeseseses
funcs.logo()

# Configure paths
baseDir = os.path.dirname(os.path.abspath(__file__))
offlinePath = os.path.join(baseDir, "offline")

# Initialise the sql database
if funcs.hasInternet():
    asyncio.run(sql.init())
else:
    print("Couldn't comunicate to server!")



#             _      
#  _ __  __ _(_)_ _  
# | '  \/ _` | | ' \ 
# |_|_|_\__,_|_|_||_|

if SETTINGS["GENERAL"]["testing"]:   # Testing mode

    print("Testing, will not listen only display webage!")
    songs = asyncio.run(sql.get(6))
    displayManager.update(songs, "Testing")
    while True:
        time.sleep(60)
        songs = asyncio.run(sql.get(6))
        displayManager.update(songs, "Testing")

else: # Full Mode

    while True:
        try:
            if funcs.hasInternet():

                displayManager.mode = "list"
                
                if len(os.listdir(offlinePath)) > 0:
                    print("Syncing offline songs...")

                    songs = asyncio.run(sql.get(6))
                    displayManager.update(songs, "Syncing")

                    for file in os.listdir(offlinePath):
                        if file.endswith(".wav"):
                            asyncio.run(sql.write(identifier.sync(path=f"{offlinePath}/{file}")))
                        time.sleep(random.randint(
                            SETTINGS["IDENTIFIACTION"]["sync inbetween time"],
                            SETTINGS["IDENTIFIACTION"]["sync inbetween time"]+2)
                        )
                    print("Finished syncing!")

                asyncio.run(sql.write(identifier.record()))

                if identifier.songPlaying and len(identifier.lastSong) > 0:
                    if displayManager.displayedSong != identifier.lastSong["title"]:
                        if deezer.getAlbumCover(identifier.lastSong["artist"], identifier.lastSong["title"]):

                            displayManager.mode = "music"
                            songs = asyncio.run(sql.get(6))
                            displayManager.update(songs, "Idle")

                elif not identifier.songPlaying:

                    displayManager.mode = "list"
                    songs = asyncio.run(sql.get(6))
                    displayManager.update(songs, "Idle")

                else:
                    songs = asyncio.run(sql.get(6))
                    displayManager.update(songs, "Idle")
                    
            else:
                print("Using offline mode as user hasn't got internet!")

                identifier.record(internet=False)
                if displayManager.mode == "list":
                    songs = asyncio.run(sql.get(6))
                    displayManager.update(songs, "Idle")
                else:
                    displayManager.mode == "Error"
                    displayManager.update({}, "Error")

        except Exception as e:
            print(e)
            
            if funcs.hasInternet():
                displayManager.mode = "list"
                songs = asyncio.run(sql.get(6))
                displayManager.update(songs, "Error")
            else:
                if displayManager.mode == "list":
                    displayManager.update(displayManager.lastList, "Error")
                else:
                    displayManager.mode == "Error"
                    displayManager.update({}, "Error")

        sleepTime = random.randint(SETTINGS["IDENTIFIACTION"]["inbetween time"]-10,SETTINGS["IDENTIFIACTION"]["inbetween time"]+10)

        print(f"Done cycle, waiting {sleepTime} seconds for next cycle!")
        time.sleep(sleepTime)