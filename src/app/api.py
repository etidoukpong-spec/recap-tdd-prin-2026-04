from flask import Flask

api = Flask(__name__)

@api.post("/api/coins")
def create_coin():
    pass

@api.get("/api/coins")
def get_coin():
    pass

@api.put("/api/coins/<id>")
def update_coin(id):
    pass

@api.delete("/api/coins/<id>")
def delete_coin(id):
    pass

@api.patch("/api/coins/<id>") 
def mark_complete():
    pass

@api.post("/api/coins/<id>/duties")
def link_duty_to_coin():
    pass