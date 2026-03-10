SETTINGS = {
    "WEB UI": {
        "host": "0.0.0.0", 
        "port": 5000,
        "album art": True
    },
    "IDENTIFIACTION": {
        "inbetween time": 60, # Time inbetween each recording in seconds
        "sync inbetween time": 5, # Time inbetween each recording during offline syncing in seconds
        "noise threshold": 3000, # The volume a noise must be above to be regonised,
        "sample rate": 44100, # The sample rate for recordings
        "sample size": 20, # The zise of each recording in settings
    },
    "SQL": {
        "database path": "database/songs.db"
    },
    "DISPLAY": {
        "connected": True,
        "album cover size": 88, # DONT CHANGE
        "album cover dithering type": "atkinson"
    }
}