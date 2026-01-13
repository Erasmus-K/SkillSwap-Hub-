import api from './axios'

export const skillApi = {
  getSkills: () => api.get('/skills'),
  getSkill: (id) => api.get(`/skills/${id}`),
  createSkill: (skillData) => api.post('/skills', skillData),
  updateSkill: (id, skillData) => api.put(`/skills/${id}`, skillData),
  deleteSkill: (id) => api.delete(`/skills/${id}`),
  searchSkills: (query) => api.get(`/skills/search?q=${query}`),
}