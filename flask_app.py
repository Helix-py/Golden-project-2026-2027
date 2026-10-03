
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def start_app():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dash")
def dash():
    return render_template("dashboard.html")

@app.route("/settings")
def setting():
    return render_template("settings.html")

@app.route("/interactive/<path:filename>")
def interactive(filename):
    return send_from_directory("interactive", filename)
