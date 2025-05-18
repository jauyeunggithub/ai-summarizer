from flask import Blueprint, jsonify
from background_tasks.ai_summary import generate_ai_summary


ai_blueprint = Blueprint('ai', __name__)


@ai_blueprint.route('/generate_summary', methods=['POST'])
def generate_summary():
    message = "Hello, RabbitMQ!"
    generate_ai_summary(message)
    return jsonify({}), 200
