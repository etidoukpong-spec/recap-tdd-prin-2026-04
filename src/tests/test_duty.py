class Duty(): 
    def __init__(self, id="", desc=""):
        self.id = id
        self.desc = desc

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