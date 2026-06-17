class Duty(): 
    def __init__(self, id=""):
        self.id = id

def test_duty_object_is_instantiated():
    duty = Duty()
    assert duty is not None

def test_duty_object_has_an_identifier():
    duty = Duty()
    assert duty.id is not None

def test_duty_object_has_a_description():
    duty = Duty()
    assert duty.desc is not None
    