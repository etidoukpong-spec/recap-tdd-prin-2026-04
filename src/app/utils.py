def format_coin_response(coin):
    return {
        "coin_id": str(coin.coin_id), 
        "coin_name": coin.coin_name, 
        "is_complete": coin.is_complete
    }

def format_duty_response(duty):
    return {
        "duty_id": str(duty.duty_id),
        "duty_name": duty.duty_name,
        "duty_desc": duty.duty_desc
    }