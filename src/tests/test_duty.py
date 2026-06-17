class Duty(): 
    pass

def test_should_instantiate_duty_object():
    duty = Duty()
    assert duty is not None

def test_should_have_an_identifier():
    duty = Duty()
    assert duty.id is not None