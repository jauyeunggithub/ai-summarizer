from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from repos.users import get_user, create_user, update_user
from helpers.payment import create_customer_with_payment_method, create_subscription
from helpers.auth import jwt_required, generate_password_reset_token
from backend.helpers.email import send_plain_text_email
from werkzeug.security import check_password_hash, generate_password_hash
import uuid


auth_blueprint = Blueprint('auth', __name__)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
FRONT_END_PASSWORD_RESET_PAGE_URL = os.getenv(
    'FRONT_END_PASSWORD_RESET_PAGE_URL')


@auth_blueprint.route('/login', methods=['POST'])
def login_view():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = get_user(email)

    if user and check_password_hash(user.hashed_password, password):
        payload = {
            'sub': email,
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@auth_blueprint.route('/signup', methods=['POST'])
def signup_view():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    payment_method_id = data.get('paymentMethodId')
    price_id = data.get('priceId')
    hashed_password = generate_password_hash(password)
    customer = create_customer_with_payment_method(email, payment_method_id)
    subscription = create_subscription(
        customer.id, payment_method_id, price_id
    )
    subscription_id = subscription['id']
    args = {
        'id': str(uuid.uuid4()),
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'subscription_id': subscription_id,
        'hashed_password': hashed_password,
        'customer_id': customer.id,
        'created': datetime.datetime.now(datetime.timezone.utc),
        'is_active': True
    }
    create_user(**args)

    response_dict = args.pop('hashed_password')
    return jsonify(response_dict), 200


@auth_blueprint.route('/generate_password_reset_token', methods=['POST'])
def generate_password_reset_token_view():
    data = request.get_json()
    email = data.get('email')
    password_reset_token = generate_password_reset_token(email)
    password_reset_url = f'{FRONT_END_PASSWORD_RESET_PAGE_URL}?token={password_reset_token}'
    args = {
        'to_email': email,
        'subject': 'Reset summarizerai.online Account Password',
        'message_text': f'Hello {email}. Please go to {password_reset_url}'
    }
    user = get_user(email)
    update_user(id=user.id, password_reset_token=password_reset_token)
    send_plain_text_email(**args)
    response_dict = {'status': 'success'}
    return jsonify(response_dict), 200


@auth_blueprint.route('/current_user', methods=['GET'])
@jwt_required
def current_user_view():
    user = request.user
    response_dict = {
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'subscriptionId': user.subscription_id,
        'created': user.created,
        'customerId': user.customer_id,
    }
    return jsonify(response_dict), 200
