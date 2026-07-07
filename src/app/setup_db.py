from src.app.models import db, Coin, Duty, Junction

def init_db():
    db.connect()
    db.create_tables([Coin, Duty, Junction], safe=True)
    
    print("Tables created successfully in the 'coins' schema!")
    
    db.close()

if __name__ == "__main__":
    init_db()