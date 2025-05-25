from flask import Blueprint, jsonify, request
from background_tasks.ai_summary import generate_ai_summary
from helpers.auth import jwt_required
from helpers.storage import upload_file_to_s3
from repos.summaries import create_summary, count_summary_results_and
import os
import uuid
import datetime
from constants.summary import StatusEnum
from models.summary import Summary
from datetime import date
import calendar
from werkzeug.utils import secure_filename


ai_blueprint = Blueprint('ai', __name__)


MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB'))
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
MAX_SUMMARIES_PER_MONTH = int(os.getenv('MAX_SUMMARIES_PER_MONTH', 50))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@ai_blueprint.route('/generate_summary', methods=['POST'])
@jwt_required
def generate_summary_view():
    today = date.today()
    first_day = date(today.year, today.month, 1)
    last_day = date(today.year, today.month,
                    calendar.monthrange(today.year, today.month)[1])
    conditions = [
        Summary.created >= first_day,
        Summary.created <= last_day,
        Summary.user_id == request.user.id
    ]
    if count_summary_results_and(conditions) >= MAX_SUMMARIES_PER_MONTH:
        return jsonify({"success": False, "error": "You have reached the limit for summary generation for this month"}), 400

    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"}), 400

    file = request.files['file']
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    if file_length > MAX_FILE_SIZE_BYTES:
        return jsonify({
            "success": False,
            "error": f"File size exceeds limit of {MAX_FILE_SIZE_MB} MB"
        }), 400

    filename = secure_filename(file.filename)
    temp_path = os.path.join("/tmp", filename)
    file.save(temp_path)

    result = upload_file_to_s3(temp_path, S3_BUCKET_NAME)

    text_to_summarize = request.form.get('textToSummarize')
    summary_id = str(uuid.uuid4())
    summary_args = {
        'id': summary_id,
        'user_id': request.user.id,
        'file_path': result['url'],
        'text_to_summarize': text_to_summarize,
        'created': datetime.datetime.now(datetime.timezone.utc),
        'status': StatusEnum.PROCESSING.value,
        'file_name': file.filename,
    }
    create_summary(**summary_args)
    args = {
        'summary_id': summary_id,
        'temp_path': temp_path,
        'text_to_summarize': text_to_summarize,
    }
    generate_ai_summary(**args)
    return jsonify(result), (200 if result["success"] else 500)
