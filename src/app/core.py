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

        client = DatabaseClient()
        client.execute()

    def read(self, duty_id):
        return self._database.get(duty_id)
    
class DatabaseClient:
    def execute(self):
        pass