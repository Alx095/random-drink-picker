#!/bin/bash
# Setup script for Menu Drink Selector App

echo "🍹 Setting up Menu Drink Selector App..."

# Create project directory
mkdir -p menu-drink-selector
cd menu-drink-selector

# Create backend directory structure
mkdir -p backend
mkdir -p frontend/src
mkdir -p frontend/public

echo "✅ Directory structure created"

# Backend setup
echo "📦 Install backend dependencies:"
echo "cd backend && pip install -r requirements.txt"

# Frontend setup  
echo "📦 Install frontend dependencies:"
echo "cd frontend && npm install"

# Environment setup
echo "🔧 Create environment files:"
echo "backend/.env - Add your Gemini API key"
echo "frontend/.env - Add backend URL"

# Run instructions
echo "🚀 To run the app:"
echo "Backend: cd backend && python server.py"
echo "Frontend: cd frontend && npm start"

echo "✅ Setup complete! Check README.md for detailed instructions."