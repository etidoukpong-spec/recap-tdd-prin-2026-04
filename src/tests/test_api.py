import os, uuid, pytest

os.environ["TESTING"] = "True"

from src.app.api import api
from src.app.models import Coin, Duty, Junction
from src.app.database import db, init_db

MODELS = [Duty, Coin, Junction]

@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()
    db.connect(reuse_if_open=True)
    db.drop_tables(MODELS, safe=True)
    db.create_tables(MODELS, safe=True)

    yield

    db.drop_tables(MODELS, safe=True)
    db.close()

@pytest.fixture()
def linked_data_setup():
    coin_a = Coin.create(coin_name="Coin A", is_complete=False)
    coin_b = Coin.create(coin_name="Coin B", is_complete=True)
    
    duty_1 = Duty.create(duty_name="Duty 1", duty_desc="First duty")
    duty_2 = Duty.create(duty_name="Duty 2", duty_desc="Shared duty")
    
    Junction.create(coin_id=coin_a, duty_id=duty_1)
    Junction.create(coin_id=coin_a, duty_id=duty_2)
    Junction.create(coin_id=coin_b, duty_id=duty_2)
    
    return {
        "coin_a": coin_a, 
        "coin_b": coin_b, 
        "duty_1": duty_1, 
        "duty_2": duty_2
    }


