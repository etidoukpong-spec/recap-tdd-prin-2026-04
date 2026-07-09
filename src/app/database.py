from peewee import DatabaseProxy, PostgresqlDatabase
from src.app.config import db_kwargs

db = DatabaseProxy()

def init_db():
    psql_db = PostgresqlDatabase(**db_kwargs)
    db.initialize(psql_db)