import { useState, useEffect } from 'react'
import { skillTagsApi } from '../api/skillTagsApi'

const SkillsProfile = () => {
  const [mySkills, setMySkills] = useState([])
  const [allSkillTags, setAllSkillTags] = useState([])
  const [showAddSkill, setShowAddSkill] = useState(false)
  const [newSkill, setNewSkill] = useState({
    skill_tag_id: '',
    skill_level: 'beginner',
    is_teaching: false,
    is_learning: false
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [mySkillsRes, skillTagsRes] = await Promise.all([
        skillTagsApi.getMySkills(),
        skillTagsApi.getSkillTags()
      ])
      setMySkills(mySkillsRes.data)
      setAllSkillTags(skillTagsRes.data)
    } catch (error) {
      console.error('Error loading skills:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddSkill = async (e) => {
    e.preventDefault()
    try {
      await skillTagsApi.addUserSkill(newSkill)
      setNewSkill({
        skill_tag_id: '',
        skill_level: 'beginner',
        is_teaching: false,
        is_learning: false
      })
      setShowAddSkill(false)
      loadData()
    } catch (error) {
      console.error('Error adding skill:', error)
    }
  }

  const handleRemoveSkill = async (skillTagId) => {
    try {
      await skillTagsApi.removeUserSkill(skillTagId)
      loadData()
    } catch (error) {
      console.error('Error removing skill:', error)
    }
  }

  const getSkillsByType = (type) => {
    return mySkills.filter(skill => skill[type])
  }

  if (loading) return <div className="text-center py-8">Loading skills...</div>

  return (
    <div className="space-y-8">
      {/* Skills I Can Teach */}
      <div className="bg-green-50 p-6 rounded-lg">
        <h3 className="text-xl font-semibold text-green-800 mb-4">Skills I Can Teach</h3>
        <div className="flex flex-wrap gap-2">
          {getSkillsByType('is_teaching').map(skill => (
            <span
              key={skill.id}
              className="bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm flex items-center gap-2"
            >
              {skill.name} ({skill.skill_level})
              <button
                onClick={() => handleRemoveSkill(skill.id)}
                className="text-green-600 hover:text-green-800"
              >
                ×
              </button>
            </span>
          ))}
          {getSkillsByType('is_teaching').length === 0 && (
            <p className="text-green-600">No teaching skills added yet</p>
          )}
        </div>
      </div>

      {/* Skills I Want to Learn */}
      <div className="bg-blue-50 p-6 rounded-lg">
        <h3 className="text-xl font-semibold text-blue-800 mb-4">Skills I Want to Learn</h3>
        <div className="flex flex-wrap gap-2">
          {getSkillsByType('is_learning').map(skill => (
            <span
              key={skill.id}
              className="bg-blue-200 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center gap-2"
            >
              {skill.name}
              <button
                onClick={() => handleRemoveSkill(skill.id)}
                className="text-blue-600 hover:text-blue-800"
              >
                ×
              </button>
            </span>
          ))}
          {getSkillsByType('is_learning').length === 0 && (
            <p className="text-blue-600">No learning goals added yet</p>
          )}
        </div>
      </div>

      {/* Add New Skill */}
      <div className="bg-white border-2 border-dashed border-gray-300 p-6 rounded-lg">
        {!showAddSkill ? (
          <button
            onClick={() => setShowAddSkill(true)}
            className="w-full text-gray-600 hover:text-gray-800 font-medium"
          >
            + Add a Skill
          </button>
        ) : (
          <form onSubmit={handleAddSkill} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Skill
              </label>
              <select
                value={newSkill.skill_tag_id}
                onChange={(e) => setNewSkill({...newSkill, skill_tag_id: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="">Choose a skill...</option>
                {allSkillTags.map(tag => (
                  <option key={tag.id} value={tag.id}>
                    {tag.name} ({tag.category})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Level
              </label>
              <select
                value={newSkill.skill_level}
                onChange={(e) => setNewSkill({...newSkill, skill_level: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={newSkill.is_teaching}
                  onChange={(e) => setNewSkill({...newSkill, is_teaching: e.target.checked})}
                  className="mr-2"
                />
                I can teach this
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={newSkill.is_learning}
                  onChange={(e) => setNewSkill({...newSkill, is_learning: e.target.checked})}
                  className="mr-2"
                />
                I want to learn this
              </label>
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
              >
                Add Skill
              </button>
              <button
                type="button"
                onClick={() => setShowAddSkill(false)}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default SkillsProfile