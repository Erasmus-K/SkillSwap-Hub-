import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import SkillsProfile from '../components/SkillsProfile'

const Profile = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('profile')
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    bio: user?.bio || ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    // TODO: Implement profile update API call
    console.log('Update profile:', formData)
    setIsEditing(false)
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  return (
    <>
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-8 pt-6">
              <button
                onClick={() => setActiveTab('profile')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'profile'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                Profile Info
              </button>
              <button
                onClick={() => setActiveTab('skills')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'skills'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                My Skills
              </button>
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'profile' && (
              <div>
                <div className="flex justify-between items-center mb-8">
                  <h1 className="text-3xl font-bold text-gray-900">Profile Information</h1>
                  <button
                    onClick={() => setIsEditing(!isEditing)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
                  >
                    {isEditing ? 'Cancel' : 'Edit Profile'}
                  </button>
                </div>

                {isEditing ? (
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name
                      </label>
                      <input
                        type="text"
                        name="full_name"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        value={formData.full_name}
                        onChange={handleChange}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        name="email"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        value={formData.email}
                        onChange={handleChange}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Bio
                      </label>
                      <textarea
                        name="bio"
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        value={formData.bio}
                        onChange={handleChange}
                        placeholder="Tell others about yourself and your expertise..."
                      />
                    </div>

                    <div className="flex gap-4">
                      <button
                        type="submit"
                        className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded transition-colors"
                      >
                        Save Changes
                      </button>
                      <button
                        type="button"
                        onClick={() => setIsEditing(false)}
                        className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Personal Information</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-500">Name</label>
                          <p className="text-lg text-gray-900">{user?.full_name}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-500">Email</label>
                          <p className="text-lg text-gray-900">{user?.email}</p>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Bio</h3>
                      <p className="text-gray-700">
                        {user?.bio || 'No bio added yet. Click "Edit Profile" to add one.'}
                      </p>
                    </div>

                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Statistics</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-blue-900">Sessions Taught</h4>
                          <p className="text-2xl font-bold text-blue-600">0</p>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-green-900">Sessions Attended</h4>
                          <p className="text-2xl font-bold text-green-600">0</p>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-purple-900">Skills Shared</h4>
                          <p className="text-2xl font-bold text-purple-600">0</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'skills' && (
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">My Skills</h1>
                <SkillsProfile />
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default Profile