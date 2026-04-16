import urllib.parse, urllib.request
from PIL import Image
import requests
import os

baseDir = os.path.dirname(os.path.abspath(__file__))
coverPath = os.path.join(baseDir, "resources", "cover.png")

def getAlbumCover(artist, song):
    print("\nGetting album cover from Deezer API")
    displayManager.update(asyncio.run(sql.get(6)), "Cover")
    response = requests.get(f"https://api.deezer.com/search?q={urllib.parse.quote(artist + ' ' + song)}").json()

    data = response["data"][0]
    coverURL = data["album"]["cover_small"]

    print(f"downloading cover '{coverURL}'...")
    try:
        urllib.request.urlretrieve(coverURL, coverPath)
        print("Downloaded album cover!")
    except:
        print("Couldn't download album cover!")

    print("Turning album cover into pixel art image")
    image = Image.open(coverPath)

    small = image.resize((88, 88), Image.NEAREST)
    small = small.convert("1")
    small.save(coverPath)

    print("album cover now pixel art!")
    return True

if __name__ == "__main__":
    getAlbumCover("daft punk", "harder better")