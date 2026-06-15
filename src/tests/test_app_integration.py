from src import controller
from src.duty import Duty

def test_db_is_called_successfully(mocker):

    mock_data = []

    mock_call = mocker.patch("src.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()

    mock_call.assert_called_once()
    assert isinstance(duties, list)

def test_duties_are_returned_from_db(mocker):
    mock_data = [{
        "identifier": "identifier", 
        "description": "description"
        }]
    
    mocker.patch("src.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()
    
    assert len(duties) > 0
    assert isinstance(duties[0], Duty)
    assert duties[0].identifier == "identifier"

def test_create_function_returns_a_duty_from_form_data(mocker):
    mock_duty = Duty("identifier", "description")
    mocker.patch("src.duty.create_duty", return_value=mock_duty)

    form_data = {
        "identifier": "duty identifier",
        "description": "duty description"
    }

    duty = controller.create_duty_from_form(form_data)

    assert duty.identifier == form_data["identifier"]
    assert duty.description == form_data["description"]

def test_new_duty_is_added_to_db(mocker):
    mock_call = mocker.patch("src.db.call_database")

    duty = Duty("identifier", "description")

    controller.save_duty_in_db(duty)

    expected_data = {"identifier": "identifier", "description": "description"}
    mock_call.assert_called_once_with("INSERT", expected_data)

def test_new_duty_is_unique_to_db(mocker):
    pass