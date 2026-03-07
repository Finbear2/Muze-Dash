import sqlite3

DB = "songs.db"

def init():
    con = sqlite3.connect(DB)
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            album TEXT,
            shazamLink TEXT,
            spotifyLink TEXT,
            starred INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    print("Initialised database!")

    con.close()

def get(limit:int = 9):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    
    cursor.execute("SELECT * FROM songs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    con.close()
    return rows

def write(data):
    con = sqlite3.connect(DB)
    cursor = con.cursor()

    if data:
        print("\nWriting to database...")
        cursor.execute("INSERT INTO songs (title, artist, album, shazamLink, spotifyLink) VALUES (?, ?, ?, ?, ?)",
                (data["title"], data["artist"], data["album"], data["link"]["shazam"], data["link"]["spotify"]))
        con.commit()
        print("Saved to database!")
    else:
        print("\nNo data, not writing anything to database!")

    con.close()