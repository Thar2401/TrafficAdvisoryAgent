import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// NYC coordinates for initial map center
const NYC_CENTER = [40.7128, -74.0060];

// NYC location coordinates (approximate)
const NYC_LOCATION_COORDS = {
  'Manhattan - Times Square': [40.7580, -73.9855],
  'Manhattan - Wall Street': [40.7074, -74.0113],
  'Brooklyn - Downtown Brooklyn': [40.6892, -73.9442],
  'Queens - Long Island City': [40.7505, -73.9370],
  'Bronx - Yankee Stadium': [40.8296, -73.9262],
  'Staten Island - St. George': [40.6436, -74.0736],
  'Manhattan - Central Park': [40.7829, -73.9654],
  'Brooklyn - Williamsburg': [40.7081, -73.9571],
  'Queens - Astoria': [40.7698, -73.9442],
  'Manhattan - Greenwich Village': [40.7335, -73.9990],
  'Brooklyn - Park Slope': [40.6710, -73.9778],
  'Queens - Flushing': [40.7677, -73.8335],
  'Bronx - Fordham': [40.8619, -73.8997],
  'Manhattan - Upper East Side': [40.7736, -73.9566],
  'Brooklyn - DUMBO': [40.7033, -73.9887],
  'Queens - Jamaica': [40.6915, -73.8064],
  'Manhattan - Chinatown': [40.7157, -73.9970],
  'Brooklyn - Coney Island': [40.5755, -73.9707],
  'Queens - Forest Hills': [40.7214, -73.8448],
  'Bronx - The Hub': [40.8177, -73.9182]
};

// Create custom icons for different traffic levels
const createTrafficIcon = (level) => {
  const colors = {
    low: '#27ae60',
    medium: '#f39c12',
    high: '#e74c3c',
    severe: '#8b0000'
  };
  
  return L.divIcon({
    className: 'custom-div-icon',
    html: `<div style="
      background-color: ${colors[level] || colors.medium};
      width: 12px;
      height: 12px;
      border-radius: 50%;
      border: 2px solid white;
      box-shadow: 0 0 8px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [12, 12],
    iconAnchor: [6, 6]
  });
};

const TrafficMap = ({ selectedRoute, trafficData = [] }) => {
  const [mapData, setMapData] = useState([]);
  
  useEffect(() => {
    // Generate random traffic data for NYC locations if not provided
    if (trafficData.length === 0) {
      const mockTrafficData = Object.entries(NYC_LOCATION_COORDS).map(([location, coords]) => ({
        location,
        coordinates: coords,
        trafficLevel: ['low', 'medium', 'high', 'severe'][Math.floor(Math.random() * 4)],
        congestion: Math.floor(Math.random() * 100),
        averageSpeed: Math.floor(Math.random() * 50) + 20
      }));
      setMapData(mockTrafficData);
    } else {
      setMapData(trafficData);
    }
  }, [trafficData]);

  // Generate route polyline if selectedRoute is provided
  const routePath = selectedRoute?.source && selectedRoute?.destination ? [
    NYC_LOCATION_COORDS[selectedRoute.source] || NYC_CENTER,
    NYC_LOCATION_COORDS[selectedRoute.destination] || NYC_CENTER
  ] : null;

  return (
    <div className="map-container" style={{ height: '500px', width: '100%', borderRadius: '12px', overflow: 'hidden' }}>
      <MapContainer
        center={NYC_CENTER}
        zoom={11}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />
        
        {/* Traffic markers */}
        {mapData.map((location, index) => (
          location.coordinates && (
            <Marker
              key={index}
              position={location.coordinates}
              icon={createTrafficIcon(location.trafficLevel)}
            >
              <Popup>
                <div style={{ color: '#2c3e50', background: '#ecf0f1', padding: '5px', borderRadius: '4px' }}>
                  <strong style={{ color: '#2c3e50' }}>{location.location}</strong><br/>
                  <span style={{ color: '#34495e' }}>Traffic: {location.trafficLevel || 'medium'}</span><br/>
                  <span style={{ color: '#34495e' }}>Congestion: {location.congestion || 50}%</span><br/>
                  <span style={{ color: '#34495e' }}>Avg Speed: {location.averageSpeed || 35} mph</span>
                </div>
              </Popup>
            </Marker>
          )
        ))}
        
        {/* Route polyline */}
        {routePath && (
          <Polyline
            positions={routePath}
            color="#3498db"
            weight={4}
            opacity={0.8}
          />
        )}
      </MapContainer>
    </div>
  );
};

export default TrafficMap;