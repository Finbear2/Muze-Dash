import requests
import os

baseDir = os.path.dirname(os.path.abspath(__file__))
logoPath = os.path.join(baseDir, "resources", "logo.txt")

def logo():
    with open(logoPath, "r") as f:
        print(f.read())

def hasInternet(url:str = "http://google.com"):
    try:
        request = requests.get(url, timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False