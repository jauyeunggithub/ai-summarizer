from flask import Blueprint, jsonify, request
from helpers.auth import jwt_required
from repos.summaries import get_paginated_summary_results


summary_blueprint = Blueprint('summary', __name__)


@summary_blueprint.route('/all', methods=['GET', 'OPTIONS'])
@jwt_required
def get_summary_view():
    page = int(request.args.get('page', 1))
    results = get_paginated_summary_results(page)
    response_results = []
    for result in results:
        result_dict = {
            'id': result.id,
            'userId': result.user_id,
            'filePath': result.file_path,
            'textToSummarize': result.text_to_summarize,
            'created': result.created,
            'summaryResult': result.summary_result,
        }
        response_results.append(result_dict)
    return jsonify(response_results), 200
