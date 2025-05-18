from flask import Flask
from .blueprints.auth import auth_blueprint
from .blueprints.ai import ai_blueprint
import os


def create_app():
    app = Flask(__name__)
    app.config["REDIS_URL"] = os.getenv('REDIS_URL', 'redis://redis:6379/0')

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(ai_blueprint, url_prefix='/ai')

    return app
