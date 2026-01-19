#!/bin/bash

echo "Starting SkillSwap Hub..."

# Kill any existing processes
echo "Stopping existing servers..."
pkill -f "uvicorn"
pkill -f "vite"

# Start backend
echo "Starting backend server..."
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend running on http://localhost:8000"
echo "Frontend running on http://localhost:5173"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Wait for user input to stop
echo "Press Ctrl+C to stop both servers"
wait