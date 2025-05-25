import apiClient from '@/plugins/axios'

export const getSummaries = ({ page = 1, perPage = 10, keyword }) => {
  return apiClient.get('/summary/all', { params: { page, perPage, keyword } })
}
