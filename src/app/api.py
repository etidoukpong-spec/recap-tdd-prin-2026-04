from flask import Flask, request, jsonify
from peewee import IntegrityError, DoesNotExist
from src.app.database import db
from src.app.models import Coin, Duty, Junction, RequestLog
from src.app.utils import format_coin_response, format_duty_response

api = Flask(__name__)

@api.get("/")
def health():
    return jsonify({"message": "Healthy"})

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
        return jsonify(format_coin_response(coin)), 201
    
    except IntegrityError:
        return jsonify({"error": "Coin with this name already exists"}), 409

@api.get("/api/coins")
def get_coins():
    coins = Coin.select()
    response_data = []
    
    for coin in coins:
        linked_duties = Duty.select().join(Junction).where(Junction.coin_id == coin.coin_id)

        coin_data = format_coin_response(coin)
        coin_data["duties"] = [format_duty_response(duty) for duty in linked_duties]
        
        response_data.append(coin_data)
        
    return jsonify(response_data), 200

@api.patch("/api/coins/<id>")
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
            mark_complete = data["is_complete"]

            if not isinstance(mark_complete, bool):
                return jsonify({
                    "error": "Something went wrong: wrong type"
                }), 400

            coin.is_complete = mark_complete
        coin.save()

    except DoesNotExist:
            return jsonify({
                "error": "Something went wrong: no such coin"
            }), 404

    except KeyError:
        return jsonify({
            "error": "Something went wrong: wrong info in payload"
        }), 400

    except IntegrityError:
            return jsonify({"error": "Coin with this name already exists"}), 409

    else:        
        return jsonify(format_coin_response(coin)), 200   

@api.delete("/api/coins/<id>")
def delete_coin(id):
    try:
        coin = Coin.get(Coin.coin_id == id)
        coin.delete_instance()
        return '', 204
    
    except DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404

@api.post("/api/coins/<id>/duties")
def link_duty_to_coin(id):
    data = request.get_json()
    duty_id = data.get("duty_id")
    
    if not duty_id:
        return jsonify({"error": "duty_id is required"}), 400
        
    try:
        coin = Coin.get(Coin.coin_id == id)

    except DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404

    try:
        duty = Duty.get(Duty.duty_id == duty_id)

    except DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404

    try:    
        Junction.create(coin_id=coin, duty_id=duty)

    except IntegrityError:
        return jsonify({"error": "This linkage already exists"}), 409
    
    else: 
        return jsonify({"message": "Duty successfully linked to coin"}), 201

@api.post("/api/duties")
def create_duty():
    data = request.get_json()
    duty_name = data.get("duty_name", "").strip()
    duty_desc = data.get("duty_desc", "").strip()
    coin_id = data.get("coin_id", "")

    if not duty_name:
        return jsonify({"error": "Name is required"}), 400

    if not duty_desc:
        return jsonify({"error": "Description is required"}), 400

    try:
        coin = Coin.get(Coin.coin_id == coin_id)

    except DoesNotExist:
        return jsonify({"error": "Coin not found"}), 404
    
    try:
        with db.atomic():
            duty = Duty.create(
                duty_name=duty_name, 
                duty_desc=duty_desc
            )

            Junction.create(coin_id=coin, duty_id=duty)

    except IntegrityError:
        return jsonify({"error": "This duty or linkage already exists"}), 409
    
    else:
        return jsonify({"message": "Duty successfully created and linked to coin"}), 201

@api.get("/api/duties")
def get_all_duties():
    duties = Duty.select()
    response_data = [format_duty_response(duty) for duty in duties]
    return jsonify(response_data), 200

@api.get("/api/duties/<id>")
def get_single_duty(id):
    try:
        duty = Duty.get(Duty.duty_id == id)

        linked_coins = Coin.select().join(Junction).where(Junction.duty_id == duty.duty_id)

        duty_data = format_duty_response(duty)
        duty_data["coins"] = [format_coin_response(coin) for coin in linked_coins] # type: ignore

        return jsonify(duty_data), 200
    except DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404
    
@api.patch("/api/duties/<id>")
def update_duty_desc(id):
    data = request.get_json()
    try:
        duty = Duty.get(Duty.duty_id == id)
        new_desc = data["duty_desc"]
        if not new_desc:
            return jsonify({"error": "Description is required"}), 400
        duty.duty_desc = new_desc
        duty.save()

        return jsonify({"message": "Duty description successfully updated"}), 200
    
    except DoesNotExist:
        return jsonify({"error": "Duty not found"}), 404

@api.get("/api/audit")
def get_audit_logs():
    logs = (
        RequestLog.select()
        .order_by(RequestLog.timestamp.desc())
        .limit(100)
    )

    response_data = [
        {
            "log_id": str(log.log_id),
            "method": log.method,
            "path": log.path,
            "ip_address": log.ip_address,
            "status_code": log.status_code,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]

    return jsonify(response_data), 200

@api.after_request
def log_request(response):
    try:
        RequestLog.create(
            method=request.method,
            path=request.path,
            ip_address=request.remote_addr or "127.0.0.1",
            status_code=response.status_code
        )
    except Exception:
        pass
        
    return response