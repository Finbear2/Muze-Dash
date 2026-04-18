import getpass
import json
import sys
import os

codeDir = os.path.dirname(os.path.abspath("code/main.py"))
baseDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(codeDir)

from CONFIG import SETTINGS

Service =f"""
[Unit]
Description=Canto
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u {os.path.join(codeDir, "main.py")}
Restart=always
User={getpass.getuser()}
WorkingDirectory={codeDir}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target"""

with open(os.path.join(baseDir, "canto.service"), "w", encoding="utf-8") as f:
    f.write(Service)
    print("Made canto.service file to be moved to syctemctl location!\n")

name = input("Enter device name, can be changed later >>> ")
SETTINGS["general"]["name"] = name

secret = input("Enter the shared secret of your server >>> ")
SETTINGS["server"]["shared secret"] = secret

url = input("Enter url of server, example: http://server_ip:port https://canto.your_domain or whatever you're hosting it as >>> ")
SETTINGS["server"]["server url"] = url

SETTINGS["display"]["connected"] = True
SETTINGS["general"]["testing"] = False

# Save config to config.json
with open(os.path.join(codeDir, "config.json"), "w", encoding="utf-8") as f:
    json.dump(SETTINGS, f, indent=4)
    print("\nSaved new config.json!")