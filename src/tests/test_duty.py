import pytest
from app.core import Duty, DutyRepository

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

class TestDutyRepository:
    def setup_method(self):
        self.duty = Duty(id="Duty 5", desc="Build and operate", coin="Automate")
        self.repository = DutyRepository()

    def teardown_method(self):
        self.repository._database.clear()

    def test_duty_repository_is_instantiated(self):
        assert self.repository is not None

    def test_repository_has_dictionary_database_attribute(self):
        assert hasattr(self.repository, "_database")
        assert isinstance(self.repository._database, dict)

    def test_repository_can_add_duty(self):
        assert self.repository.add(self.duty) is None

    def test_repository_can_read_duty(self):
        assert self.repository.read(self.duty.id) is None
