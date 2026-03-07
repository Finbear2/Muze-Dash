from flask import Flask, render_template
import sql

app = Flask(__name__)

@app.route("/")
def recent():
    return render_template("index.html", data=sql.get())