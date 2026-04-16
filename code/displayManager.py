from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from CONFIG import SETTINGS
import textwrap
import socket
import funcs
import os

displayedSong = "None"
mode = "music"
lastMode = "list"
lastList = {}
refreshes = 0

baseDir = os.path.dirname(os.path.abspath(__file__))
coverPath = os.path.join(baseDir, "resources", "cover.png")

epd = None
connected = SETTINGS["DISPLAY"]["connected"]

if connected:
    from waveshare_epd import epd2in13_V4

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", SETTINGS["DISPLAY"]["font size"])

    epd = epd2in13_V4.EPD()
    epd.Clear()
    print("Screen Initialised")

def drawTopBar(draw:ImageDraw.Draw, status:str):
    print("Drawing top bar...")

    if funcs.hasInternet():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
        s.close()

        draw.text((7, 2), f"WIFI-{ip}", font=font, fill=0)

    textLength = draw.textlength(f"{datetime.now().strftime('%H:%M')}-{status}", font=font)
    draw.text((243-textLength, 2), f"{datetime.now().strftime('%H:%M')}-{status}", font=font, fill=0)

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

    wrappedTitle = textwrap.fill(title, width=17)
    wrappedArtist = textwrap.fill(artist, width=17)
    wrappedAlbum = textwrap.fill(album, width=17)

    draw.text((141,25), f"{wrappedTitle}\n\n{wrappedArtist}\n{wrappedAlbum}", font=font, fill=0)

    draw.ellipse([(15, 30.5), (15+76, 30.5+76)])
    draw.ellipse([(43.5, 59), (43.5+19, 59+19)])

    # Mid point is 67.5
    draw.rectangle([(48, 23), (137, 112)], outline=0, width=1, fill=255)

    cover = Image.open(coverPath).convert("1")
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

        draw.text((10,25+(15*i)), f"{title} - {artist}", font=font, fill=0)

    print("Done drawing song list!")
    return draw

def update(songimformation:dict, status:str):
    if not connected: return None;
    print("\nUpdating screen...")

    global refreshes
    global displayedSong
    global lastMode
    global lastList

    image = Image.new("1", (250, 122), 255)
    draw = ImageDraw.Draw(image)
    print("New image buffer created!")

    draw = drawTopBar(draw, status)

    if mode == "music":
        draw, image = displaySong(draw, songimformation, image)
    elif mode == "list":
        draw = displayList(draw, songimformation)

    print("Pushing image buffer to screen...")

    epd.init()

    refreshes += 1
    if refreshes >= SETTINGS["DISPLAY"]["full refresh counter"]:
        epd.display(epd.getbuffer(image))
        refreshes = 0
    else:
        if mode == lastMode:
            if mode == "music":
                if displayedSong != songimformation[0]["title"]:
                    epd.display(epd.getbuffer(image))
                else:
                    epd.displayPartial(epd.getbuffer(image))
            elif mode == "list":
                if songimformation == lastList:
                    epd.displayPartial(epd.getbuffer(image))
                else:
                    epd.display(epd.getbuffer(image))
            else:
                epd.display(epd.getbuffer(image))
        else:
            epd.display(epd.getbuffer(image))

    lastMode = mode
    lastList = songimformation
    displayedSong = songimformation[0]["title"]

    print("Done, screen is updated!\n")
    epd.sleep()
    

if __name__ == "__main__":
    initScreen()

    image = Image.new("1", (250, 122), 255)
    draw = ImageDraw.Draw(image)

    draw = drawTopBar(draw, "Testing")

    epd.display(epd.getbuffer(image))
    epd.sleep()
