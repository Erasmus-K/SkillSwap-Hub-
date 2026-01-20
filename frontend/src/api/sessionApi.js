import axios from "axios";

// Fetch all sessions
export const getSessions = async () => {
  try {
    const response = await axios.get("http://localhost:8000/sessions");
    return response.data;
  } catch (error) {
    console.error("Error fetching sessions:", error.response?.data || error);
    throw error;
  }
};

// Book a session
export const bookSession = async (sessionId) => {
  try {
    const response = await axios.post("http://localhost:8000/bookings", {
      session_id: sessionId,
    });
    return response.data;
  } catch (error) {
    console.error("Error booking session:", error.response?.data || error);
    throw error;
  }
};
