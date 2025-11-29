#!/bin/bash

# Dialed In Fitness - Startup Script

echo "🚀 Starting Dialed In Fitness..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   (the directory containing backend/ and frontend/ folders)"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Start backend in background
echo "🔧 Starting backend API..."
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "   Backend PID: $BACKEND_PID"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
python3 -m streamlit run Home.py &
FRONTEND_PID=$!
cd ..

echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:8501"
echo ""

echo "✅ Both services are starting..."
echo ""
echo "📝 To stop the application:"
echo "   Press Ctrl+C in this terminal, or run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🎯 Your browser should open automatically."
echo "   If not, navigate to: http://localhost:8501"
echo ""

# Wait for user to stop
wait
