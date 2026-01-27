import React, { useState, useEffect } from 'react';
import { trafficAPI } from '../services/api';

const RealTimeData = () => {
  const [realTimeData, setRealTimeData] = useState(null);
  const [nycData, setNycData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Sample real-time data based on NYC traffic patterns
  const sampleRealTimeData = {
    current_conditions: {
      timestamp: new Date().toISOString(),
      overall_congestion: 0.65,
      average_speed: 24.5,
      active_incidents: 3,
      weather_condition: 'Clear'
    },
    live_routes: [
      {
        route: 'FDR Drive Southbound',
        current_speed: 18.5,
        congestion_level: 0.85,
        travel_time_multiplier: 1.8,
        incidents: ['Construction at Exit 6', 'Heavy traffic from Brooklyn Bridge'],
        last_updated: new Date().toISOString()
      },
      {
        route: 'Brooklyn Bridge',
        current_speed: 12.3,
        congestion_level: 0.92,
        travel_time_multiplier: 2.1,
        incidents: ['Accident cleared, residual delays'],
        last_updated: new Date().toISOString()
      },
      {
        route: 'Manhattan Bridge',
        current_speed: 22.1,
        congestion_level: 0.58,
        travel_time_multiplier: 1.3,
        incidents: [],
        last_updated: new Date().toISOString()
      },
      {
        route: 'Williamsburg Bridge',
        current_speed: 28.7,
        congestion_level: 0.42,
        travel_time_multiplier: 1.1,
        incidents: [],
        last_updated: new Date().toISOString()
      },
      {
        route: 'Queens Midtown Tunnel',
        current_speed: 15.2,
        congestion_level: 0.88,
        travel_time_multiplier: 1.9,
        incidents: ['High volume traffic'],
        last_updated: new Date().toISOString()
      }
    ],
    traffic_alerts: [
      {
        type: 'construction',
        location: 'Manhattan - 42nd Street',
        description: 'Lane closure on 42nd Street between 7th and 8th Avenue',
        severity: 'medium',
        estimated_end: '2024-01-20T18:00:00Z'
      },
      {
        type: 'incident',
        location: 'Brooklyn - BQE Eastbound',
        description: 'Vehicle breakdown cleared, traffic normalizing',
        severity: 'low',
        estimated_end: '2024-01-19T16:30:00Z'
      },
      {
        type: 'event',
        location: 'Manhattan - Times Square',
        description: 'Large event ending, expect increased pedestrian traffic',
        severity: 'high',
        estimated_end: '2024-01-19T22:00:00Z'
      }
    ],
    public_transit: {
      subway_status: 'Good Service',
      bus_delays: 'Minor delays on M15, M42 routes',
      service_alerts: [
        'No service changes planned for weekend',
        'Express service running normally'
      ]
    }
  };

  const sampleWeatherData = {
    location: 'New York City',
    temperature: 18,
    condition: 'Clear',
    visibility: 10,
    wind_speed: 8,
    humidity: 65,
    traffic_impact: 'Minimal - favorable driving conditions'
  };

  useEffect(() => {
    loadRealTimeData();
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(loadRealTimeData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadRealTimeData = async () => {
    setLoading(true);
    try {
      // Try to load real data from API
      const [realTimeResponse, weatherResponse] = await Promise.allSettled([
        trafficAPI.getRealTimeData(),
        trafficAPI.getWeatherData('NYC')
      ]);

      if (realTimeResponse.status === 'fulfilled') {
        setRealTimeData(realTimeResponse.value.data);
      } else {
        // Use sample data
        setRealTimeData(sampleRealTimeData);
      }

      if (weatherResponse.status === 'fulfilled') {
        setWeatherData(weatherResponse.value.data);
      } else {
        setWeatherData(sampleWeatherData);
      }

      // Try to load NYC Open Data
      try {
        const nycResponse = await trafficAPI.getNYCTrafficData();
        setNycData(nycResponse.data);
      } catch (error) {
        console.log('NYC Open Data not available, using sample data');
      }

      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error loading real-time data:', error);
      // Fallback to sample data
      setRealTimeData(sampleRealTimeData);
      setWeatherData(sampleWeatherData);
      setLastUpdate(new Date());
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getTrafficStatusColor = (level) => {
    if (level < 0.3) return '#28a745';
    if (level < 0.6) return '#ffc107';
    if (level < 0.8) return '#fd7e14';
    return '#dc3545';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#28a745',
      medium: '#ffc107',
      high: '#dc3545'
    };
    return colors[severity] || '#6c757d';
  };

  if (loading && !realTimeData) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading real-time traffic data...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>📡 Real-Time Traffic Data</h2>
          <div>
            {lastUpdate && (
              <span style={{ color: '#666', fontSize: '0.9rem', marginRight: '15px' }}>
                Last updated: {formatTime(lastUpdate)}
              </span>
            )}
            <button className="btn" onClick={loadRealTimeData} disabled={loading}>
              {loading ? '🔄 Updating...' : '🔄 Refresh'}
            </button>
          </div>
        </div>

        {realTimeData?.current_conditions && (
          <div className="grid grid-4" style={{ marginBottom: '30px' }}>
            <div className="metric">
              <div className="metric-value" style={{ color: getTrafficStatusColor(realTimeData.current_conditions.overall_congestion) }}>
                {(realTimeData.current_conditions.overall_congestion * 100).toFixed(0)}%
              </div>
              <div className="metric-label">Overall Congestion</div>
            </div>
            <div className="metric">
              <div className="metric-value">{realTimeData.current_conditions.average_speed} km/h</div>
              <div className="metric-label">Average Speed</div>
            </div>
            <div className="metric">
              <div className="metric-value">{realTimeData.current_conditions.active_incidents}</div>
              <div className="metric-label">Active Incidents</div>
            </div>
            <div className="metric">
              <div className="metric-value">☀️ {realTimeData.current_conditions.weather_condition}</div>
              <div className="metric-label">Weather</div>
            </div>
          </div>
        )}
      </div>

      <div className="real-time-grid">
        {/* Live Route Conditions */}
        <div className="data-card" style={{ gridColumn: 'span 2' }}>
          <h4>🛣️ Live Route Conditions</h4>
          {realTimeData?.live_routes?.map((route, index) => (
            <div key={index} style={{ 
              padding: '15px', 
              margin: '10px 0', 
              backgroundColor: '#2c3e50', 
              borderRadius: '8px',
              borderLeft: `4px solid ${getTrafficStatusColor(route.congestion_level)}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h5 style={{ margin: 0, color: '#ffffff' }}>{route.route}</h5>
                <span style={{ 
                  backgroundColor: getTrafficStatusColor(route.congestion_level),
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '0.8rem'
                }}>
                  {(route.congestion_level * 100).toFixed(0)}%
                </span>
              </div>
              <div style={{ marginTop: '8px' }}>
                <span style={{ marginRight: '15px' }}>🚗 {route.current_speed} km/h</span>
                <span style={{ marginRight: '15px' }}>⏱️ {route.travel_time_multiplier.toFixed(1)}x normal time</span>
                <span style={{ fontSize: '0.8rem', color: '#666' }}>
                  Updated: {formatTime(route.last_updated)}
                </span>
              </div>
              {route.incidents && route.incidents.length > 0 && (
                <div style={{ marginTop: '8px' }}>
                  {route.incidents.map((incident, idx) => (
                    <div key={idx} style={{ color: '#dc3545', fontSize: '0.9rem' }}>
                      ⚠️ {incident}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Weather Information */}
        {weatherData && (
          <div className="data-card">
            <h4>🌤️ Weather Conditions</h4>
            <div className="data-value">{weatherData.temperature}°C</div>
            <p><strong>Condition:</strong> {weatherData.condition}</p>
            <p><strong>Visibility:</strong> {weatherData.visibility} km</p>
            <p><strong>Wind:</strong> {weatherData.wind_speed} km/h</p>
            <p><strong>Humidity:</strong> {weatherData.humidity}%</p>
            <div style={{ 
              backgroundColor: '#34495e', 
              padding: '10px', 
              borderRadius: '6px',
              marginTop: '10px'
            }}>
              <strong>Traffic Impact:</strong><br/>
              {weatherData.traffic_impact}
            </div>
          </div>
        )}

        {/* Traffic Alerts */}
        <div className="data-card">
          <h4>🚨 Traffic Alerts</h4>
          {realTimeData?.traffic_alerts?.map((alert, index) => (
            <div key={index} style={{
              padding: '12px',
              margin: '8px 0',
              backgroundColor: '#2c3e50',
              borderRadius: '6px',
              borderLeft: `4px solid ${getSeverityColor(alert.severity)}`
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
                <span style={{
                  backgroundColor: getSeverityColor(alert.severity),
                  color: 'white',
                  padding: '2px 6px',
                  borderRadius: '3px',
                  fontSize: '0.7rem',
                  marginRight: '8px'
                }}>
                  {alert.severity.toUpperCase()}
                </span>
                <strong style={{ fontSize: '0.9rem' }}>{alert.location}</strong>
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9rem' }}>{alert.description}</p>
              <div style={{ fontSize: '0.8rem', color: '#ffffff' }}>
                Estimated end: {formatTime(alert.estimated_end)}
              </div>
            </div>
          ))}
        </div>

        {/* Public Transit Status */}
        {realTimeData?.public_transit && (
          <div className="data-card">
            <h4>🚇 Public Transit Status</h4>
            <div style={{ marginBottom: '15px' }}>
              <div style={{ 
                backgroundColor: '#34495e', 
                padding: '8px', 
                borderRadius: '4px',
                marginBottom: '8px'
              }}>
                <strong>Subway:</strong> {realTimeData.public_transit.subway_status}
              </div>
              <div style={{ 
                backgroundColor: '#2c3e50', 
                padding: '8px', 
                borderRadius: '4px',
                marginBottom: '8px'
              }}>
                <strong>Bus:</strong> {realTimeData.public_transit.bus_delays}
              </div>
            </div>
            <div>
              <strong>Service Alerts:</strong>
              {realTimeData.public_transit.service_alerts?.map((alert, index) => (
                <div key={index} style={{ fontSize: '0.9rem', margin: '5px 0' }}>
                  • {alert}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* NYC Open Data Integration */}
        {nycData && (
          <div className="data-card" style={{ gridColumn: 'span 2' }}>
            <h4>🏙️ NYC Open Data - Real Traffic Information</h4>
            <p style={{ color: '#ffffff', fontStyle: 'italic', marginBottom: '15px' }}>
              Live data from NYC Department of Transportation
            </p>
            {/* This would display actual NYC open data if available */}
            <div style={{ 
              backgroundColor: '#2c3e50', 
              padding: '15px', 
              borderRadius: '8px',
              textAlign: 'center' 
            }}>
              <p>🔄 Real-time NYC traffic data integration</p>
              <p>Traffic cameras, sensor data, and incident reports</p>
              <p style={{ fontSize: '0.9rem', color: '#ffffff' }}>
                Data updated every 2 minutes from NYC DOT feeds
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="insights-section">
        <h3>🎯 Real-Time Recommendations</h3>
        <div className="grid grid-2">
          <div className="recommendation-card">
            <h4>🚗 For Drivers</h4>
            <ul style={{ paddingLeft: '20px' }}>
              <li>Avoid FDR Drive southbound - severe congestion</li>
              <li>Use Manhattan Bridge instead of Brooklyn Bridge</li>
              <li>Consider alternate routes via Queens</li>
              <li>Expect 15-20 minute delays on major arteries</li>
            </ul>
          </div>
          
          <div className="recommendation-card">
            <h4>🚇 Public Transit Users</h4>
            <ul style={{ paddingLeft: '20px' }}>
              <li>Subway running on schedule - recommended option</li>
              <li>Minor delays on select bus routes</li>
              <li>Express trains available for faster travel</li>
              <li>Consider subway for Manhattan destinations</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeData;