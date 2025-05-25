from flask import Blueprint, jsonify, request
from helpers.auth import jwt_required
from repos.summaries import get_paginated_summary_results, count_summary_results
from models.summary import Summary


summary_blueprint = Blueprint('summary', __name__)


@summary_blueprint.route('/all', methods=['GET'])
@jwt_required
def get_summary_view():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    keyword = request.args.get('keyword')
    conditions = []
    if keyword:
        conditions = [
            Summary.file_name.ilike(f"%{keyword}%"),
            Summary.description.ilike(f"%{keyword}%"),
            Summary.file_path.ilike(f"%{keyword}%"),
            Summary.summary_result.ilike(f"%{keyword}%"),
        ]

    results = get_paginated_summary_results(page, per_page, conditions)
    total_count = count_summary_results(conditions)
    response_results = []
    for result in results:
        result_dict = {
            'id': result.id,
            'userId': result.user_id,
            'filePath': result.file_path,
            'textToSummarize': result.text_to_summarize,
            'created': result.created,
            'summaryResult': result.summary_result,
            'fileName': result.file_name,
            'description': result.description,
        }
        response_results.append(result_dict)
    response_dict = {
        'results': response_results,
        'totalCount': total_count,
    }
    return jsonify(response_dict), 200
