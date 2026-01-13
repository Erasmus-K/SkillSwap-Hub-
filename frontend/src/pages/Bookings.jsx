import { useState, useEffect } from 'react'
import { sessionApi } from '../api/sessionApi'
import Navbar from '../components/Navbar'
import { Link } from 'react-router-dom'

const Bookings = () => {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await sessionApi.getMyBookings()
        setBookings(response.data)
      } catch (error) {
        console.error('Error fetching bookings:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchBookings()
  }, [])

  const handleCancelBooking = async (sessionId) => {
    try {
      await sessionApi.cancelBooking(sessionId)
      setBookings(bookings.filter(booking => booking.session.id !== sessionId))
    } catch (error) {
      console.error('Error canceling booking:', error)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
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

  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">My Bookings</h1>
          <p className="text-gray-600">Manage your upcoming learning sessions</p>
        </div>

        {bookings.length > 0 ? (
          <div className="space-y-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{booking.session.title}</h3>
                    <p className="text-gray-600 mb-2">{booking.session.description}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>📅 {formatDate(booking.session.scheduled_at)}</span>
                      <span>⏱️ {booking.session.duration} minutes</span>
                      <span>👨‍🏫 {booking.session.teacher?.name}</span>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      booking.status === 'confirmed' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {booking.status}
                    </span>
                  </div>
                </div>

                <div className="flex justify-between items-center pt-4 border-t">
                  <div className="flex gap-2">
                    {booking.session.meet_link && (
                      <a
                        href={booking.session.meet_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition-colors"
                      >
                        Join Session
                      </a>
                    )}
                    <Link
                      to={`/sessions/${booking.session.id}`}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
                    >
                      View Details
                    </Link>
                  </div>
                  
                  <button
                    onClick={() => handleCancelBooking(booking.session.id)}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
                  >
                    Cancel Booking
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg mb-4">You haven't booked any sessions yet.</p>
            <Link
              to="/skills"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors"
            >
              Browse Skills
            </Link>
          </div>
        )}
      </div>
    </>
  )
}

export default Bookings