import apiClient from '@/plugins/axios'

export const getActivePrices = async () => {
  return apiClient.get('/payment/get_active_prices')
}
