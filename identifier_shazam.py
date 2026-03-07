from shazamio import Shazam
import urllib.parse

async def identify(path:str = "temp.wav", raw:bool = False):
    client = Shazam()
    print("Making shazam request...")
    result = await client.recognize(path)
    print("Recieved data!")
    if raw:
        return result
    elif len(result["matches"]) == 0:
        return None
    track = result["track"]
    data = {
        "title": track["title"],
        "artist": track["subtitle"],
        "album": track["sections"][0]["metadata"][0]["text"],
        "released": track["sections"][0]["metadata"][2]["text"],
        "link": {
            "shazam": track["share"]["href"],
            "spotify": f"https://open.spotify.com/search/{urllib.parse.quote(track['title'] + ' ' + track['subtitle'])}"
        }
    }
    return data