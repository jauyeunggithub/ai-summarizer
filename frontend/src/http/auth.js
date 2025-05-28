import apiClient from '@/plugins/axios'

export const login = ({ email, password }) => {
  return apiClient.post('/auth/login', {
    email,
    password,
  })
}

export const signup = ({
  email,
  username,
  password,
  firstName,
  lastName,
  paymentMethodId,
  priceId,
}) => {
  return apiClient.post('/auth/signup', {
    email,
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

export const getPasswordResetToken = ({ email }) => {
  return apiClient.post('/auth/generate_password_reset_token', { email })
}

export const resetPassword = ({ passwordResetToken, password }) => {
  return apiClient.post('/auth/reset_password', { passwordResetToken, password })
}
