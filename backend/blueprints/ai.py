from flask import Blueprint, jsonify
from ..background_tasks.ai_summary import generate_ai_summary
from ..helpers.auth import jwt_required


ai_blueprint = Blueprint('ai', __name__)


@ai_blueprint.route('/generate_summary', methods=['POST'])
@jwt_required
def generate_summary_view():
    message = "Hello, RabbitMQ!"
    generate_ai_summary(message)
    return jsonify({}), 200
