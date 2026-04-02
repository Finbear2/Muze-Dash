from CONFIG import SETTINGS
import sqlite3
import aiohttp

sqlURL = f"{SETTINGS['GENERAL']['server url']}/sql"

async def init():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{sqlURL}/init",
            headers={"key": SETTINGS["GENERAL"]["shared secret"]}) as resp:
            if resp.status not in (200, 204):
                print(f"\nDatabase Initlization Failed! Error code {resp.status}")
            else:
                print("\nDatabase Initliazed!")

async def get(limit:int = 9):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{sqlURL}/get",
            headers={
                "key": SETTINGS["GENERAL"]["shared secret"],
                "limit": str(limit)
            }) as resp:
            if resp.status not in (200, 204):
                print(f"\nDatabase to get data from database! Error code {resp.status}")
                return None
            else:
                result = await resp.json()
                return result

async def write(data):
    if data:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{sqlURL}/write",
                headers={"key": SETTINGS["GENERAL"]["shared secret"]},
                json=data) as resp:
                if resp.status not in (200, 204):
                    print(f"\nFailed to write to database! Error code {resp.status}")
                    return None
                else:
                    result = await resp.json()
                    return result
    else:
        print("Nothing to write to database!")
        return None