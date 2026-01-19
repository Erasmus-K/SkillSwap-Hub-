import api from './axios'

export const skillTagsApi = {
  getSkillTags: () => api.get('/skill-tags/'),
  createSkillTag: (skillTag) => api.post('/skill-tags/', skillTag),
  addUserSkill: (userSkill) => api.post('/skill-tags/user-skills', userSkill),
  getMySkills: () => api.get('/skill-tags/user-skills/me'),
  removeUserSkill: (skillTagId) => api.delete(`/skill-tags/user-skills/${skillTagId}`),
}