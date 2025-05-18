from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


with open("/run/secrets/db_password.txt", "r") as secret_file:
    db_password = secret_file.read().strip()

db_url = f"postgresql://postgres:{db_password}@db:5432/postgres"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
