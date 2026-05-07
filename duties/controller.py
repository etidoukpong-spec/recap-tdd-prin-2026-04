from duties import db
from duties.duty import Duty

def get_duties_from_db():
    data = db.call_database()
    return [Duty(row["identifier"], row["description"]) for row in data]
