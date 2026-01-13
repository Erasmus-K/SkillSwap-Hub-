import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { sessionApi } from '../api/sessionApi'
import Navbar from '../components/Navbar'

const LiveSession = () => {
  const { id } = useParams()
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isBooked, setIsBooked] = useState(false)

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await sessionApi.getSession(id)
        setSession(response.data)
        // TODO: Check if user has booked this session
      } catch (error) {
        console.error('Error fetching session:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSession()
  }, [id])

  const handleBookSession = async () => {
    try {
      await sessionApi.bookSession(id)
      setIsBooked(true)
      // Refresh session data to get updated booking count
      const response = await sessionApi.getSession(id)
      setSession(response.data)
    } catch (error) {
      console.error('Error booking session:', error)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

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

  if (!session) {
    return (
      <>
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Session not found</h1>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{session.title}</h1>
            <p className="text-gray-600 text-lg mb-6">{session.description}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Session Details</h3>
                <div className="space-y-2 text-gray-600">
                  <p>📅 <strong>Date:</strong> {formatDate(session.scheduled_at)}</p>
                  <p>⏱️ <strong>Duration:</strong> {session.duration} minutes</p>
                  <p>👥 <strong>Max Participants:</strong> {session.max_participants}</p>
                  <p>💰 <strong>Price:</strong> {session.price ? `$${session.price}` : 'Free'}</p>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Instructor</h3>
                <div className="space-y-2 text-gray-600">
                  <p><strong>Name:</strong> {session.teacher?.name}</p>
                  <p><strong>Email:</strong> {session.teacher?.email}</p>
                  {session.teacher?.bio && (
                    <p><strong>Bio:</strong> {session.teacher.bio}</p>
                  )}
                </div>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Skill</h3>
              <div className="flex items-center gap-4">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                  {session.skill?.name}
                </span>
                <span className="text-gray-600">{session.skill?.category}</span>
              </div>
            </div>
          </div>

          <div className="border-t pt-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-500">
                  {session.current_participants || 0} / {session.max_participants} participants
                </p>
                <div className="w-64 bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ 
                      width: `${((session.current_participants || 0) / session.max_participants) * 100}%` 
                    }}
                  ></div>
                </div>
              </div>
              
              <div className="flex gap-4">
                {session.meet_link && isBooked && (
                  <a
                    href={session.meet_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors"
                  >
                    Join Session
                  </a>
                )}
                
                {!isBooked && (
                  <button
                    onClick={handleBookSession}
                    disabled={session.current_participants >= session.max_participants}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg transition-colors"
                  >
                    {session.current_participants >= session.max_participants 
                      ? 'Session Full' 
                      : 'Book Session'
                    }
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default LiveSession