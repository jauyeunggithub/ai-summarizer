from flask import Blueprint, Response, request
import requests


file_blueprint = Blueprint('file', __name__)


@file_blueprint.route('/fetch_file', methods=['GET'])
def fetch_file_view():
    url = request.args.get('url')
    r = requests.get(url)

    return Response(
        r.content,
        content_type=r.headers.get('Content-Type', 'application/octet-stream')
    )
