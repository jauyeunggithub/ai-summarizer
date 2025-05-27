from flask import Blueprint, jsonify, request
from helpers.auth import jwt_required
from repos.summaries import (
    get_paginated_summary_results,
    count_summary_results,
    update_summary,
    get_summary,
)
from models.summary import Summary
from helpers.storage import delete_s3_file_from_url


summary_blueprint = Blueprint('summary', __name__)


@summary_blueprint.route('/all', methods=['GET'])
@jwt_required
def get_summary_view():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    keyword = request.args.get('keyword')
    conditions = [
        Summary.user_id == request.user.id
    ]
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
            'status': result.status,
        }
        response_results.append(result_dict)
    response_dict = {
        'results': response_results,
        'totalCount': total_count,
    }
    return jsonify(response_dict), 200


@summary_blueprint.route('/delete/<summary_id>', methods=['DELETE'])
@jwt_required
def delete_summary_view(summary_id):
    summary = get_summary(summary_id)
    update_summary(summary_id=summary_id, is_deleted=True)
    delete_s3_file_from_url(summary['file_path'])
    response_dict = {
        'summaryId': summary_id,
    }
    return jsonify(response_dict), 200
