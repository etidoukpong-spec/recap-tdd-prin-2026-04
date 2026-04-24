from duties import controller
from duties.duty import Duty

def test_db_is_called_successfully(mocker):

    mock_data = [{
        "identifier": 1,
        "description": "Script and Code"
    }]
    mocker.patch("duties.controller.call_database", return_value=mock_data)

    actual_result = controller.call_database()

    controller.call_database.assert_called_once()
    assert isinstance(actual_result, list)
    for duty in actual_result:
        assert isinstance(duty, dict)


def test_duties_are_returned(mocker):
    mocker.patch("duties.controller.get_duties_from_db", return_value=[Duty(1, "Script and Code")])
    duties = controller.get_duties_from_db()
    assert isinstance(duties, list)
    for duty in duties:
        assert isinstance(duty, Duty)
    assert len(duties) > 0