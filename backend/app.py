from flask import Flask
from flask_cors import CORS
from blueprints.auth import auth_blueprint
from blueprints.ai import ai_blueprint
from blueprints.payment import payment_blueprint
from blueprints.status import status_blueprint
from blueprints.summary import summary_blueprint
from blueprints.file import file_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(ai_blueprint, url_prefix='/ai')
    app.register_blueprint(payment_blueprint, url_prefix='/payment')
    app.register_blueprint(status_blueprint, url_prefix='/status')
    app.register_blueprint(summary_blueprint, url_prefix='/summary')
    app.register_blueprint(file_blueprint, url_prefix='/file')

    return app
