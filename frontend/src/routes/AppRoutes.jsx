import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import ProtectedRoute from '../components/ProtectedRoute'

// Pages
import Login from '../pages/Login'
import Register from '../pages/Register'
import Dashboard from '../pages/Dashboard'
import Skills from '../pages/Skills'
import SkillDetails from '../pages/SkillDetails'
import SkillsDiscovery from '../pages/SkillsDiscovery'
import Teach from '../pages/Teach'
import Bookings from '../pages/Bookings'
import Profile from '../pages/Profile'
import LiveSession from '../pages/LiveSession'

const AppRoutes = () => {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <Routes>
      {/* Public Routes */}
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} 
      />
      <Route 
        path="/register" 
        element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />} 
      />
      
      {/* Protected Routes */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/skills" 
        element={
          <ProtectedRoute>
            <Skills />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/skills/:id" 
        element={
          <ProtectedRoute>
            <SkillDetails />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/teach" 
        element={
          <ProtectedRoute>
            <Teach />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/bookings" 
        element={
          <ProtectedRoute>
            <Bookings />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/profile" 
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/skills-discovery" 
        element={
          <ProtectedRoute>
            <SkillsDiscovery />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/sessions/:id" 
        element={
          <ProtectedRoute>
            <LiveSession />
          </ProtectedRoute>
        } 
      />
      
      {/* Default Routes */}
      <Route 
        path="/" 
        element={
          isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
        } 
      />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default AppRoutes