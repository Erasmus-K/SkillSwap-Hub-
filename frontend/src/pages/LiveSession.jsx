import React, { useState } from "react";
import { bookSession } from "../api/sessionApi";

const LiveSession = ({ session }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [meetLink, setMeetLink] = useState(session?.meet_link || "");

  const handleBookSession = async () => {
    if (!session?.id) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const data = await bookSession(session.id);
      console.log("Booking response:", data);
      setSuccess(true);

      // Update Meet link if backend returns it
      if (data.meet_link) {
        setMeetLink(data.meet_link);
      }
    } catch (err) {
      console.error("Error booking session:", err.response?.data || err);
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 border rounded-lg shadow-md bg-white">
      <h2 className="text-xl font-bold">{session.title}</h2>
      <p className="mt-2">{session.description}</p>

      <button
        onClick={handleBookSession}
        disabled={loading}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Booking..." : "Book Session"}
      </button>

      {success && <p className="mt-2 text-green-600">Session booked successfully!</p>}
      {error && <p className="mt-2 text-red-600">Error: {error}</p>}

      {meetLink && (
        <p className="mt-2">
          Meet Link:{" "}
          <a href={meetLink} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
            Join Session
          </a>
        </p>
      )}
    </div>
  );
};

export default LiveSession;
