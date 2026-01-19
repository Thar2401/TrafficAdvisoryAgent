# Simple Traffic Advisory System - Streamlit App (Optimized)

import streamlit as st

# Page config must be first
st.set_page_config(
    page_title="AI Traffic Advisory Agent", 
    page_icon="", 
    layout="wide"
)

import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import json
import random

# Location coordinates
LOCATION_COORDS = {
    "Downtown": [40.7128, -74.0060],
    "Airport": [40.6892, -73.8844],
    "Business District": [40.7589, -73.9851],
    "University": [40.7282, -73.9942],
    "Residential Area A": [40.7505, -73.9934],
    "Shopping Mall": [40.7505, -73.9956],
    "Hospital": [40.7831, -73.9712],
    "Stadium": [40.8176, -73.9782],
    "Beach": [40.5897, -73.9497],
    "Residential Area B": [40.7648, -73.9808],
    "Financial District": [40.7074, -74.0113],
    "Tech Hub": [40.7419, -73.9891],
    "Industrial Zone": [40.6602, -73.8370],
    "Port Area": [40.6643, -74.0431],
    "Suburban Mall": [40.7282, -73.7949],
    "Medical Center": [40.7899, -73.9441],
    "Convention Center": [40.7505, -73.9934],
    "Train Station": [40.7520, -73.9775],
    "Bus Terminal": [40.7589, -73.9899],
    "City Park": [40.7682, -73.9816],
    "Entertainment District": [40.7580, -73.9855],
    "Historic District": [40.7033, -74.0170],
    "Waterfront": [40.7407, -74.0041],
    "Government Center": [40.7128, -74.0059],
    "Art District": [40.7505, -73.9944]
}

LOCATIONS = list(LOCATION_COORDS.keys())

