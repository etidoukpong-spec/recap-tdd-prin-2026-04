import os, dotenv

dotenv.load_dotenv()

db_kwargs = {
    "database": os.getenv("DB_NAME"),
    "user":os.getenv("DB_USER"),
    "port":os.getenv("DB_PORT"), # int(os.getenv("DB_PORT", 5432)) if TypeError
    "host":os.getenv("DB_HOST"),
    "password":os.getenv("DB_PASSWORD"),
}

test_mode = str(os.getenv("TESTING")).lower() in ("true", "1")