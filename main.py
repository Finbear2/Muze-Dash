import identifier
import threading
import random
import web
import funcs
import time
import sql
import os

sql.init()
threading.Thread(target=web.app.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True).start()

testing=True

while True:
    if not testing:
        if funcs.hasInternet():
            print("Syncing offline songs...")
            for file in os.listdir("offline"):
                if file.endswith(".wav"):
                    sql.write(identifier.sync(path=f"offline/{file}"))
                time.sleep(random.randint(5,7))
            print("Finished syncing!")
            sql.write(identifier.record())
        else:
            print("Using offline mode as user hasn't got internet!")
            sql.write(identifier.record(internet=False))

    time.sleep(random.randint(50,70))