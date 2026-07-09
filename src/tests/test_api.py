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
    

def test_user_can_get_a_coin():
    with api.test_client() as client:
        response = client.get("/api/coins")

        assert response.status_code == 200

def test_user_can_create_a_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        assert response.status_code == 201

def test_user_can_update_a_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = response.json["coin_id"]

        new_data = {"coin_name": "Test Coin2"}
        response = client.put(f"/api/coins/{coin_uuid}", json=new_data)

        assert response.status_code == 200

def test_user_can_delete_a_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = response.json["coin_id"]

        response = client.delete(f"/api/coins/{coin_uuid}")

        assert response.status_code == 204

def test_user_cannot_create_a_duplicate_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        client.post("/api/coins", json=coin)

        response2 = client.post("/api/coins", json=coin)

        assert response2.status_code == 409

def test_user_cannot_omit_name():
    with api.test_client() as client:
        coin = {"coin_name": "", "is_complete": False}
        response = client.post("/api/coins", json=coin)

        assert response.status_code == 400

def test_user_cannot_update_a_nonexistant_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = uuid.uuid4()

        new_data = {"coin_name": "Test Coin2"}
        response = client.put(f"/api/coins/{coin_uuid}", json=new_data)

        assert response.status_code == 404

def test_user_cannot_delete_a_nonexistent_coin():
    with api.test_client() as client:
        coin = {"coin_name": "Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = uuid.uuid4()

        response = client.delete(f"/api/coins/{coin_uuid}")

        assert response.status_code == 404

def test_user_can_mark_coin_completed():
    with api.test_client() as client:
        coin = {"coin_name": "Completion Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = response.json["coin_id"]

        patch_data = {"is_complete": True}
        patch_response = client.patch(f"/api/coins/{coin_uuid}", json=patch_data)

        assert patch_response.status_code == 200
        assert patch_response.json["is_complete"] == True

def test_user_can_link_duty_to_coin():
    duty = Duty.create(duty_name="Test Duty", duty_desc="A test description")
    
    with api.test_client() as client:
        coin = {"coin_name": "Link Test Coin", "is_complete": False}
        response = client.post("/api/coins", json=coin)
        coin_uuid = response.json["coin_id"]

        link_data = {"duty_id": str(duty.duty_id)}
        link_response = client.post(f"/api/coins/{coin_uuid}/duties", json=link_data)

        assert link_response.status_code == 201