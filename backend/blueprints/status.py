from flask import Blueprint, jsonify
import os


status_blueprint = Blueprint('status', __name__)
flask_env = os.getenv('FLASK_ENV')


@status_blueprint.route('/', methods=['GET'])
def get_status_view():
    response = {
        'status': 'ok',
        'env': flask_env,
    }
    return jsonify(response), 200
