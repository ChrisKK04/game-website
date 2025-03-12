# This file handles routing

from flask import Flask
from flask import redirect, render_template, request, session
import config, db

app = Flask(__name__)
app.secret_key = config.secret_key # setting session key

@app.route("/") # homepage
def index():
    return render_template("index.html")