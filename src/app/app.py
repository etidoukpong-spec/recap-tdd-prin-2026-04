from flask import Flask, render_template, request
from .core import Duty, DutyRepository

app = Flask(__name__)
repository = DutyRepository()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        id_chosen = request.form.get("duty_id")
        desc_typed = request.form.get("description")

        duty = Duty(id=id_chosen,desc=desc_typed)

        repository.add(duty)
    
    options = Duty.get_options()
    duties =  repository.read_all()
    
    return render_template("index.html", options=options, duties=duties)