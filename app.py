from flask import Flask, render_template, request
from duties.controller import get_duties_from_db, create_duty_from_form, save_duty_in_db

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            duty = create_duty_from_form(request.form)
            save_duty_in_db(duty)
            message = f"{duty.identifier} created!"
        except:
            message = "Something went wrong"
        duties = get_duties_from_db()
        return render_template("index.html", message=message, duties=duties)
    else:
        duties = get_duties_from_db()
        return render_template("index.html", duties=duties)