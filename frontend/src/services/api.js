import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const trafficAPI = {
  // Get available locations
  getLocations: () => api.get('/locations'),
  
  // Get route recommendations
  getRouteRecommendations: (data) => api.post('/route-recommendations', data),
  
  // Get traffic insights
  getTrafficInsights: (location, hour) => api.get(`/traffic-insights?location=${location || ''}&hour=${hour || ''}`),
  
  // Get real-time data
  getRealTimeData: () => api.get('/real-time-data'),
  
  // Get dashboard data
  getDashboardData: () => api.get('/dashboard-data'),
  
  // Get historical traffic data
  getHistoricalData: (startDate, endDate, location) => 
    api.get(`/historical-data?start=${startDate}&end=${endDate}&location=${location || ''}`),
  
  // Get NYC open data (real traffic data)
  getNYCTrafficData: () => api.get('/nyc-traffic-data'),
  
  // Get weather data
  getWeatherData: (location) => api.get(`/weather-data?location=${location}`),
  
  // Health check
  healthCheck: () => api.get('/health'),
};

export default api;