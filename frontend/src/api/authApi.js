import api from './axios'

export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  refreshToken: () => api.post('/auth/refresh'),
  googleAuth: (token) => api.post('/auth/google', { token }),
  getCurrentUser: () => api.get('/auth/me'),
}