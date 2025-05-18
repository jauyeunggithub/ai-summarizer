from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
