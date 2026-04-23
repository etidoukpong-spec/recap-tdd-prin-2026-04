from flask import Flask, render_template
from controller import get_duties_from_db

app = Flask(__name__)

@app.route("/")
def index():
    duties = get_duties_from_db()
    return render_template("index.html", duties=duties)