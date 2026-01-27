import React, { useState, useEffect } from 'react';
import { trafficAPI } from '../services/api';
import TrafficMap from './TrafficMap';

// NYC Real locations for demonstration
const NYC_LOCATIONS = [
  'Manhattan - Times Square',
  'Manhattan - Wall Street',
  'Brooklyn - Downtown Brooklyn',
  'Queens - Long Island City',
  'Bronx - Yankee Stadium',
  'Staten Island - St. George',
  'Manhattan - Central Park',
  'Brooklyn - Williamsburg',
  'Queens - Astoria',
  'Manhattan - Greenwich Village',
  'Brooklyn - Park Slope',
  'Queens - Flushing',
  'Bronx - Fordham',
  'Manhattan - Upper East Side',
  'Brooklyn - DUMBO',
  'Queens - Jamaica',
  'Manhattan - Chinatown',
  'Brooklyn - Coney Island',
  'Queens - Forest Hills',
  'Bronx - The Hub'
];

const RoutePlanner = ({ isLoading, setIsLoading }) => {
  const [formData, setFormData] = useState({
    source: '',
    destination: '',
    preferredTime: new Date().toTimeString().slice(0, 5),
  });
  
  const [preferences, setPreferences] = useState({
    travelTime: 0.4,
    congestion: 0.3,
    fuelEfficiency: 0.2,
    environmentalImpact: 0.1,
  });
  
  const [locations, setLocations] = useState(NYC_LOCATIONS);
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Load locations from API if available
    const loadLocations = async () => {
      try {
        const response = await trafficAPI.getLocations();
        if (response.data && response.data.length > 0) {
          setLocations(response.data);
        }
      } catch (err) {
        console.log('Using default NYC locations');
      }
    };
    
    loadLocations();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePreferenceChange = (preference, value) => {
    setPreferences(prev => ({
      ...prev,
      [preference]: value
    }));
  };

  const normalizePreferences = () => {
    const total = Object.values(preferences).reduce((sum, val) => sum + val, 0);
    if (total === 0) return preferences;
    
    return Object.keys(preferences).reduce((norm, key) => {
      norm[key] = preferences[key] / total;
      return norm;
    }, {});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.source || !formData.destination) {
      setError('Please select both source and destination');
      return;
    }
    
    if (formData.source === formData.destination) {
      setError('Source and destination cannot be the same');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const requestData = {
        source: formData.source,
        destination: formData.destination,
        preferred_time: formData.preferredTime,
        user_preferences: normalizePreferences()
      };
      
      const response = await trafficAPI.getRouteRecommendations(requestData);
      setRecommendations(response.data);
    } catch (err) {
      console.error('Route planning error:', err);
      setError(err.response?.data?.error || 'Failed to get route recommendations. Using demo data.');
      
      // Generate demo response for demonstration
      setRecommendations({
        primary_recommendation: {
          route_description: `${formData.source} → ${formData.destination} via optimal route`,
          recommended_departure: formData.preferredTime,
          travel_metrics: {
            estimated_travel_time_min: Math.floor(Math.random() * 60) + 15,
            distance_km: Math.floor(Math.random() * 20) + 5,
            traffic_level: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)]
          },
          environmental_impact: {
            fuel_consumption_l: (Math.random() * 5 + 2).toFixed(1),
            co2_emission_kg: (Math.random() * 10 + 5).toFixed(1)
          },
          recommendation_strength: 'Strong'
        },
        alternative_options: [
          {
            route_description: 'Alternative Route 1',
            departure_time: formData.preferredTime,
            key_metrics: {
              travel_time_min: Math.floor(Math.random() * 60) + 20,
              traffic_level: 'medium',
              fuel_consumption_l: (Math.random() * 4 + 3).toFixed(1)
            },
            best_for: 'Scenic route with moderate traffic'
          }
        ],
        traffic_insights: [
          'Traffic is expected to be lighter in 30 minutes',
          'Alternative routes available to avoid construction',
          'Weather conditions are favorable for travel'
        ],
        sustainability_insights: {
          improvement_opportunities: [
            'Consider carpooling to reduce environmental impact',
            'Electric vehicle charging stations available on route',
            'Public transportation options are efficient during peak hours'
          ]
        }
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getTrafficStatusColor = (level) => {
    const colors = {
      low: '#28a745',
      medium: '#ffc107',
      high: '#fd7e14',
      severe: '#dc3545'
    };
    return colors[level] || '#6c757d';
  };

  return (
    <div>
      <div className="route-form">
        <h2>🗺️ Route Planning</h2>
        
        {error && (
          <div className="alert alert-warning">
            <strong>Note:</strong> {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="source">📍 From (Source)</label>
              <select
                id="source"
                name="source"
                value={formData.source}
                onChange={handleInputChange}
                required
              >
                <option value="">Select starting location</option>
                {locations.map((location, index) => (
                  <option key={index} value={location}>{location}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="destination">🎯 To (Destination)</label>
              <select
                id="destination"
                name="destination"
                value={formData.destination}
                onChange={handleInputChange}
                required
              >
                <option value="">Select destination</option>
                {locations.map((location, index) => (
                  <option key={index} value={location}>{location}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="preferredTime">🕐 Preferred Time</label>
              <input
                type="time"
                id="preferredTime"
                name="preferredTime"
                value={formData.preferredTime}
                onChange={handleInputChange}
              />
            </div>
            
            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? 'Planning...' : '🚀 Get Route'}
            </button>
          </div>
        </form>
      </div>

      {/* Interactive Traffic Map */}
      <div className="route-form">
        <h2>🗺️ NYC Traffic Map</h2>
        <TrafficMap 
          selectedRoute={{
            source: formData.source,
            destination: formData.destination
          }}
        />
      </div>

      <div className="preferences-section">
        <h3>⚙️ Optimization Preferences</h3>
        <div className="preferences-grid">
          <div className="preference-item">
            <label>Travel Time Priority: {(preferences.travelTime * 100).toFixed(0)}%</label>
            <input
              type="range"
              className="slider"
              min="0"
              max="1"
              step="0.1"
              value={preferences.travelTime}
              onChange={(e) => handlePreferenceChange('travelTime', parseFloat(e.target.value))}
            />
          </div>
          <div className="preference-item">
            <label>Congestion Avoidance: {(preferences.congestion * 100).toFixed(0)}%</label>
            <input
              type="range"
              className="slider"
              min="0"
              max="1"
              step="0.1"
              value={preferences.congestion}
              onChange={(e) => handlePreferenceChange('congestion', parseFloat(e.target.value))}
            />
          </div>
          <div className="preference-item">
            <label>Fuel Efficiency: {(preferences.fuelEfficiency * 100).toFixed(0)}%</label>
            <input
              type="range"
              className="slider"
              min="0"
              max="1"
              step="0.1"
              value={preferences.fuelEfficiency}
              onChange={(e) => handlePreferenceChange('fuelEfficiency', parseFloat(e.target.value))}
            />
          </div>
          <div className="preference-item">
            <label>Environmental Impact: {(preferences.environmentalImpact * 100).toFixed(0)}%</label>
            <input
              type="range"
              className="slider"
              min="0"
              max="1"
              step="0.1"
              value={preferences.environmentalImpact}
              onChange={(e) => handlePreferenceChange('environmentalImpact', parseFloat(e.target.value))}
            />
          </div>
        </div>
      </div>

      {isLoading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>🔄 Analyzing traffic patterns and optimizing routes...</p>
        </div>
      )}

      {recommendations && !isLoading && (
        <div className="results-section">
          <div className="primary-recommendation">
            <h3>🌟 Primary Recommendation</h3>
            
            <div className="grid grid-4">
              <div className="metric">
                <div className="metric-value">🛣️</div>
                <div className="metric-label">
                  {recommendations.primary_recommendation.route_description}
                </div>
              </div>
              <div className="metric">
                <div className="metric-value">
                  {recommendations.primary_recommendation.travel_metrics.estimated_travel_time_min}min
                </div>
                <div className="metric-label">Travel Time</div>
              </div>
              <div className="metric">
                <div className="metric-value">
                  {recommendations.primary_recommendation.travel_metrics.distance_km}km
                </div>
                <div className="metric-label">Distance</div>
              </div>
              <div className="metric">
                <div 
                  className="metric-value"
                  style={{ color: getTrafficStatusColor(recommendations.primary_recommendation.travel_metrics.traffic_level) }}
                >
                  <span className={`status-indicator ${recommendations.primary_recommendation.travel_metrics.traffic_level}`}></span>
                  {recommendations.primary_recommendation.travel_metrics.traffic_level.toUpperCase()}
                </div>
                <div className="metric-label">Traffic Level</div>
              </div>
            </div>
            
            <div className="grid grid-4" style={{ marginTop: '15px' }}>
              <div className="metric">
                <div className="metric-value">⛽ {recommendations.primary_recommendation.environmental_impact.fuel_consumption_l}L</div>
                <div className="metric-label">Fuel Consumption</div>
              </div>
              <div className="metric">
                <div className="metric-value">🌱 {recommendations.primary_recommendation.environmental_impact.co2_emission_kg}kg</div>
                <div className="metric-label">CO2 Emissions</div>
              </div>
              <div className="metric">
                <div className="metric-value">🕐 {recommendations.primary_recommendation.recommended_departure}</div>
                <div className="metric-label">Departure Time</div>
              </div>
              <div className="metric">
                <div className="metric-value">⭐ {recommendations.primary_recommendation.recommendation_strength}</div>
                <div className="metric-label">Rating</div>
              </div>
            </div>
          </div>

          {recommendations.alternative_options && recommendations.alternative_options.length > 0 && (
            <div className="alternatives-section">
              <h3>🔀 Alternative Options</h3>
              {recommendations.alternative_options.map((alt, index) => (
                <div key={index} className="alternative">
                  <h4>{alt.route_description}</h4>
                  <div className="grid grid-3">
                    <div>
                      <strong>🕐 Departure:</strong> {alt.departure_time}<br/>
                      <strong>⏱️ Travel Time:</strong> {alt.key_metrics.travel_time_min} min
                    </div>
                    <div>
                      <strong>🚦 Traffic:</strong> {alt.key_metrics.traffic_level}<br/>
                      <strong>⛽ Fuel:</strong> {alt.key_metrics.fuel_consumption_l} L
                    </div>
                    <div>
                      <strong>🎯 Best for:</strong> {alt.best_for}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {recommendations.traffic_insights && (
            <div className="insights-section">
              <h3>💡 Traffic Insights</h3>
              {recommendations.traffic_insights.map((insight, index) => (
                <div key={index} className="insight-item">
                  • {insight}
                </div>
              ))}
            </div>
          )}

          {recommendations.sustainability_insights?.improvement_opportunities && (
            <div className="insights-section">
              <h3>🌱 Sustainability Tips</h3>
              {recommendations.sustainability_insights.improvement_opportunities.map((tip, index) => (
                <div key={index} className="insight-item">
                  • {tip}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RoutePlanner;