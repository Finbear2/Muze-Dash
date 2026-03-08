from flask import Flask, render_template
import random
import sql

app = Flask(__name__)

@app.route("/")
def recent():
    data = sql.get(200)

    for song in data:
        red = random.randint(220,255)
        green = random.randint(220,255)
        blue = random.randint(220,255)
        song["colour"] = dict()
        song["colour"]["pastel"] = f"rgb({red}, {green}, {blue})"
        song["colour"]["button"] = f"rgb({red-50}, {green-50}, {blue-50})"

    return render_template("index.html", data=data)