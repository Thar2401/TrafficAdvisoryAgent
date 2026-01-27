#!/bin/bash

# Traffic Advisory Agent - Setup Script
echo "🚦 Setting up AI Traffic Advisory Agent (React + Flask Version)"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16+ first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Setting up Backend (Flask)...${NC}"

# Set up backend
cd backend || exit 1

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Backend setup complete!${NC}"

# Set up frontend
echo -e "${BLUE}📦 Setting up Frontend (React)...${NC}"
cd ../frontend || exit 1

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✅ Frontend setup complete!${NC}"

# Go back to root directory
cd ..

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend:"
echo "   cd backend"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "   source venv/Scripts/activate"
else
    echo "   source venv/bin/activate"
fi
echo "   python app.py"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser to http://localhost:3000"
echo ""
echo -e "${BLUE}🌍 Contributing to SDG 11: Sustainable Cities and Communities${NC}"