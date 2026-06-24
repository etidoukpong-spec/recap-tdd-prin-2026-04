class Duty: 
    def __init__(self, id="", desc="", coin=""):
        if not id:
            raise ValueError("Name cannot be blank")
        if not desc:
            raise ValueError("Description cannot be blank")
            
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

    def read(self, duty_id):
        return self._database.get(duty_id)