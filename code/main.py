
# ████████████████████ ████████ █████████████████    _____            _        
# █░▒▓██       ███▓▒░█ █░░░░░░█ █░░░░░░░░░░░░░░░█   / ____|          | |       
# █░▓█            █▓▒█ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |     __ _ _ __ | |_ ___  
# █▓█              █▓█ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |    / _` | '_ \| __/ _ \ 
# ██      ████      ██ █░░░░░░█ █░░░░░░░░░░░░░░░█  | |___| (_| | | | | || (_) |
# ██      ████      ██ █░░░░░░█ █████████████████   \_____\__,_|_| |_|\__\___/ 
# █▓█              █▓█ █░░░░░░█                    
# █▒▓█            █▓░█ █░░░░░░█ █████████████████  Version 0.1
# █░░▓██        ██▓░▒█ █░░░░░░█ ██             ██  @Finbear2 2026   
# ████████████████████ ████████ █████████████████  



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

testData = [
    {
        "title": "Test Song",
        "artist": "Test",
        "album": "Testing Songs Volume 3"
    }
]

muted = False
boot = True
inactivity = 0

# Print logo cause vibeseseses
funcs.logo()

# Configure paths
baseDir = os.path.dirname(os.path.abspath(__file__))
offlinePath = os.path.join(baseDir, "offline")

# Initialise the sql database
if funcs.hasInternet():
    asyncio.run(sql.init())
else:
    print("Couldn't communicate to server!")



#             _      
#  _ __  __ _(_)_ _  
# | '  \/ _` | | ' \ 
# |_|_|_\__,_|_|_||_|

async def main():
    global boot

    if SETTINGS["general"]["testing"]:   # Testing mode

        if funcs.hasInternet():

            displayManager.mode = "music"

            status = await funcs.getStatus(boot)
            boot = False

            SETTINGS["general"]["name"] = status["name"]
            funcs.saveSettings(SETTINGS)

            print("Testing, will not listen only display song list!")
            songs = await sql.get(6)
            displayManager.update(songs, "Testing")
            displayManager.mode = "list"
            while True:
                time.sleep(60)
                songs = await sql.get(6)
                displayManager.update(songs, "Testing")

        else:

            displayManager.mode = "music"

            print("Testing, will not listen only displaying test data then quit!")
            displayManager.update(testData, "Testing")

    else: # Full Mode

        while True:
            try:
                if funcs.hasInternet():
                    
                    if len(os.listdir(offlinePath)) > 0:
                        print("Syncing offline songs...")

                        songs = await sql.get(6) 
                        displayManager.update(songs, "Syncing")

                        for file in os.listdir(offlinePath):
                            if file.endswith(".wav"):
                                data = await identifier.sync(path=f"{offlinePath}/{file}")
                                await sql.write(data)
                            time.sleep(random.randint(
                                SETTINGS["identification"]["sync inbetween time"],
                                SETTINGS["identification"]["sync inbetween time"]+2)
                            )
                        print("Finished syncing!")

                    status = await funcs.getStatus(boot) 
                    boot = False

                    SETTINGS["general"]["name"] = status["name"]
                    funcs.saveSettings(SETTINGS)

                    if not muted:

                        data = await identifier.record()
                        await sql.write(data)

                        songs = await sql.get(6)

                        if songPlaying:
                            deezer.getAlbumCover(identifier.lastSong["artist"], identifier.lastSong["title"])
                            displayManager.mode = "music"
                        else:
                            displayManager.mode = "list"

                        displayManager.update(songs, "idle")

                    else:

                        displayManager.mode = "list"
                        displayManager.update(songs, "Muted")
                        
                else:
                    print("Using offline mode as user hasn't got internet!")

                    displayManager.mode = "Blank"

                    if not muted:
                        await identifier.record(internet=False)
                        displayManager.update({}, "Offline")
                    else:
                        displayManager.update({}, "Offline-Muted")

                    
                    

            except Exception as e:
                print(e)
                
                if funcs.hasInternet():
                    displayManager.mode = "list"
                    songs = await sql.get(6)
                    displayManager.update(songs, "Error")
                else:
                    displayManager.mode = "Blank"
                    displayManager.update({}, "Error")

            sleepTime = random.randint(SETTINGS["identification"]["inbetween time"]-10,SETTINGS["identification"]["inbetween time"]+10)

            if displayManager.inactivity >= SETTINGS["display"]["screen saver threshold"]:
                sleepTime = sleepTime*2

            print(f"Done cycle, waiting {sleepTime} seconds for next cycle!")
            time.sleep(sleepTime)

asyncio.run(main())