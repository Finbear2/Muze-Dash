SETTINGS = {
    "GENERAL": {
        "testing": False,
        "shared secret": "Fish",
        "server url": "http://192.168.0.119:5000",
    },
    "IDENTIFIACTION": {
        "inbetween time": 60, # Time inbetween each recording in seconds
        "sync inbetween time": 5, # Time inbetween each recording during offline syncing in seconds
        "noise threshold": 3000, # The volume a noise must be above to be regonised dault is 3000
        "sample rate": 44100, # The sample rate for recordings
        "sample size": 20, # The size of each recording in seconds
    },
    "DISPLAY": {
        "connected": False,
        "full refresh counter": 3,
        "font size": 9,
    },
}
