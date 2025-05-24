from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from repos.users import get_user, create_user
from helpers.payment import create_customer_with_payment_method, create_subscription
from werkzeug.security import check_password_hash, generate_password_hash


auth_blueprint = Blueprint('auth', __name__)
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


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

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
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
    subscription_id = None
    args = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'subscription_id': subscription_id,
        'hashed_password': hashed_password
    }
    create_user(**args)
    customer = create_customer_with_payment_method(email, payment_method_id)
    create_subscription(customer.id, payment_method_id, price_id)
    response_dict = args.pop('hashed_password')
    return jsonify(response_dict), 200
