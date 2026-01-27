#!/bin/bash

# Quick start script for Traffic Advisory Agent
echo "🚦 Starting AI Traffic Advisory Agent..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend not set up. Please run ./setup.sh first."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend not set up. Please run ./setup.sh first."
    exit 1
fi

# Function to start backend
start_backend() {
    echo "🔧 Starting Flask backend..."
    cd backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo "✅ Backend started (PID: $BACKEND_PID)"
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting React frontend..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
}

# Start backend
start_backend

# Wait a moment for backend to initialize
sleep 3

# Start frontend
start_frontend

echo ""
echo "🌐 Application starting..."
echo "📊 Backend API: http://localhost:5000"
echo "💻 Frontend App: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    exit 0
}

# Set up cleanup on script exit
trap cleanup INT TERM

# Wait for user input to stop
wait