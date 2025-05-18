import stripe
import os


stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = stripe_secret_key


def get_active_prices(limit=10):
    try:
        prices = stripe.Price.list(
            active=True,
            limit=limit,
            expand=["data.product"]
        )

        price_list = []
        for price in prices.auto_paging_iter():
            price_info = {
                "price_id": price.id,
                "product_name": price.product.name if hasattr(price.product, "name") else "Unnamed",
                "unit_amount": price.unit_amount,
                "currency": price.currency,
                "recurring_interval": price.recurring.interval if price.recurring else "one_time"
            }
            price_list.append(price_info)

        return price_list

    except stripe.error.StripeError as e:
        return {"error": str(e)}


def create_customer_with_payment_method(email, payment_method_id):
    try:
        customer = stripe.Customer.create(
            email=email,
        )

        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer.id,
        )

        stripe.Customer.modify(
            customer.id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )

        return customer

    except stripe.error.StripeError as e:
        return {"error": str(e)}


def create_subscription(customer_id, payment_method_id, price_id):
    try:
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )

        stripe.Customer.modify(
            customer_id,
            invoice_settings={'default_payment_method': payment_method_id},
        )

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            expand=['latest_invoice.payment_intent'],
        )

        return subscription
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def cancel_subscription(subscription_id):
    try:
        subscription = stripe.Subscription.delete(subscription_id)
        return subscription
    except stripe.error.StripeError as e:
        return {"error": str(e)}
