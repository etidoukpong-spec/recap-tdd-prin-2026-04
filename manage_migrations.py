import os
import sys

os.environ["TESTING"] = "False"

from peewee_migrate import Router
from src.app.database import db, init_db
import src.app.models as models

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_migrations.py [create <name> | migrate]")
        sys.exit(1)

    command = sys.argv[1]

    init_db()
    db.connect()

    db.execute_sql("CREATE SCHEMA IF NOT EXISTS coins;")
    db.execute_sql("SET search_path TO coins;")

    router = Router(db, migrate_dir='src/migrations', ignore=['basemodel', 'base_model'])

    if command == "create":
        if len(sys.argv) < 3:
            print("Error: Provide a name. Example: python manage_migrations.py create initial")
            sys.exit(1)
        name = sys.argv[2]
        router.create(name, auto=models)
        print(f"Migration '{name}' generated in src/migrations/.")

    elif command == "migrate":
        router.run()
        print("Database migrated successfully.")

    db.close()

if __name__ == "__main__":
    main()