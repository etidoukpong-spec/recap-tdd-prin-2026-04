import uuid, os, dotenv
from peewee import *

dotenv.load_dotenv()

db = PostgresqlDatabase(
    "etido",
    user="etido",
    port=25060,
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASSWORD"),
)

class BaseModel(Model):
    class Meta:
        database = db

class Duty(BaseModel): 
    duty_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_name = CharField(unique=True)
    duty_desc = CharField()

    class Meta:
        schema = 'coins'
        table_name = 'duty'

    
class Coin(BaseModel):
    coin_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    coin_name = CharField(unique=True)
    is_complete = BooleanField()

    class Meta:
        schema = 'coins'
        table_name = 'coin'

class Junction(BaseModel):
    junction_id = UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    duty_id = ForeignKeyField(Duty, on_delete="CASCADE")
    coin_id = ForeignKeyField(Coin, on_delete="CASCADE")

    class Meta:
        schema = 'coins'
        table_name = 'coin_duty_junction'
