import { useState, useEffect } from 'react'
import { skillApi } from '../api/skillApi'
import Navbar from '../components/Navbar'
import { Link } from 'react-router-dom'

const Skills = () => {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await skillApi.getSkills()
        setSkills(response.data)
      } catch (error) {
        console.error('Error fetching skills:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSkills()
  }, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    try {
      setLoading(true)
      const response = await skillApi.searchSkills(searchQuery)
      setSkills(response.data)
    } catch (error) {
      console.error('Error searching skills:', error)
    } finally {
      setLoading(false)
    }
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
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Browse Skills</h1>
          
          <form onSubmit={handleSearch} className="flex gap-4 mb-6">
            <input
              type="text"
              placeholder="Search skills..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Search
            </button>
          </form>
        </div>

        {skills.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {skills.map((skill) => (
              <div key={skill.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <h3 className="text-xl font-semibold mb-2">{skill.name}</h3>
                <p className="text-gray-600 mb-4">{skill.description}</p>
                
                <div className="flex items-center justify-between mb-4">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    {skill.category}
                  </span>
                  <span className="text-sm text-gray-500">
                    {skill.sessions?.length || 0} sessions
                  </span>
                </div>
                
                <Link
                  to={`/skills/${skill.id}`}
                  className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition-colors"
                >
                  View Sessions
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No skills found.</p>
            <p className="text-gray-400">Try a different search term.</p>
          </div>
        )}
      </div>
    </>
  )
}

export default Skills