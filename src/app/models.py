import uuid
from peewee import *
from src.app.config import test_mode
from src.app.database import db

class BaseModel(Model):
    class Meta:
        schema = "test" if test_mode else "coins"
        database = db

class Duty(BaseModel): 
    duty_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_name = CharField(unique=True)
    duty_desc = CharField()

    class Meta:
        table_name = 'duty'

    
class Coin(BaseModel):
    coin_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    coin_name = CharField(unique=True)
    is_complete = BooleanField(default=False)

    class Meta:
        table_name = 'coin'

class Junction(BaseModel):
    junction_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_id = ForeignKeyField(Duty, backref="coins", on_delete="CASCADE", on_update="CASCADE")
    coin_id = ForeignKeyField(Coin, backref="duties", on_delete="CASCADE", on_update="CASCADE")

    class Meta:
        table_name = 'coin_duty_junction'
        indexes = (
            (('coin_id', 'duty_id'), True),
        )
