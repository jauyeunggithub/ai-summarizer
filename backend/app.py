import os
from flask import Flask
from blueprints.auth import auth_blueprint


app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')


@app.route('/')
def index():
    return 'Flask + RabbitMQ Listener is running!'
