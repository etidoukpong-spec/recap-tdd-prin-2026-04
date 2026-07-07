import uuid
from peewee import *
from src.app.config import DB_CONFIG

db = PostgresqlDatabase(**DB_CONFIG)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class DutyModel(BaseModel): 
    duty_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_name = CharField(unique=True)
    duty_desc = CharField()

    
class CoinModel(BaseModel):
    coin_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    coin_name = CharField(unique=True)
    is_complete = BooleanField()

class Junction(BaseModel):
    junction_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_id = ForeignKeyField(DutyModel, on_delete="CASCADE")
    coin_id = ForeignKeyField(CoinModel, on_delete="CASCADE")
