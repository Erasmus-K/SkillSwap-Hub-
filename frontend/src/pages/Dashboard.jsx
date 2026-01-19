import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { sessionApi } from '../api/sessionApi'
import SessionCard from '../components/SessionCard'
import Navbar from '../components/Navbar'

const Dashboard = () => {
  const { user } = useAuth()
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await sessionApi.getSessions()
        setSessions(response.data)
      } catch (error) {
        console.error('Error fetching sessions:', error)
        // Could add user-facing error handling here
        setSessions([])
      } finally {
        setLoading(false)
      }
    }

    fetchSessions()
  }, [])

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Discover new skills and share your expertise
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-900">Available Sessions</h3>
            <p className="text-3xl font-bold text-blue-600">{sessions.length}</p>
          </div>
          <div className="bg-green-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-green-900">Your Bookings</h3>
            <p className="text-3xl font-bold text-green-600">0</p>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-purple-900">Skills Taught</h3>
            <p className="text-3xl font-bold text-purple-600">0</p>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Sessions</h2>
          {sessions.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sessions.slice(0, 6).map((session) => (
                <SessionCard key={session.id} session={session} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No sessions available yet.</p>
              <p className="text-gray-400">Be the first to create a session!</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default Dashboard