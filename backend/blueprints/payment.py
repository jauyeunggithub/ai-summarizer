from flask import Blueprint, jsonify, request
from helpers.payment import (
    get_active_prices,
    renew_subscrption,
    cancel_subscription,
)
from helpers.auth import jwt_required


payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/get_active_prices', methods=['GET'])
def get_active_prices_view():
    return jsonify(get_active_prices()), 200


@payment_blueprint.route('/renew_subscription', methods=['GET'])
@jwt_required
def renew_subscription_view():
    data = request.get_json()
    customer_id = data.get('customerId')
    price_id = data.get('priceId')
    renew_subscrption(customer_id, price_id)
    return jsonify(), 200


@payment_blueprint.route('/cancel_subscription', methods=['POST'])
@jwt_required
def cancel_subscription_view():
    cancel_subscription(request.user.subscription_id)
    return jsonify(), 200
