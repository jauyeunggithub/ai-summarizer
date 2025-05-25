import apiClient from '@/plugins/axios'

export const generateSummary = (formData) => {
  return apiClient.post('/ai/generate_summary', formData)
}
