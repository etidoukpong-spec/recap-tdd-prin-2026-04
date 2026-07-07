from flask import Flask, request, jsonify
from peewee import IntegrityError
from src.app.models import CoinModel, DutyModel, Junction

api = Flask(__name__)

@api.post("/api/coins")
def create_coin():
    data = request.get_json()
    coin_name = data.get("coin_name", "").strip()
    
    if not coin_name:
        return jsonify({"error": "coin_name is required"}), 400

    try:
        coin = CoinModel.create(
            coin_name=coin_name, 
            is_complete=data.get("is_complete", False)
        )
        return jsonify({
            "coin_id": str(coin.coin_id), 
            "coin_name": coin.coin_name, 
            "is_complete": coin.is_complete
        }), 201
    except IntegrityError:
        return jsonify({"error": "Coin with this name already exists"}), 409


@api.get("/api/coins")
def get_coin():
    coins = CoinModel.select()
    response_data = [
        {
            "coin_id": str(coin.coin_id), 
            "coin_name": coin.coin_name, 
            "is_complete": coin.is_complete
        } for coin in coins
    ]
    return jsonify(response_data), 200


@api.put("/api/coins/<id>")
def update_coin(id):
    data = request.get_json()
    
    try:
        coin = CoinModel.get(CoinModel.coin_id == id)
        
        if "coin_name" in data:
            new_name = data["coin_name"].strip()
            if not new_name:
                return jsonify({"error": "coin_name cannot be empty"}), 400
            coin.coin_name = new_name
            
        if "is_complete" in data:
            coin.is_complete = data["is_complete"]
            
        coin.save()
        
        return jsonify({
            "coin_id": str(coin.coin_id), 
            "coin_name": coin.coin_name, 
            "is_complete": coin.is_complete
        }), 200
        
    except CoinModel.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    except IntegrityError:
        return jsonify({"error": "Coin with this name already exists"}), 409


@api.delete("/api/coins/<id>")
def delete_coin(id):
    try:
        coin = CoinModel.get(CoinModel.coin_id == id)
        coin.delete_instance()
        return '', 204
    except CoinModel.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404


@api.patch("/api/coins/<id>") 
def mark_complete(id):
    data = request.get_json()
    
    try:
        coin = CoinModel.get(CoinModel.coin_id == id)
        
        if "is_complete" in data:
            coin.is_complete = data["is_complete"]
            coin.save()
            
        return jsonify({
            "coin_id": str(coin.coin_id), 
            "coin_name": coin.coin_name, 
            "is_complete": coin.is_complete
        }), 200
        
    except CoinModel.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404


@api.post("/api/coins/<id>/duties")
def link_duty_to_coin(id):
    data = request.get_json()
    duty_id = data.get("duty_id")
    
    if not duty_id:
        return jsonify({"error": "duty_id is required"}), 400
        
    try:
        coin = CoinModel.get(CoinModel.coin_id == id)
        duty = DutyModel.get(DutyModel.duty_id == duty_id)
        
        Junction.create(coin_id=coin, duty_id=duty)
        
        return jsonify({"message": "Duty successfully linked to coin"}), 201
        
    except CoinModel.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    except DutyModel.DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404
    except IntegrityError:
        return jsonify({"error": "This linkage already exists"}), 409