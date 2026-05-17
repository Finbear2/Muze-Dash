from CONFIG import SETTINGS
from pathlib import Path
import requests
import aiohttp
import json
import os

baseDir = os.path.dirname(os.path.abspath(__file__))
logoPath = os.path.join(baseDir, "resources", "logo.txt")
settingsPath = os.path.join(baseDir, "config.json")
saversDir = Path.home()

def logo():
    with open(logoPath, "r") as f:
        print(f.read())

async def getStatus(boot: bool):

    screenSaverPaths = []

    for file in os.listdir(saverPath):
        if file.endswith(".png"):
            screenSaverPaths.append(os.path.join(saverPath, file))

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{SETTINGS['server']['server url']}/status",
            headers={
                "key": SETTINGS["server"]["shared secret"],
                "name": SETTINGS["general"]["name"],
                "boot": "true" if boot else "false",
            },
            json={
                "screensavers": screenSaverPaths
            }) as resp:
            if resp.status not in (200, 204):
                print(f"\nCouldn't get status from server! Error code {resp.status}")
                print(resp.json())
                return None
            else:
                print("Got status from server!")
                result = await resp.json()
                return result

def saveSettings(data: dict):
    if SETTINGS == data:
        print("Not saving settings as no changes were made!")
        return None

    print("Saving settings config...")
    with open(settingsPath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        print("Saved to config.json")

def hasInternet(url:str = "http://google.com"):
    try:
        request = requests.get(url, timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False