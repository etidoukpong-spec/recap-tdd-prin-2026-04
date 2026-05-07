from duties.controller import create_duty
from duties.duty import Duty

# MARK: Test Duty

def test_duty_has_identifier():
    duty = Duty("Duty 1", "Script and code in at least one general purpose language and at least one domain-specific language to orchestrate infrastructure, follow test driven development and ensure appropriate test coverage.")
    assert duty.get_identifier()

def test_another_duty_has_a_different_name():
    duty2 = Duty("Duty 2", "Initiate and facilitate knowledge sharing and technical collaboration with teams and individuals, with a focus on supporting development of team members.")
    assert duty2.get_identifier() is not "Duty 1"

def test_duty_has_a_description():
    duty = Duty("Duty 1", "Script and code in at least one general purpose language and at least one domain-specific language to orchestrate infrastructure, follow test driven development and ensure appropriate test coverage.")
    assert duty.get_description() 
    assert "Script and code" in duty.get_description()

def test_duty_has_a_different_description():
    duty2 = Duty("Duty 2", "Initiate and facilitate knowledge sharing and technical collaboration with teams and individuals, with a focus on supporting development of team members.")
    assert duty2.get_description() 
    assert "Initiate and facilitate" in duty2.get_description()

# MARK: Test Create

def test_create_function_returns_a_duty():
    duty = create_duty()
    assert type(duty) == Duty
    
def test_duty_created_matches_input():
    identifier = "test identifier"
    description = "test description"
    duty = create_duty(identifier, description)
    assert duty.get_identifier() == identifier
    assert duty.get_description() == description
