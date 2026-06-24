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
        pass

    def read(self, duty_id):
        pass