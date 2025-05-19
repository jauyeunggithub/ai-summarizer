from flask import Blueprint, jsonify, request
from helpers.payment import (
    get_active_prices,
    create_subscription,
    cancel_subscription,
    create_customer_with_payment_method
)
from helpers.auth import jwt_required


payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/get_active_prices', methods=['GET'])
def get_active_prices_view():
    return jsonify(get_active_prices()), 200


@jwt_required
def create_subscription_view():
    data = request.get_json()
    email = data.get('email')
    payment_method_id = data.get('payment_method_id')
    price_id = data.get('price_id')
    customer = create_customer_with_payment_method(email, payment_method_id)
    create_subscription(customer.id, payment_method_id, price_id)
    return jsonify(), 200


@payment_blueprint.route('/cancel_subscription', methods=['POST'])
@jwt_required
def cancel_subscription_view():
    cancel_subscription(request.user.subscription_id)
    return jsonify(), 200
