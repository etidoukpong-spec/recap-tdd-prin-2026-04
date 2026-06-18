class Duty(): 
    def __init__(self, id="", desc="", coin=""):
        self.id = id
        self.desc = desc
        self.coin = coin

class DutyRepository():
    def __init__(self):
        self._database = {}

    def add(self):
        pass

def test_duty_object_is_instantiated():
    duty = Duty()
    assert duty is not None

def test_duty_object_has_an_identifier():
    duty = Duty()
    assert duty.id is not None

def test_duty_object_has_a_description():
    duty = Duty()
    assert duty.desc is not None

def test_duty_belongs_to_a_coin():
    duty = Duty()
    assert duty.coin is not None

def test_duty_repository_is_instantiated():
    repository = DutyRepository()
    assert repository is not None

def test_repository_has_dictionary_database_attribute():
    repository = DutyRepository()
    assert hasattr(repository, "_database")
    assert isinstance(repository._database, dict)

def test_repository_can_add_duty():
    repository = DutyRepository()
    assert repository.add() is None