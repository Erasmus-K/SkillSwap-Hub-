import { Link } from 'react-router-dom'

const SessionCard = ({ session }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-semibold mb-2">{session.title}</h3>
      <p className="text-gray-600 mb-3">{session.description}</p>
      
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm text-gray-500">
          By {session.teacher?.name || 'Unknown'}
        </span>
        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
          {session.skill?.name}
        </span>
      </div>
      
      <div className="text-sm text-gray-600 mb-4">
        <p>📅 {formatDate(session.scheduled_at)}</p>
        <p>⏱️ {session.duration} minutes</p>
        <p>👥 {session.max_participants} max participants</p>
      </div>
      
      <div className="flex justify-between items-center">
        <span className="text-lg font-bold text-green-600">
          ${session.price || 'Free'}
        </span>
        <Link
          to={`/sessions/${session.id}`}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
        >
          View Details
        </Link>
      </div>
    </div>
  )
}

export default SessionCard