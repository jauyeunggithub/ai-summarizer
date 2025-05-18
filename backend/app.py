from flask import Flask
from blueprints.auth import auth_blueprint
from blueprints.ai import ai_blueprint


app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(ai_blueprint, url_prefix='/ai')


@app.route('/')
def index():
    return 'Flask + RabbitMQ Listener is running!'
