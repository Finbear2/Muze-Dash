# Canto

Identify every song around you that plays viewable on a Web-UI and on the E-Ink sreen

**This project is in beta and not yet tested on hardware and support is not garunteed!**

@Fin 2026

<img src="resources/Buddy Holly-Weezer.png" width="500"/>
<img src="resources/Read My Mind-The Killers.png" width="500"/>

----

## What is it?

Canto is a little device designed to be ran on harware such as a Pi Zero that uses the ShazamIO python package to identify songs around you then with a 2.13 inch waveshare screen connected, it will display a black and white, pixel art version of the album art using the Deezer API and pyxelate

In it's current stage of development, it is fully coded but stl files for a case and any hardware specific features have not been made. Though, using a mock driver I was able to code a screen though the drivers need changing and maybe certain implementations will need fixing.

## Hardware

This software is ideally ran on a

- PI Zero 2 WH
- Waveshare 2.13" E-Ink screen (This at the moment cannot be changed)
- IS2 MEM microphone

Once the software is tested on device, I will provide a linux image that will have everything pre-configured
