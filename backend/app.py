import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


with open("/run/secrets/db_password.txt", "r") as secret_file:
    db_password = secret_file.read().strip()

db_url = f"postgresql://postgres:{db_password}@db:5432/postgres"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Flask + RabbitMQ Listener is running!'
