from omni_epd import displayfactory
from PIL import Image, ImageDraw
from datetime import datetime
import textwrap
import socket
import funcs

displayedSong = "None"
mode = "list"

def drawTopBar(draw:ImageDraw.Draw, status:str):
    print("Drawing top bar...")

    if funcs.hasInternet():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # doesn't actually send anything, relax
        ip = s.getsockname()[0]
        s.close()

        draw.text((7, 2), f"WIFI-{ip}", fill=0)

    textLength = draw.textlength(f"{datetime.now().strftime('%H:%M')}-{status}")
    draw.text((243-textLength, 2), f"{datetime.now().strftime('%H:%M')}-{status}", fill=0)

    draw.line([(0,15), (250,15)], fill=0, width=1)

    print("Finished drawing top bar!")
    return draw

def displaySong(draw:ImageDraw.Draw, songimformation:dict, image:Image.new):
    global displayedSong

    print("Drawing song view...")

    topSong = songimformation[0]
    title = topSong["title"]
    artist = topSong["artist"]
    album = topSong["album"]

    displayedSong = title

    wrappedArtist = textwrap.fill(artist, width=17)
    wrappedAlbum = textwrap.fill(album, width=17)

    draw.text((141,25), title, fill=0)
    draw.text((141,45), f"{wrappedArtist}\n{wrappedAlbum}", fill=0)

    draw.ellipse([(15, 30.5), (15+76, 30.5+76)])
    draw.ellipse([(43.5, 59), (43.5+19, 59+19)])

    # Mid point is 67.5
    draw.rectangle([(48, 23), (137, 112)], outline=0, width=1, fill=255)

    cover = Image.open("resources/cover.png").convert('1')
    image.paste(cover, (49,24))

    print("Finished drawing!")
    return draw, image

def displayList(draw:ImageDraw.Draw, songimformation):
    global displayedSong
    displayedSong = "None"

    print("Drawing song list...")

    for i in range(len(songimformation)):
        print(f"Drawing song {i+1}...")
        song = songimformation[i]
        title = song["title"]
        artist = song["artist"]

        draw.text((10,25+(15*i)), f"{title} - {artist}", fill=0)

    print("Done drawing song list!")
    return draw

def update(songimformation:dict, status:str):
    print("\nUpdating screen...")

    # swap "omni_epd.mock" for "waveshare_epd.epd2in13_V2" when Pi arrives
    epd = displayfactory.load_display_driver("omni_epd.mock")

    epd.prepare()

    image = Image.new("1", (250, 122), 255)
    draw = ImageDraw.Draw(image)
    print("New image buffer created!")

    draw = drawTopBar(draw, status)

    if mode == "music":
        draw, image = displaySong(draw, songimformation, image)
    elif mode == "list":
        draw = displayList(draw, songimformation)

    print("Pushing image buffer to screen...")
    epd.display(image)
    print("Done, screen is updated!\n")
    epd.close()
    

if __name__ == "__main__":
    # swap "omni_epd.mock" for "waveshare_epd.epd2in13_V2" when Pi arrives
    epd = displayfactory.load_display_driver("omni_epd.mock")

    epd.prepare()

    image = Image.new("1", (250, 122), 255)
    draw = ImageDraw.Draw(image)

    draw = drawTopBar(draw, "Testing")

    epd.display(image)
    epd.close()
