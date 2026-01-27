@echo off
REM Traffic Advisory Agent - Setup Script for Windows

echo 🚦 Setting up AI Traffic Advisory Agent (React + Flask Version)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo 📦 Setting up Backend (Flask)...

REM Set up backend
cd backend
if errorlevel 1 (
    echo ❌ Failed to navigate to backend directory
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Backend setup complete!

REM Set up frontend
echo 📦 Setting up Frontend (React)...
cd ..\frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

REM Go back to root directory
cd ..

echo 🎉 Setup complete!
echo.
echo To start the application:
echo.
echo 1. Start the backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python app.py
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Open your browser to http://localhost:3000
echo.
echo 🌍 Contributing to SDG 11: Sustainable Cities and Communities

pause