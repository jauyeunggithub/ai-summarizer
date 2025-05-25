import apiClient from '@/plugins/axios'

export const fetchFile = async ({ url }) => {
  return apiClient.get('/file/fetch_file', { params: { url }, responseType: 'blob' })
}