class SimpleTrafficAdvisor:
    """Simple traffic advisor - optimized for fast loading"""
    
    def __init__(self):
        self.locations = LOCATIONS
        self.traffic_data = self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate minimal sample data for fast loading"""
        data = []
        
        # Only generate for popular routes (16 routes × 8 hours = 128 records vs 14,400)
        common_routes = [
            ("Downtown", "Airport"), ("Airport", "Downtown"),
            ("Downtown", "Business District"), ("Business District", "Downtown"),
            ("University", "Downtown"), ("Downtown", "University"),
            ("Shopping Mall", "Residential Area A"), ("Hospital", "Downtown")
        ]
        
        # Only key hours
        key_hours = [7, 8, 9, 12, 17, 18, 19, 22]
        
        for source, destination in common_routes:
            distance = random.uniform(10, 40)
            base_time = distance * 2.0
            
            for hour in key_hours:
                congestion = self._get_congestion_level(hour)
                actual_time = base_time * (1 + congestion * 0.5)
                speed = distance / (actual_time / 60)
                
                data.append({
                    'source': source,
                    'destination': destination,
                    'distance_km': round(distance, 1),
                    'hour': hour,
                    'base_time_min': round(base_time, 1),
                    'congestion_level': round(congestion, 2),
                    'travel_time_min': round(actual_time, 1),
                    'speed_kmh': round(speed, 1),
                    'traffic_status': self._get_traffic_status(congestion)
                })
        
        return pd.DataFrame(data)
    
    def _get_congestion_level(self, hour):
        """Get congestion level based on hour"""
        if hour in [7, 8, 17, 18]:
            return random.uniform(0.7, 0.9)
        elif hour in [6, 9, 16, 19]:
            return random.uniform(0.5, 0.7)
        elif 10 <= hour <= 15:
            return random.uniform(0.3, 0.5)
        else:
            return random.uniform(0.1, 0.3)
    
    def _get_traffic_status(self, congestion):
        """Convert congestion level to status"""
        if congestion < 0.3:
            return "Low"
        elif congestion < 0.6:
            return "Medium"
        elif congestion < 0.8:
            return "High"
        else:
            return "Severe"
    
    def get_route_recommendation(self, source, destination, preferred_time=None):
        """Get route recommendation"""
        if preferred_time:
            hour = int(preferred_time.split(':')[0])
        else:
            hour = datetime.now().hour
        
        # Find route in data
        route_data = self.traffic_data[
            (self.traffic_data['source'] == source) & 
            (self.traffic_data['destination'] == destination) &
            (self.traffic_data['hour'] == hour)
        ]
        
        # Generate on-the-fly if not found
        if route_data.empty:
            distance = random.uniform(10, 40)
            congestion = self._get_congestion_level(hour)
            base_time = distance * 2.0
            actual_time = base_time * (1 + congestion * 0.5)
            speed = distance / (actual_time / 60)
            
            route = pd.Series({
                'distance_km': round(distance, 1),
                'hour': hour,
                'base_time_min': round(base_time, 1),
                'congestion_level': round(congestion, 2),
                'travel_time_min': round(actual_time, 1),
                'speed_kmh': round(speed, 1),
                'traffic_status': self._get_traffic_status(congestion)
            })
        else:
            route = route_data.iloc[0]
        
        fuel_consumption = route['distance_km'] * 0.08
        co2_emissions = fuel_consumption * 2.31
        
        # Generate alternatives
        alternatives = []
        for offset in [-1, 1]:
            alt_hour = (hour + offset) % 24
            alt_cong = self._get_congestion_level(alt_hour)
            alt_time = route['base_time_min'] * (1 + alt_cong * 0.5)
            
            alternatives.append({
                'departure_time': f"{alt_hour:02d}:00",
                'travel_time_min': round(alt_time, 1),
                'traffic_status': self._get_traffic_status(alt_cong),
                'congestion_level': round(alt_cong, 2)
            })
        
        # Calculate additional insights
        time_saved = max(0, route['base_time_min'] * 1.5 - route['travel_time_min'])
        congestion_pct = int(route['congestion_level'] * 100)
        delay_mins = route['travel_time_min'] - route['base_time_min']
        
        return {
            'primary_recommendation': {
                'route_description': f"{source} to {destination}",
                'recommended_departure': f"{hour:02d}:00",
                'travel_metrics': {
                    'distance_km': route['distance_km'],
                    'estimated_travel_time_min': route['travel_time_min'],
                    'traffic_level': route['traffic_status'].lower(),
                    'speed_kmh': route['speed_kmh']
                },
                'environmental_impact': {
                    'fuel_consumption_l': round(fuel_consumption, 2),
                    'co2_emission_kg': round(co2_emissions, 2)
                },
                'recommendation_strength': 'High' if route['congestion_level'] < 0.5 else 'Medium'
            },
            'alternative_options': alternatives[:3],
            'traffic_insights': [
                f"Current traffic level is {route['traffic_status'].lower()} with {congestion_pct}% congestion",
                f"Average speed expected: {route['speed_kmh']:.0f} km/h on this route",
                f"Expected delay due to traffic: {delay_mins:.1f} minutes",
                f"This route will take {route['travel_time_min']:.0f} min vs {route['base_time_min']:.0f} min in ideal conditions",
                f"Best time to travel: Early morning (5-7 AM) or late evening (8-10 PM)",
                f"Peak congestion hours to avoid: 8-10 AM and 5-7 PM",
                f"Distance to cover: {route['distance_km']} km"
            ],
            'sustainability_insights': {
                'improvement_opportunities': [
                    f"Fuel consumption: ~{fuel_consumption:.1f}L for this journey",
                    f"CO2 emissions: ~{co2_emissions:.1f}kg carbon footprint",
                    f"Consider carpooling to reduce emissions by 50%",
                    f"Public transport could save up to {co2_emissions*0.7:.1f}kg CO2"
                ]
            }
        }

# Initialize advisor (cached for performance)
@st.cache_resource
def get_advisor():
    return SimpleTrafficAdvisor()

advisor = get_advisor()

# Header
st.markdown("# AI Traffic Advisory Agent")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## Control Panel")
    st.success("System Ready")
    
    st.markdown("### Route Preferences")
    time_priority = st.selectbox("Time Priority", ["Low", "Medium", "High", "Critical"], index=2)
    eco_priority = st.selectbox("Environmental Priority", ["Low", "Medium", "High", "Critical"], index=1)
    comfort_priority = st.selectbox("Comfort Priority", ["Low", "Medium", "High", "Critical"], index=1)
    
    st.markdown("---")
    st.info("""
    **Features:**
    - Real-time traffic analysis
    - Fuel efficiency optimization  
    - Environmental impact tracking
    - Smart timing recommendations
    """)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Route Selection")
    source = st.selectbox("From (Source)", advisor.locations, index=0)
    destination = st.selectbox("To (Destination)", advisor.locations, index=1)
    
with col2:
    st.markdown("### Timing")
    preferred_date = st.date_input("Departure Date", value=datetime.now().date())
    preferred_time = st.time_input("Departure Time")
    
    # Use current time if no time selected
    if preferred_time:
        hour = preferred_time.hour
        minute = preferred_time.minute
    else:
        hour = datetime.now().hour
        minute = datetime.now().minute
    time_str = f"{hour:02d}:{minute:02d}"

# Route Map (shown by default)
if source != destination:
    st.markdown("### 🗺️ Route Map")
    with st.spinner("Loading map..."):
        src = LOCATION_COORDS[source]
        dst = LOCATION_COORDS[destination]
        
        # Create route points with intermediate waypoints for street-level routing
        lat_steps = np.linspace(src[0], dst[0], 20)
        lon_steps = np.linspace(src[1], dst[1], 20)
        
        map_df = pd.DataFrame({
            'Location': [source, destination],
            'Lat': [src[0], dst[0]], 
            'Lon': [src[1], dst[1]],
            'Type': ['Source', 'Destination']
        })
        
        fig = px.scatter_mapbox(
            map_df, lat='Lat', lon='Lon', color='Type',
            hover_name='Location',
            color_discrete_map={'Source': '#FF4B4B', 'Destination': '#00CC66'},
            mapbox_style='open-street-map', zoom=11, height=800,
            size=[30, 30]  # Bigger marker dots
        )
        
        # Add route line with intermediate points for street-following effect
        fig.add_scattermapbox(
            lat=lat_steps.tolist(), lon=lon_steps.tolist(),
            mode='lines+markers', 
            line=dict(width=5, color='#1E90FF'),
            marker=dict(size=3, color='#1E90FF'),
            name='Route',
            showlegend=False
        )
        
        fig.update_layout(
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            mapbox=dict(style='open-street-map', zoom=12)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Analysis button
if st.button("Get Traffic Advisory", type="primary", use_container_width=True):
    if source == destination:
        st.error("Source and destination cannot be the same!")
    else:
        with st.spinner("Analyzing..."):
            rec = advisor.get_route_recommendation(source, destination, time_str)
            
            st.markdown("## 🎯 Traffic Advisory Results")
            primary = rec['primary_recommendation']
            
            # Route description in full width with colored background
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
                <h3 style='margin: 0; color: white;'>📍 {primary['route_description']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""<div style='background-color: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;'>
                            <h4 style='color: #2E7D32; margin: 0;'>🕐 Departure</h4>
                            <h2 style='color: #1B5E20; margin: 5px 0;'>{}</h2>
                            </div>""".format(primary['recommended_departure']), unsafe_allow_html=True)
            with col2:
                st.markdown("""<div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;'>
                            <h4 style='color: #1565C0; margin: 0;'>⏱️ Travel Time</h4>
                            <h2 style='color: #0D47A1; margin: 5px 0;'>{:.0f} min</h2>
                            </div>""".format(primary['travel_metrics']['estimated_travel_time_min']), unsafe_allow_html=True)
            with col3:
                traffic_colors = {'low': '#4CAF50', 'medium': '#FF9800', 'high': '#FF5722', 'severe': '#D32F2F'}
                traffic_level = primary['travel_metrics']['traffic_level']
                color = traffic_colors.get(traffic_level, '#757575')
                st.markdown("""<div style='background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 4px solid {};'>
                            <h4 style='color: {}; margin: 0;'>🚦 Traffic Level</h4>
                            <h2 style='color: {}; margin: 5px 0;'>{}</h2>
                            </div>""".format(color, color, color, traffic_level.title()), unsafe_allow_html=True)
            
            # Environmental metrics
            st.markdown("### 🌱 Environmental Impact")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""<div style='background: linear-gradient(135deg, #FFA726 0%, #FB8C00 100%); 
                            padding: 15px; border-radius: 10px; text-align: center; color: white;'>
                            <p style='margin: 0; font-size: 14px;'>Distance</p>
                            <h2 style='margin: 5px 0; color: white;'>{} km</h2>
                            </div>""".format(primary['travel_metrics']['distance_km']), unsafe_allow_html=True)
            with col2:
                st.markdown("""<div style='background: linear-gradient(135deg, #66BB6A 0%, #43A047 100%); 
                            padding: 15px; border-radius: 10px; text-align: center; color: white;'>
                            <p style='margin: 0; font-size: 14px;'>Fuel Usage</p>
                            <h2 style='margin: 5px 0; color: white;'>{} L</h2>
                            </div>""".format(primary['environmental_impact']['fuel_consumption_l']), unsafe_allow_html=True)
            with col3:
                st.markdown("""<div style='background: linear-gradient(135deg, #42A5F5 0%, #1E88E5 100%); 
                            padding: 15px; border-radius: 10px; text-align: center; color: white;'>
                            <p style='margin: 0; font-size: 14px;'>CO2 Emissions</p>
                            <h2 style='margin: 5px 0; color: white;'>{} kg</h2>
                            </div>""".format(primary['environmental_impact']['co2_emission_kg']), unsafe_allow_html=True)
            
            # Alternatives
            if rec['alternative_options']:
                st.markdown("### 🔀 Alternative Departure Times")
                for i, alt in enumerate(rec['alternative_options']):
                    status_colors = {'Low': '#4CAF50', 'Medium': '#FF9800', 'High': '#FF5722', 'Severe': '#D32F2F'}
                    bg_colors = {'Low': '#E8F5E9', 'Medium': '#FFF3E0', 'High': '#FFEBEE', 'Severe': '#FFCDD2'}
                    status = alt['traffic_status']
                    st.markdown("""
                    <div style='background-color: {}; padding: 12px; border-radius: 8px; 
                                margin: 8px 0; border-left: 4px solid {};'>
                        <span style='font-weight: bold; font-size: 18px; color: {};'>⏰ {}</span>
                        <span style='margin-left: 20px; color: #555;'>Travel: <strong>{:.0f} min</strong></span>
                        <span style='margin-left: 20px; color: {}; font-weight: bold;'>Traffic: {}</span>
                    </div>
                    """.format(bg_colors.get(status, '#F5F5F5'), status_colors.get(status, '#757575'),
                              status_colors.get(status, '#757575'), alt['departure_time'], 
                              alt['travel_time_min'], status_colors.get(status, '#757575'), status), unsafe_allow_html=True)
            
            # Insights
            st.markdown("### 💡 Traffic Insights")
            for i, insight in enumerate(rec['traffic_insights']):
                st.markdown("""
                <div style='background: linear-gradient(90deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 12px 20px; border-radius: 8px; margin: 8px 0; 
                            border-left: 4px solid #2196F3;'>
                    <p style='margin: 0; color: #0D47A1; font-size: 15px;'>🔹 {}</p>
                </div>
                """.format(insight), unsafe_allow_html=True)
            
            st.markdown("### 🌿 Sustainability Tips")
            for i, tip in enumerate(rec['sustainability_insights']['improvement_opportunities']):
                st.markdown("""
                <div style='background: linear-gradient(90deg, #E8F5E9 0%, #C8E6C9 100%); 
                            padding: 12px 20px; border-radius: 8px; margin: 8px 0; 
                            border-left: 4px solid #4CAF50;'>
                    <p style='margin: 0; color: #1B5E20; font-size: 15px;'>🌱 {}</p>
                </div>
                """.format(tip), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<strong>AI Traffic Advisory Agent</strong><br>
Traffic optimization for reduced congestion and environmental impact
</div>
""", unsafe_allow_html=True)