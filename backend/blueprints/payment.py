from flask import Blueprint, jsonify, request
from helpers.payment import (
    get_active_prices,
    renew_subscription,
    cancel_subscription,
    create_setup_intent,
    attach_payment_method,
    get_payment_details,
    get_subscription_status,
    is_subscription_paid
)
from helpers.auth import jwt_required
from repos.users import update_user


payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/get_active_prices', methods=['GET'])
def get_active_prices_view():
    return jsonify(get_active_prices()), 200


@payment_blueprint.route('/renew_subscription', methods=['POST'])
@jwt_required
def renew_subscription_view():
    data = request.get_json()
    customer_id = request.user.customer_id
    price_id = data.get('priceId')
    subscription_id = renew_subscription(customer_id, price_id)
    update_user(
        id=request.user.id,
        subscription_id=subscription_id,
        is_active=True
    )
    return jsonify(), 200


@payment_blueprint.route('/cancel_subscription', methods=['POST'])
@jwt_required
def cancel_subscription_view():
    cancel_subscription(request.user.subscription_id)
    update_user(id=request.user.id, is_active=False, subscription_id=None)
    return jsonify(), 200


@payment_blueprint.route('/create_setup_intent', methods=['POST'])
@jwt_required
def create_setup_intent_view():
    customer_id = request.user.customer_id
    try:
        setup_intent = create_setup_intent(customer_id)
        return jsonify({'clientSecret': setup_intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payment_blueprint.route('/attach_payment_method', methods=['POST'])
@jwt_required
def attach_payment_method_view():
    data = request.get_json()
    customer_id = request.user.customer_id
    payment_method_id = data.get('paymentMethodId')
    try:
        attach_payment_method(payment_method_id, customer_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payment_blueprint.route('/get_payment_details', methods=['GET'])
@jwt_required
def get_payment_details_view():
    customer_id = request.user.customer_id
    card = get_payment_details(customer_id)
    return jsonify({
        'brand': card.brand,
        'last4': card.last4,
        'expMonth': card.exp_month,
        'expYear': card.exp_year,
    })


@payment_blueprint.route('/get_subscription_status', methods=['GET'])
@jwt_required
def get_subscription_status_view():
    subscription_id = request.user.subscription_id
    subscription_dict = get_subscription_status(subscription_id)
    return jsonify(subscription_dict)


@payment_blueprint.route('/is_subscription_paid', methods=['GET'])
@jwt_required
def is_subscription_paid_view():
    subscription_id = request.user.subscription_id
    subscription_paid = is_subscription_paid(subscription_id)
    return jsonify({'paid': subscription_paid})
