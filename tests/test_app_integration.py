from app import app

from duties import controller
from duties.duty import Duty

def test_db_is_called_successfully(mocker):

    mock_data = []

    mock_call = mocker.patch("duties.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()

    mock_call.assert_called_once()
    assert isinstance(duties, list)

def test_duties_are_returned_from_db(mocker):
    mock_data = [{
        "identifier": "identifier", 
        "description": "description"
        }]
    
    mocker.patch("duties.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()
    
    assert len(duties) > 0
    assert isinstance(duties[0], Duty)
    assert duties[0].identifier == "identifier"

def test_create_function_returns_a_duty_from_form_data(mocker):
    mock_duty = Duty("identifier", "description")
    mocker.patch("duties.duty.create_duty", return_value=mock_duty)

    form_data = {
        "identifier": "identifier",
        "description": "description"
    }

    duty = controller.create_duty_from_form(form_data)

    assert duty.identifier == form_data["identifier"]
    assert duty.description == form_data["description"]

