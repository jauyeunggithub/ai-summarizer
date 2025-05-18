from flask import Blueprint, jsonify


status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/', methods=['GET'])
def get_status_view():
    return jsonify({'status': 'ok'}), 200
