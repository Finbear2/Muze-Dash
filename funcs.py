import requests

def hasInternet(url:str = "http://google.com"):
    try:
        request = requests.get(url, timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False