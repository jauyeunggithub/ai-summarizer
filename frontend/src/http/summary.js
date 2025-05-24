import apiClient from '@/plugins/axios'

export const getSummaries = () => {
  return apiClient.get('/summary/all')
}
