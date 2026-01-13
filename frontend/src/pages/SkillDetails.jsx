import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { skillApi } from '../api/skillApi'
import SessionCard from '../components/SessionCard'
import Navbar from '../components/Navbar'

const SkillDetails = () => {
  const { id } = useParams()
  const [skill, setSkill] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSkill = async () => {
      try {
        const response = await skillApi.getSkill(id)
        setSkill(response.data)
      } catch (error) {
        console.error('Error fetching skill:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSkill()
  }, [id])

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

  if (!skill) {
    return (
      <>
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Skill not found</h1>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{skill.name}</h1>
          <p className="text-gray-600 text-lg mb-4">{skill.description}</p>
          
          <div className="flex items-center gap-4">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
              {skill.category}
            </span>
            <span className="text-gray-500">
              {skill.sessions?.length || 0} available sessions
            </span>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Sessions</h2>
          {skill.sessions && skill.sessions.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {skill.sessions.map((session) => (
                <SessionCard key={session.id} session={session} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No sessions available for this skill yet.</p>
              <p className="text-gray-400">Check back later or create your own session!</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default SkillDetails