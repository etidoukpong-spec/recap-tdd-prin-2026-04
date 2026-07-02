import pytest
from src.app.core import DatabaseClient, Duty, DutyRepository

class TestDutyObject:
    def setup_method(self):
        self.duty = Duty(id="Duty 5", desc="Build and operate", coin="Automate")  

    def test_duty_object_is_instantiated(self):
        assert self.duty is not None

    def test_duty_object_has_an_identifier(self):
        assert self.duty.id is not None

    def test_duty_object_has_a_description(self):
        assert self.duty.desc is not None

    def test_duty_belongs_to_a_coin(self):
        assert self.duty.coin is not None
    
    def test_duty_identifier_present(self):
        with pytest.raises(ValueError, match="Name cannot be blank"):
            Duty(id="", desc="Build and operate", coin="Automate")

    def test_duty_description_present(self):
        with pytest.raises(ValueError, match="Description cannot be blank"):
            Duty(id="Duty 5", desc="", coin="Automate")

    def test_cannot_create_duty_unassigned_to_automate_coin(self):
        with pytest.raises(ValueError, match="Duty is not assigned to the Automate coin"):
            Duty(id="Duty 1", desc="Script and code in a general purpose language")

class TestDutyRepository:
    def setup_method(self):
        self.duty = Duty(id="Duty 5", desc="Build and operate", coin="Automate")
        self.duty_2 = Duty(id="Duty 7", desc="Provision cloud infrastructure", coin="Automate")
        self.duplicate_duty = Duty(id="Duty 5", desc="Provision cloud infrastructure", coin="Automate")
        self.repository = DutyRepository()
        self.db_client = DatabaseClient()
        self.mock_row = {
            "id": "Duty 7", 
            "desc": "Provision cloud infrastructure", 
            "coin": "Automate"
        }

    def test_duty_repository_is_instantiated(self):
        assert self.repository is not None

    def test_repository_has_dictionary_database_attribute(self):
        assert hasattr(self.repository, "_database")
        assert isinstance(self.repository._database, dict)

    def test_repository_can_add_duty(self):
        assert self.repository.add(self.duty) is None

    def test_repository_can_read_duty(self):
        assert self.repository.read(self.duty.id) is None

    def test_repository_stores_added_duty_in_database(self):  
        self.repository.add(self.duty)
        
        assert self.repository.read(self.duty.id) == self.duty

    def test_repository_can_read_all_values_in_database(self):
        repository = DutyRepository()
        repository.add(self.duty)
        repository.add(self.duty_2)

        values = repository.read_all()

        assert isinstance(values, list)
        assert isinstance(values[0], Duty)
        assert len(values) == 2

    def test_repository_prevents_adding_duties_with_duplicate_ids(self):
        self.repository.add(self.duty)

        with pytest.raises(ValueError, match="Duty with this name already exists"):
            self.repository.add(self.duplicate_duty)

    def test_db_client_exists(self):
        assert self.db_client is not None

    def test_database_client_has_save_method(self):
        assert hasattr(self.db_client, "save")

    def test_repository_calls_database_client_on_add(self, mocker):
        mock_execute = mocker.patch("src.app.core.DatabaseClient.save")

        self.repository.add(self.duty)

        mock_execute.assert_called_once()

    def test_repository_passes_payload_to_client(self, mocker):
        mock_execute = mocker.patch("src.app.core.DatabaseClient.save")
        
        self.repository.add(self.duty)
        
        expected_payload = {
            "id": "Duty 5",
            "desc": "Build and operate",
            "coin": "Automate"
        }
        mock_execute.assert_called_once_with(expected_payload)

    def test_database_client_has_fetch_method(self):
        assert hasattr(self.db_client, "fetch")

    def test_repository_calls_database_client_on_read(self, mocker):
        mock_execute = mocker.patch("src.app.core.DatabaseClient.fetch", return_value=self.mock_row)

        self.repository.read("Duty 7")

        mock_execute.assert_called_once()

    def test_repository_reads_and_hydrates_data_from_database_client(self, mocker):                
        mocker.patch("src.app.core.DatabaseClient.fetch", return_value=self.mock_row)
        
        duty = self.repository.read("Duty 7")

        assert isinstance(duty, Duty)
        assert duty.id == "Duty 7"
        assert duty.desc == "Provision cloud infrastructure"