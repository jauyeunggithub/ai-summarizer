from flask import Blueprint, jsonify, request
from helpers.auth import jwt_required
from repos.summaries import get_paginated_summary_results


summary_blueprint = Blueprint('summary', __name__)


@summary_blueprint.route('/', methods=['GET'])
@jwt_required
def get_summary_view():
    data = request.get_json()
    page = data.get('page')
    result = get_paginated_summary_results(page)
    return jsonify(result), 200
