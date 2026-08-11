from flask import Flask, request, jsonify
from peewee import IntegrityError
from src.app.models import Coin, Duty, Junction

api = Flask(__name__)

@api.get("/")
def health():
    return "Healthy"

@api.post("/api/coins")
def create_coin():
    data = request.get_json()
    coin_name = data.get("coin_name", "").strip()
    
    if not coin_name:
        return jsonify({"error": "coin_name is required"}), 400

    try:
        coin = Coin.create(
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
    coins = Coin.select()
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
        coin = Coin.get(Coin.coin_id == id)
        
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
        
    except Coin.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    except IntegrityError:
        return jsonify({"error": "Coin with this name already exists"}), 409


@api.delete("/api/coins/<id>")
def delete_coin(id):
    try:
        coin = Coin.get(Coin.coin_id == id)
        coin.delete_instance()
        return '', 204
    except Coin.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404


@api.patch("/api/coins/<id>") 
def mark_complete(id):
    data = request.get_json()
    
    try:
        coin = Coin.get(Coin.coin_id == id)
        
        if "is_complete" in data:
            coin.is_complete = data["is_complete"]
            coin.save()
            
        return jsonify({
            "coin_id": str(coin.coin_id), 
            "coin_name": coin.coin_name, 
            "is_complete": coin.is_complete
        }), 200
        
    except Coin.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404


@api.post("/api/coins/<id>/duties")
def link_duty_to_coin(id):
    data = request.get_json()
    duty_id = data.get("duty_id")
    
    if not duty_id:
        return jsonify({"error": "duty_id is required"}), 400
        
    try:
        coin = Coin.get(Coin.coin_id == id)
        duty = Duty.get(Duty.duty_id == duty_id)
        
        Junction.create(coin_id=coin, duty_id=duty)
        
        return jsonify({"message": "Duty successfully linked to coin"}), 201
        
    except Coin.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    except Duty.DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404
    except IntegrityError:
        return jsonify({"error": "This linkage already exists"}), 409
    
@api.post("/api/duties")
def create_duty():
    data = request.get_json()
    duty_name = data.get("duty_name", "").strip()
    duty_desc = data.get("duty_desc", "").strip()
    coin_id = data.get("coin_id", "")

    if not duty_name:
        return jsonify({"error": "duty_name is required"}), 400

    try:
        coin = Coin.get(Coin.coin_id == coin_id)
        duty = Duty.create(
            duty_name=duty_name, 
            duty_desc=duty_desc
        )

        Junction.create(coin_id=coin, duty_id=duty)

        return jsonify({"message": "Duty successfully created and linked to coin"}), 201
    except Coin.DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    except IntegrityError:
        return jsonify({"error": "This duty or linkage already exists"}), 409

@api.get("/api/duties")
def get_all_duties():
    duties = Duty.select()
    response_data = [
        {
            "duty_id": str(duty.duty_id),
            "duty_name": duty.duty_name,
            "duty_desc": duty.duty_desc
        }
        for duty in duties
    ]
    return jsonify(response_data), 200

@api.get("/api/duties/<id>")
def get_single_duty(id):
    try:
        duty = Duty.get(Duty.duty_id == id)
        response_data = {
            "duty_id": str(duty.duty_id),
            "duty_name": duty.duty_name,
            "duty_desc": duty.duty_desc
        }
        return jsonify(response_data), 200
    except Duty.DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404
    
@api.put("/api/duties/<id>")
def update_duty_desc(id):
    data = request.get_json()
    new_desc = data.get("duty_desc")

    if not new_desc:
        return jsonify({"error": "duty_desc is required"}), 400
    
    try:
        duty = Duty.get(Duty.duty_id == id)
        duty.duty_desc = new_desc
        duty.save()
        return jsonify({"message": "Duty description successfully updated"}), 200
    except Duty.DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404
