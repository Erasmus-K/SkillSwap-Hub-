import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { skillTagsApi } from '../api/skillTagsApi'
import { sessionApi } from '../api/sessionApi'
import Navbar from '../components/Navbar'

const Teach = () => {
  const [myTeachingSkills, setMyTeachingSkills] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    skill_id: '',
    start_time: '',
    end_time: '',
    max_participants: 10
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const fetchMySkills = async () => {
      try {
        const response = await skillTagsApi.getMySkills()
        // Filter only skills the user can teach
        const teachingSkills = response.data.filter(skill => skill.is_teaching)
        setMyTeachingSkills(teachingSkills)
      } catch (error) {
        console.error('Error fetching skills:', error)
      }
    }

    fetchMySkills()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Convert datetime-local to ISO format
      const sessionData = {
        ...formData,
        start_time: new Date(formData.start_time).toISOString(),
        end_time: new Date(formData.end_time).toISOString()
      }
      await sessionApi.createSession(sessionData)
      navigate('/dashboard', { state: { message: 'Session created successfully!' } })
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create session')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) : e.target.value
    setFormData({ ...formData, [e.target.name]: value })
  }

  const handleStartTimeChange = (e) => {
    const startTime = e.target.value
    setFormData({ 
      ...formData, 
      start_time: startTime,
      // Auto-set end time to 1 hour later
      end_time: startTime ? new Date(new Date(startTime).getTime() + 60 * 60 * 1000).toISOString().slice(0, 16) : ''
    })
  }

  return (
    <>
      <Navbar />
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Create a Teaching Session</h1>
          <p className="text-gray-600">Share your expertise and help others learn new skills</p>
        </div>

        {myTeachingSkills.length === 0 ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
            <h3 className="text-lg font-medium text-yellow-800 mb-2">No Teaching Skills Found</h3>
            <p className="text-yellow-700 mb-4">
              You need to add skills you can teach before creating a session.
            </p>
            <button
              onClick={() => navigate('/profile')}
              className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded transition-colors"
            >
              Add Skills to Profile
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session Title
              </label>
              <input
                type="text"
                name="title"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Introduction to Python Programming"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                name="description"
                rows={4}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe what you'll teach and what students will learn..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skill You'll Teach
              </label>
              <select
                name="skill_id"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.skill_id}
                onChange={handleChange}
              >
                <option value="">Select a skill you can teach</option>
                {myTeachingSkills.map((skill) => (
                  <option key={skill.id} value={skill.id}>
                    {skill.name} ({skill.skill_level})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date & Time
              </label>
              <input
                type="datetime-local"
                name="start_time"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.start_time}
                onChange={handleStartTimeChange}
                min={new Date().toISOString().slice(0, 16)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date & Time
              </label>
              <input
                type="datetime-local"
                name="end_time"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.end_time}
                onChange={handleChange}
                min={formData.start_time}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Participants
              </label>
              <input
                type="number"
                name="max_participants"
                min="1"
                max="50"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.max_participants}
                onChange={handleChange}
              />
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-colors disabled:opacity-50"
              >
                {loading ? 'Creating Session...' : 'Create Session'}
              </button>
            </div>
          </form>
        )}
      </div>
    </>
  )
}

export default Teach