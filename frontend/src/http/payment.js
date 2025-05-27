import apiClient from '@/plugins/axios'

export const getActivePrices = async () => {
  return apiClient.get('/payment/get_active_prices')
}

export const createSetupIntent = async () => {
  return apiClient.post('/payment/create_setup_intent')
}

export const attachPaymentMethods = async ({ paymentMethodId }) => {
  return apiClient.post('/payment/attach_payment_method', {
    paymentMethodId,
  })
}

export const cancelSubscription = async () => {
  return apiClient.post('/payment/cancel_subscription')
}

export const getPaymentDetails = async () => {
  return apiClient.get('/payment/get_payment_details')
}

export const getSubscriptionStatus = async () => {
  return apiClient.get('/payment/get_subscription_status')
}

export const renewSubscription = async ({ priceId }) => {
  return apiClient.post('/payment/renew_subscription', {
    priceId,
  })
}
