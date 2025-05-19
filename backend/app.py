from flask import Flask
from blueprints.auth import auth_blueprint
from blueprints.ai import ai_blueprint
from blueprints.payment import payment_blueprint
from blueprints.status import status_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(ai_blueprint, url_prefix='/ai')
    app.register_blueprint(payment_blueprint, url_prefix='/payment')
    app.register_blueprint(status_blueprint, url_prefix='/status')

    return app
