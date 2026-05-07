from duties.controller import create_duty
from duties.duty import Duty

# MARK: Test Duty

def test_duty_has_identifier():
    duty = Duty("Duty 1", "Script and code")
    assert duty.has_identifier("Duty 1")

def test_duty_has_identifier_without_identifier():
    duty = Duty("", "Script and code")
    assert duty.has_identifier("Duty 1") == False

def test_another_duty_has_a_different_identifier():
    duty2 = Duty("Duty 2", "Initiate and facilitate")
    assert duty2.has_identifier("Duty 1") == False
    assert duty2.has_identifier("Duty 2")

def test_duty_has_a_description():
    duty = Duty("Duty 1", "Script and code")
    assert duty.has_description("Script and code")

def test_duty_has_description_without_description():
    duty = Duty("Duty 1", "")
    assert duty.has_description("Script and code") == False

def test_duty_has_a_different_description():
    duty2 = Duty("Duty 2", "Initiate and facilitate")
    assert duty2.has_description("Script and code") == False
    assert duty2.has_description("Initiate and facilitate") 

# MARK: Test Create

def test_create_function_returns_a_duty():
    duty = create_duty()
    assert type(duty) == Duty
    
def test_duty_created_matches_input():
    identifier = "test identifier"
    description = "test description"
    duty = create_duty(identifier, description)
    assert duty.matches(identifier, description)
