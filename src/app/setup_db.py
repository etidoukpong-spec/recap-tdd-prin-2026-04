import json

from src.app.models import db, Coin, Duty, Junction

def init_db():
    with open('src/app/seed_data.json') as json_data:
        seed_data = json.load(json_data)
        all_duties = seed_data['duties']
    if db.is_closed():
        db.connect()
        
    db.drop_tables([Coin, Duty, Junction], safe=True)
    db.create_tables([Coin, Duty, Junction], safe=True)
    
    print("Tables created successfully in the 'coins' schema!")

    Duty.insert_many(all_duties).execute()

    print("Duties seeded successfully in the 'duties' table!")
    
    
    db.close()

if __name__ == "__main__":
    init_db()