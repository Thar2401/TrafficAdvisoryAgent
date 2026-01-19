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
                f"Current traffic level is {route['traffic_status'].lower()}",
                f"Average speed expected: {route['speed_kmh']:.0f} km/h"
            ],
            'sustainability_insights': {
                'improvement_opportunities': [
                    f"Fuel consumption: ~{fuel_consumption:.1f}L",
                    f"CO2 emissions: ~{co2_emissions:.1f}kg"
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
st.markdown("### Optimizing urban mobility")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## Control Panel")
    st.success("System Ready")
    
    st.markdown("### Route Preferences")
    time_priority = st.selectbox("Time Priority", ["Low", "Medium", "High", "Critical"], index=2)
    eco_priority = st.selectbox("Environmental Priority", ["Low", "Medium", "High", "Critical"], index=1)
    comfort_priority = st.selectbox("Comfort Priority", ["Level 1 (Low)", "Level 2 (Medium)", "Level 3 (High)", "Level 4 (Critical)"], index=1)
    
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
    preferred_time = st.time_input("Departure Time", value=datetime.now().time())
    time_str = preferred_time.strftime("%H:%M")

# Optional Map (lazy loaded)
show_map = st.checkbox("Show Route Map", value=False)

if show_map and source != destination:
    with st.spinner("Loading map..."):
        src = LOCATION_COORDS[source]
        dst = LOCATION_COORDS[destination]
        
        map_df = pd.DataFrame({
            'Location': [source, destination],
            'Lat': [src[0], dst[0]], 
            'Lon': [src[1], dst[1]],
            'Type': ['Source', 'Destination']
        })
        
        fig = px.scatter_mapbox(
            map_df, lat='Lat', lon='Lon', color='Type',
            hover_name='Location',
            color_discrete_map={'Source': 'red', 'Destination': 'blue'},
            mapbox_style='open-street-map', zoom=11, height=300
        )
        
        fig.add_scattermapbox(
            lat=[src[0], dst[0]], lon=[src[1], dst[1]],
            mode='lines', line=dict(width=3, color='orange'), name='Route'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Analysis button
if st.button("Get Traffic Advisory", type="primary", use_container_width=True):
    if source == destination:
        st.error("Source and destination cannot be the same!")
    else:
        with st.spinner("Analyzing..."):
            rec = advisor.get_route_recommendation(source, destination, time_str)
            
            st.markdown("## Traffic Advisory Results")
            primary = rec['primary_recommendation']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Route", primary['route_description'])
            with col2:
                st.metric("Departure", primary['recommended_departure'])
            with col3:
                st.metric("Travel Time", f"{primary['travel_metrics']['estimated_travel_time_min']:.0f} min")
            with col4:
                st.metric("Traffic Level", primary['travel_metrics']['traffic_level'].title())
            
            # Environmental metrics
            st.markdown("### Environmental Impact")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Distance", f"{primary['travel_metrics']['distance_km']} km")
            with col2:
                st.metric("Fuel Usage", f"{primary['environmental_impact']['fuel_consumption_l']} L")
            with col3:
                st.metric("CO2 Emissions", f"{primary['environmental_impact']['co2_emission_kg']} kg")
            
            # Alternatives
            if rec['alternative_options']:
                st.markdown("### Alternative Departure Times")
                for alt in rec['alternative_options']:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{alt['departure_time']}**")
                    with col2:
                        st.write(f"Travel: {alt['travel_time_min']:.0f} min")
                    with col3:
                        st.write(f"{alt['traffic_status']}")
            
            # Insights
            st.markdown("### Traffic Insights")
            for insight in rec['traffic_insights']:
                st.write(f"• {insight}")
            
            st.markdown("### Sustainability Tips")
            for tip in rec['sustainability_insights']['improvement_opportunities']:
                st.write(f"• {tip}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<strong>AI Traffic Advisory Agent</strong><br>
Traffic optimization for reduced congestion and environmental impact
</div>
""", unsafe_allow_html=True)