from duties import db
from duties.duty import Duty, create_duty

def create_duty_from_form(form_data: dict):
    identifier = form_data["identifier"]
    description = form_data["description"]
    duty = create_duty(identifier, description)
    return duty

def get_duties_from_db():
    data = db.call_database()
    return [Duty(row["identifier"], row["description"]) for row in data]

def save_duty_in_db(duty):
    data = {"identifier": duty.identifier, "description": duty.description}
    db.call_database("INSERT", data)

