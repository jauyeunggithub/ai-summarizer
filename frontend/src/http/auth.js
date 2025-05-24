import apiClient from '@/plugins/axios'

export const login = ({ email, password }) => {
  return apiClient.post('/auth/login', {
    email,
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

export const getCurrentUser = () => {
  return apiClient.get('/auth/current_user')
}
