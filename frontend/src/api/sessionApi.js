import api from './axios'

export const sessionApi = {
  getSessions: () => api.get('/sessions'),
  getSession: (id) => api.get(`/sessions/${id}`),
  createSession: (sessionData) => api.post('/sessions', sessionData),
  updateSession: (id, sessionData) => api.put(`/sessions/${id}`, sessionData),
  deleteSession: (id) => api.delete(`/sessions/${id}`),
  bookSession: (sessionId) => api.post(`/sessions/${sessionId}/book`),
  cancelBooking: (sessionId) => api.delete(`/sessions/${sessionId}/book`),
  getMyBookings: () => api.get('/bookings/my'),
}
