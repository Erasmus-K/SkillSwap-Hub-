import { useState, useEffect } from "react";
import { getSessions, bookSession } from "../api/sessionApi"; // ✅ Correct named imports
import { skillTagsApi } from "../api/skillTagsApi";
import Navbar from "../components/Navbar";

const SkillsDiscovery = () => {
  const [myLearningSkills, setMyLearningSkills] = useState([]);
  const [availableSessions, setAvailableSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState(null);
  const [bookingSuccess, setBookingSuccess] = useState(null);

  useEffect(() => {
    loadMyLearningSkills();
    loadAvailableSessions();
  }, []);

  const loadMyLearningSkills = async () => {
    try {
      const response = await skillTagsApi.getMySkills();
      const learningSkills = response.data.filter((skill) => skill.is_learning);
      setMyLearningSkills(learningSkills);
    } catch (error) {
      console.error("Error loading learning skills:", error);
    }
  };

  const loadAvailableSessions = async () => {
    try {
      const data = await getSessions();
      setAvailableSessions(data);
    } catch (error) {
      console.error("Error loading sessions:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSessionsForSkill = (skillId) => {
    return availableSessions.filter((session) => session.skill_id === skillId);
  };

  const handleBookSession = async (sessionId, setMeetLink) => {
    setBookingLoading(true);
    setBookingError(null);
    setBookingSuccess(null);

    try {
      const data = await bookSession(sessionId);
      setBookingSuccess(`Session booked successfully!`);
      
      // Update Meet link if returned from backend
      if (data.meet_link && setMeetLink) {
        setMeetLink(data.meet_link);
      }
    } catch (error) {
      console.error("Error booking session:", error);
      setBookingError(error.response?.data?.detail || "Something went wrong");
    } finally {
      setBookingLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <>
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Skills Discovery</h1>
          <p className="text-gray-600">Find teachers for skills you want to learn</p>
        </div>

        {myLearningSkills.length === 0 ? (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="text-lg font-medium text-blue-800 mb-2">No Learning Goals Found</h3>
            <p className="text-blue-700 mb-4">
              Add skills you want to learn to see available teachers and sessions.
            </p>
            <button
              onClick={() => (window.location.href = "/profile")}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
            >
              Add Learning Goals
            </button>
          </div>
        ) : (
          <div className="space-y-8">
            {myLearningSkills.map((skill) => {
              const sessions = getSessionsForSkill(skill.id);
              return (
                <div key={skill.id} className="bg-white border border-gray-200 rounded-lg p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900">{skill.name}</h3>
                      <p className="text-gray-600">{skill.category}</p>
                      <p className="text-sm text-gray-500">{skill.description}</p>
                    </div>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                      Want to learn
                    </span>
                  </div>

                  {sessions.length > 0 ? (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-3">Available Sessions ({sessions.length})</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {sessions.map((session) => {
                          const [meetLink, setMeetLink] = useState(session.meet_link || "");

                          return (
                            <div key={session.id} className="border border-gray-200 rounded-lg p-4">
                              <h5 className="font-medium text-gray-900 mb-2">{session.title}</h5>
                              <p className="text-sm text-gray-600 mb-2">{session.description}</p>
                              <div className="text-xs text-gray-500 space-y-1">
                                <p>📅 {new Date(session.start_time).toLocaleDateString()}</p>
                                <p>⏰ {new Date(session.start_time).toLocaleTimeString()}</p>
                                <p>👥 Max {session.max_participants} participants</p>
                              </div>

                              {meetLink && (
                                <p className="mt-2 text-blue-600 underline text-sm">
                                  Meet Link: <a href={meetLink} target="_blank" rel="noopener noreferrer">{meetLink}</a>
                                </p>
                              )}

                              <button
                                onClick={() => handleBookSession(session.id, setMeetLink)}
                                className="w-full mt-3 bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded text-sm transition-colors"
                                disabled={bookingLoading}
                              >
                                {bookingLoading ? "Booking..." : "Book Session"}
                              </button>

                              {bookingError && <p className="text-red-600 text-sm mt-1">{bookingError}</p>}
                              {bookingSuccess && <p className="text-green-600 text-sm mt-1">{bookingSuccess}</p>}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
                      <p className="text-gray-600 mb-3">No sessions available for {skill.name} yet</p>
                      <p className="text-sm text-gray-500 mb-3">
                        You can request a session or check back later
                      </p>
                      <button
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm transition-colors"
                        onClick={() => alert("Session request feature coming soon!")}
                      >
                        Request Session
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
};

export default SkillsDiscovery;
