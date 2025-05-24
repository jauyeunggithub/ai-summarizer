import apiClient from '@/plugins/axios'

export const login = ({ username, password }) => {
  return apiClient.post('/auth/login', {
    username,
    password,
  })
}

export const signup = ({ username, password, firstName, lastName, paymentMethodId, priceId }) => {
  return apiClient.post('/auth/signup', {
    username,
    password,
    firstName,
    lastName,
    paymentMethodId,
    priceId,
  })
}