class TestCoinAPI:
    # --- CREATE ---
    def test_user_can_create_a_coin(self):
        with api.test_client() as client:
            coin = {"coin_name": "New Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            assert response.status_code == 201

    def test_user_cannot_create_a_duplicate_coin(self):
        with api.test_client() as client:
            coin = {"coin_name": "Duplicate Coin", "is_complete": False}
            client.post("/api/coins", json=coin)
            
            response = client.post("/api/coins", json=coin)
            assert response.status_code == 409

    def test_user_cannot_omit_name(self):
        with api.test_client() as client:
            coin = {"coin_name": "", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            assert response.status_code == 400

    # --- READ ---
    def test_user_can_get_a_coin(self):
        with api.test_client() as client:
            response = client.get("/api/coins")
            assert response.status_code == 200

    def test_get_coins_master_view_includes_linked_duties(self, linked_data_setup):
        with api.test_client() as client:
            response = client.get("/api/coins")
            assert response.status_code == 200
            data = response.json

            assert len(data) == 2 # type: ignore
            
            coin_a_data = next(coin for coin in data if coin["coin_name"] == "Coin A") # type: ignore
            
            assert "duties" in coin_a_data
            assert len(coin_a_data["duties"]) == 2
            
            duty_names = [d["duty_name"] for d in coin_a_data["duties"]]
            assert "Duty 1" in duty_names
            assert "Duty 2" in duty_names

    # --- UPDATE ---
    def test_user_can_update_a_coin_name(self):
        with api.test_client() as client:
            coin = {"coin_name": "Old Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin) 
            coin_uuid = response.json["coin_id"] # type: ignore

            new_data = {"coin_name": "New Coin"}
            response = client.patch(f"/api/coins/{coin_uuid}", json=new_data)
            assert response.status_code == 200

    def test_user_can_mark_coin_completed(self):
        with api.test_client() as client:
            coin = {"coin_name": "Completion Test Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            coin_uuid = response.json["coin_id"] # type: ignore

            new_data = {"is_complete": True}
            new_response = client.patch(f"/api/coins/{coin_uuid}", json=new_data)
            completed_coin = new_response.json

            assert new_response.status_code == 200
            assert completed_coin["is_complete"] == True # type: ignore

    def test_user_cannot_update_a_nonexistant_coin(self):
        with api.test_client() as client:
            new_data = {"coin_name": "New Coin"}
            response = client.patch(f"/api/coins/{uuid.uuid4()}", json=new_data)
            assert response.status_code == 404

            coin_uuid = uuid.uuid4()
            response = client.patch(f"/api/coins/{coin_uuid}", json={"is_complete": True})
            assert response.status_code == 404

    def test_user_cannot_mark_a_nonexistent_coin_complete(self):
        with api.test_client() as client:
            coin_uuid = uuid.uuid4()
            response = client.patch(f"/api/coins/{coin_uuid}", json={"is_complete": True})
            assert response.status_code == 404

    def test_user_cannot_update_a_coin_with_a_duplicate_name(self):
        with api.test_client() as client:
            client.post("/api/coins", json={"coin_name": "Coin Alpha", "is_complete": False})

            response = client.post("/api/coins", json={"coin_name": "Coin Beta", "is_complete": False})
            coin_2_uuid = response.json["coin_id"] # type: ignore

            new_data = {"coin_name": "Coin Alpha"}
            new_response = client.patch(f"/api/coins/{coin_2_uuid}", json=new_data)
            assert new_response.status_code == 409

    def test_user_cannot_update_a_coin_with_an_empty_name(self):
        with api.test_client() as client:
            response = client.post("/api/coins", json={"coin_name": "Old Coin"})
            coin_uuid = response.json["coin_id"] # type: ignore

            new_data = {"coin_name": ""}
            new_response = client.patch(f"/api/coins/{coin_uuid}", json=new_data)
            assert new_response.status_code == 400

    # --- DELETE ---
    def test_user_can_delete_a_coin(self):
        with api.test_client() as client:
            coin = {"coin_name": "Coin to Delete", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            coin_uuid = response.json["coin_id"] # type: ignore

            response = client.delete(f"/api/coins/{coin_uuid}")
            assert response.status_code == 204

    def test_user_cannot_delete_a_nonexistent_coin(self):
        with api.test_client() as client:
            response = client.delete(f"/api/coins/{uuid.uuid4()}")
            assert response.status_code == 404


class TestDutyAPI:
    # --- CREATE ---
    def test_user_can_create_a_duty(self):
        with api.test_client() as client:
            coin = {"coin_name": "Duty Parent Coin", "is_complete": False}
            coin_response = client.post("/api/coins", json=coin)
            coin_uuid = coin_response.json["coin_id"] # type: ignore

            duty = {"duty_name": "New Duty", "duty_desc": "New Desc", "coin_id": coin_uuid}
            duty_response = client.post("/api/duties", json=duty)
            assert duty_response.status_code == 201

    def test_user_cannot_omit_duty_name(self):
        with api.test_client() as client:
            duty = {"duty_name": "", "duty_desc": "Description"}
            response = client.post("/api/duties", json=duty)
            assert response.status_code == 400

    def test_user_cannot_create_duty_with_empty_description(self):
        with api.test_client() as client:
            coin = {"coin_name": "Duty Parent Coin", "is_complete": False}
            coin_response = client.post("/api/coins", json=coin)
            coin_uuid = coin_response.json["coin_id"] # type: ignore

            duty = {"duty_name": "New Duty", "duty_desc": "", "coin_id": coin_uuid}
            duty_response = client.post("/api/duties", json=duty)
            assert duty_response.status_code == 400

    def test_user_cannot_create_duty_with_a_nonexistent_coin(self):
        with api.test_client() as client:
            duty = {"duty_name": "New Duty", "duty_desc": "Desc", "coin_id": str(uuid.uuid4())}
            response = client.post("/api/duties", json=duty)
            assert response.status_code == 404

    # --- READ ---
    def test_user_can_get_all_duties(self):
        with api.test_client() as client:
            Duty.create(duty_name="Duty 1", duty_desc="Desc 1")
            Duty.create(duty_name="Duty 2", duty_desc="Desc 2")

            response = client.get("/api/duties")
            assert response.status_code == 200
            assert len(response.json) == 2 # type: ignore

    def test_user_can_get_a_single_duty(self):
        duty = Duty.create(duty_name="Unique Duty", duty_desc="Desc")
        with api.test_client() as client:
            response = client.get(f"/api/duties/{duty.duty_id}")
            assert response.status_code == 200
            assert response.json["duty_name"] == "Unique Duty" # type: ignore

    def test_get_single_duty_detail_view_includes_linked_coins(self, linked_data_setup):
            target_duty = linked_data_setup["duty_2"] 

            with api.test_client() as client:
                response = client.get(f"/api/duties/{target_duty.duty_id}")
                assert response.status_code == 200
                data = response.json

                assert data["duty_name"] == "Duty 2" # type: ignore
                assert "coins" in data # type: ignore
                assert len(data["coins"]) == 2 # type: ignore
                
                coin_names = [coin["coin_name"] for coin in data["coins"]] # type: ignore
                assert "Coin A" in coin_names
                assert "Coin B" in coin_names

    def test_user_cannot_get_a_nonexistent_duty(self):
        with api.test_client() as client:
            response = client.get(f"/api/duties/{uuid.uuid4()}")
            assert response.status_code == 404

    # --- UPDATE ---
    def test_user_can_update_a_duty_description(self):
        with api.test_client() as client:
            duty = Duty.create(duty_name="Duty to Update", duty_desc="Old Desc")
            new_data = {"duty_desc": "New Desc"}
            response = client.patch(f"/api/duties/{duty.duty_id}", json=new_data)
            assert response.status_code == 200
            
            updated_duty = Duty.get(Duty.duty_id == duty.duty_id)
            assert updated_duty.duty_desc == "New Desc"

    def test_user_cannot_update_a_duty_description_with_empty_value(self):
        with api.test_client() as client:
            duty = Duty.create(duty_name="Duty to Update", duty_desc="Old Desc")
            new_data = {"duty_desc": ""}
            response = client.patch(f"/api/duties/{duty.duty_id}", json=new_data)
            assert response.status_code == 400

    def test_user_cannot_update_description_of_a_nonexistent_duty(self):
        with api.test_client() as client:
            new_data = {"duty_desc": "New Desc"}
            response = client.patch(f"/api/duties/{uuid.uuid4()}", json=new_data)
            assert response.status_code == 404


class TestCoinDutyLinkAPI:
    # --- CREATE (Linkages only expose a create endpoint in these tests) ---
    def test_user_can_link_duty_to_coin(self):
        with api.test_client() as client:
            duty = Duty.create(duty_name="Test Duty", duty_desc="Test Desc")
            coin = {"coin_name": "Link Test Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            coin_uuid = response.json["coin_id"] # type: ignore

            link_data = {"duty_id": str(duty.duty_id)}
            link_response = client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)
            assert link_response.status_code == 201

    def test_user_cannot_link_duty_without_duty_id(self):
        with api.test_client() as client:
            coin_uuid = uuid.uuid4()
            response = client.post(f"/api/coins/{coin_uuid}/duties", json={})
            assert response.status_code == 400

    def test_user_cannot_link_duty_to_a_nonexistent_coin(self):
        with api.test_client() as client:
            duty = Duty.create(duty_name="Test Duty", duty_desc="A test description")
            coin_uuid = uuid.uuid4()
            link_data = {"duty_id": str(duty.duty_id)}
            response = client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)
            assert response.status_code == 404

    def test_user_cannot_link_a_nonexistent_duty_to_a_coin(self):
        with api.test_client() as client:
            coin = {"coin_name": "Link Test Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            coin_uuid = response.json["coin_id"] # type: ignore

            link_data = {"duty_id": str(uuid.uuid4())}
            response2 = client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)
            assert response2.status_code == 404

    def test_user_cannot_create_a_duplicate_linkage(self):
        with api.test_client() as client:
            duty = Duty.create(duty_name="Test Duty", duty_desc="Test Desc")
            coin = {"coin_name": "Duplicate Link Coin", "is_complete": False}
            response = client.post("/api/coins", json=coin)
            coin_uuid = response.json["coin_id"] # type: ignore

            link_data = {"duty_id": str(duty.duty_id)}
            client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)
            
            response2 = client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)
            assert response2.status_code == 409