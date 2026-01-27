import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import RoutePlanner from './components/RoutePlanner';
import TrafficDashboard from './components/TrafficDashboard';
import RealTimeData from './components/RealTimeData';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('route-planner');
  const [isLoading, setIsLoading] = useState(false);

  return (
    <Router>
      <div className="App">
        <Header />
        
        <div className="container">
          <nav className="tabs">
            <button 
              className={`tab ${activeTab === 'route-planner' ? 'active' : ''}`}
              onClick={() => setActiveTab('route-planner')}
            >
              🗺️ Route Planner
            </button>
            <button 
              className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              📊 Traffic Dashboard
            </button>
            <button 
              className={`tab ${activeTab === 'real-time' ? 'active' : ''}`}
              onClick={() => setActiveTab('real-time')}
            >
              📡 Real-Time Data
            </button>
          </nav>

          <div className="tab-content">
            {activeTab === 'route-planner' && (
              <RoutePlanner isLoading={isLoading} setIsLoading={setIsLoading} />
            )}
            {activeTab === 'dashboard' && (
              <TrafficDashboard />
            )}
            {activeTab === 'real-time' && (
              <RealTimeData />
            )}
          </div>
        </div>

        <footer className="footer">
          <div className="container">
            <p>🌍 <strong>Contributing to SDG 11: Sustainable Cities and Communities</strong></p>
            <p>AI-powered traffic optimization for reduced congestion and environmental impact</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;