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
                "priceId": price.id,
                "productName": price.product.name if hasattr(price.product, "name") else "Unnamed",
                "unitAmount": price.unit_amount,
                "currency": price.currency,
                "recurringInterval": price.recurring.interval if price.recurring else "one_time"
            }
            price_list.append(price_info)

        return price_list

    except stripe.error.StripeError as e:
        return {"error": str(e)}


def get_subscription_status(subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return {
            "success": True,
            "subscriptionId": subscription.id,
            "status": subscription.status
        }
    except stripe.error.StripeError as e:
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


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
        )

        return subscription
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def renew_subscription(customer_id, price_id):
    new_subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
    )
    return new_subscription['id']


def cancel_subscription(subscription_id):
    try:
        subscription = stripe.Subscription.delete(subscription_id)
        return subscription
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def create_setup_intent(customer_id):
    setup_intent = stripe.SetupIntent.create(
        customer=customer_id,
    )
    return setup_intent


def attach_payment_method(payment_method_id, customer_id):
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id,
    )

    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id,
        }
    )


def get_payment_details(customer_id):
    customer = stripe.Customer.retrieve(customer_id)
    default_pm_id = customer.get(
        "invoice_settings", {}).get("default_payment_method")
    pm = stripe.PaymentMethod.retrieve(default_pm_id)
    card = pm.card
    return card


def get_subscription_status(subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription.to_dict()
    except stripe.error.StripeError as e:
        return f"Stripe error: {e.user_message or str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
