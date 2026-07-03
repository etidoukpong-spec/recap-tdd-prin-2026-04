from flask import Flask, render_template, request
from .core import Duty, DutyRepository

app = Flask(__name__)
repository = DutyRepository()

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    
    if request.method == "POST":
        id_chosen = request.form.get("duty_id")
        desc_typed = request.form.get("description")

        try:
            duty = Duty(id=id_chosen, desc=desc_typed)
            repository.add(duty)
        except ValueError as e:
            error_message = str(e)
    
    options = Duty.get_options()
    duties = repository.read_all()
    
    return render_template("index.html", options=options, duties=duties, error_message=error_message)