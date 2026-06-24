class Duty: 
    ALLOWED_AUTOMATE_DUTIES = ["Duty 5", "Duty 7", "Duty 10"]

    def __init__(self, id="", desc="", coin=""):
        if not id:
            raise ValueError("Name cannot be blank")
        if not desc:
            raise ValueError("Description cannot be blank")
        
        if id not in self.ALLOWED_AUTOMATE_DUTIES:
            raise ValueError("Duty is not assigned to the Automate coin")
                             
        self.id = id
        self.desc = desc
        self.coin = coin

class DutyRepository:
    def __init__(self):
        self._database = {}

    def add(self, duty):
        if self.read(duty.id) is not None:
            raise ValueError("Duty with this name already exists")
        self._database[duty.id] = duty

        payload = {"id": duty.id, "desc": duty.desc, "coin": duty.coin}

        client = DatabaseClient()
        client.save(payload)

    def read(self, duty_id):
        client = DatabaseClient()
        row = client.fetch(duty_id)
        if row == None:
            return self._database.get(duty_id)
        duty = Duty(id=row["id"], desc=row["desc"], coin=row["coin"])
        return duty
    
class DatabaseClient:
    def save(self, payload):
        pass
    def fetch(self, id):
        pass