#!/bin/bash
set -e

sudo apt-get update

sudo apt-get install -y git portaudio19-dev python3-scipy python3-aiohttp python3-pip python3-pil python3-numpy python3-gpiozero fonts-dejavu-core unzip wget

python3 -m pip install sounddevice --break-system-packages
python3 -m pip install spidev --break-system-packages

if [ ! -d "Canto" ]; then
    wget -O canto.zip https://github.com/Finbear2/Canto/archive/refs/heads/main.zip
    unzip canto.zip
    mv Canto-main Canto
fi

cd Canto

mkdir -p code/offline

mv code/screenSavers/* ~/ 

cd ..

python3 setup.py

sudo mv canto.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable canto.service

sudo raspi-config nonint do_spi 0
sudo usermod -aG spi $USER

echo "Installed, restarting device. Canto will run on all future startups automatically!"
sudo reboot