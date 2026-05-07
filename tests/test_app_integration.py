from duties import controller
from duties.duty import Duty

def test_db_is_called_successfully(mocker):

    mock_data = []

    mock_call = mocker.patch("duties.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()

    mock_call.assert_called_once()
    assert isinstance(duties, list)

def test_duties_are_returned(mocker):
    mock_data = [{
        "identifier": "identifier", 
        "description": "description"
        }]
    
    mocker.patch("duties.db.call_database", return_value=mock_data)
    duties = controller.get_duties_from_db()
    
    assert len(duties) > 0
    assert isinstance(duties[0], Duty)
    assert duties[0].identifier == "identifier"
