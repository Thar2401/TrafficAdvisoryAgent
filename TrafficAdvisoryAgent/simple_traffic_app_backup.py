# Simple Traffic Advisory System - Streamlit App

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

# Location coordinates for map functionality
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
    """Simple traffic advisor with basic functionality"""
    
    def __init__(self):
        self.locations = LOCATIONS
        self.traffic_data = self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample traffic data - optimized for faster loading"""
        data = []
        
        # Only generate data for most common routes (not all combinations)
        # This reduces initial load from 14,400 records to ~300 records
        common_routes = [
            ("Downtown", "Airport"), ("Airport", "Downtown"),
            ("Downtown", "Business District"), ("Business District", "Downtown"),
            ("University", "Downtown"), ("Downtown", "University"),
            ("Shopping Mall", "Residential Area A"), ("Residential Area A", "Shopping Mall"),
            ("Hospital", "Downtown"), ("Downtown", "Hospital"),
            ("Stadium", "Downtown"), ("Downtown", "Stadium"),
            ("Financial District", "Business District"), ("Tech Hub", "Downtown"),
            ("Airport", "Business District"), ("Beach", "Downtown")
        ]
        
        for source, destination in common_routes:
            distance = random.uniform(5, 50)
            base_time = distance * random.uniform(1.5, 3)
            
            # Generate data for key hours only (not all 24 hours)
            key_hours = [7, 8, 9, 12, 17, 18, 19, 22]
            for hour in key_hours:
                congestion = self._get_congestion_level(hour)
                actual_time = base_time * (1 + congestion * 0.5)
                speed = distance / (actual_time / 60) if actual_time > 0 else 30
                
                data.append({
                    'route_id': f"{source}_{destination}",
                    'source': source,
                    'destination': destination,
                    'distance_km': round(distance, 1),
                    'hour': hour,
                    'base_time_min': round(base_time, 1),
                    'congestion_level': round(congestion, 2),
                    'travel_time_min': round(actual_time, 1),
                    'speed_kmh': round(speed, 1),
                    'traffic_status': self._get_traffic_status(congestion)
                data.append({
                            'route_id': route_id,
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
        # Rush hours: 7-9 AM and 5-7 PM
        if hour in [7, 8, 17, 18]:
            return random.uniform(0.7, 0.9)
        elif hour in [6, 9, 16, 19]:
            return random.uniform(0.5, 0.7)
        elif hour in [10, 11, 12, 13, 14, 15]:
            return random.uniform(0.3, 0.5)
        else:
            return random.uniform(0.1, 0.3)
    
    def _get_traffic_status(self, congestion):
        """Convert congestion level to status"""
        if congestion < 0.3:
            return "Low"
        # If no exact match, generate estimate on the fly
        if route_data.empty:
            # Quick estimate based on typical patterns
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
                return "High"
        else:
            return "Severe"
    
    def get_route_recommendation(self, source, destination, preferred_time=None, priorities=None):
        """Get route recommendation"""
        if preferred_time:
            hour = int(preferred_time.split(':')[0])
        else:
            hour = datetime.now().hour
        
        # Convert priority levels to weights
        priority_weights = {}
        if priorities:
            for key, level in priorities.items():
                level_num = int(level.split()[1]) if 'Level' in level else 2
                priority_weights[key] = level_num / 4.0  # Normalize to 0-1
        
        # Find the route
        route_data = self.traffic_data[
            (self.traffic_data['source'] == source) & 
            (self.traffic_data['destination'] == destination) &
            (self.traffic_data['hour'] == hour)
        ]
        
        if route_data.empty:
            return {"error": f"No route found from {source} to {destination}"}
        
        route = route_data.iloc[0]
        
        # Calculate environmental impact
        fuel_consumption = route['distance_km'] * 0.08  # L/km
        co2_emissions = fuel_consumption * 2.31  # kg CO2/L
        
        # Generate alternative times
        alternatives = []
        for alt_hour in [hour-1, hour+1, hour-2, hour+2]:
            alt_hour = alt_hour % 24
            alt_data = self.traffic_data[
                (self.traffic_data['source'] == source) & 
                (self.traffic_data['destination'] == destination) &
                (self.traffic_data['hour'] == alt_hour)
            ]
            if not alt_data.empty:
                alt_route = alt_data.iloc[0]
                alternatives.append({
                    'departure_time': f"{alt_hour:02d}:00",
                    'travel_time_min': alt_route['travel_time_min'],
                    'traffic_status': alt_route['traffic_status'],
                    'congestion_level': alt_route['congestion_level']
                })
        
        recommendation = {
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
                f"Average speed expected: {route['speed_kmh']} km/h",
                f"Travel time is {int((route['travel_time_min'] / route['base_time_min'] - 1) * 100)}% longer than base time due to traffic"
            ],
            'sustainability_insights': {
                'improvement_opportunities': [
                    f"This route will consume approximately {fuel_consumption:.1f}L of fuel",
                    f"CO2 emissions for this trip: {co2_emissions:.1f}kg",
                    "Consider carpooling to reduce environmental impact",
                    "Off-peak travel can reduce fuel consumption by up to 20%"
                ]
            },
            'action_items': [
                {
                    'action': 'Departure Time',
                    'description': f"Leave at {hour:02d}:00 for optimal travel time",
                    'priority': 'high'
        # If no data, generate quick estimate
        if route_data.empty:
            # Generate hourly estimates on the fly
            hourly_data = []
            for hour in range(24):
                congestion = self._get_congestion_level(hour)
                distance = random.uniform(10, 40)
                base_time = distance * 2.0
                actual_time = base_time * (1 + congestion * 0.5)
                speed = distance / (actual_time / 60)
                
                hourly_data.append({
                    'hour': hour,
                    'congestion_level': round(congestion, 2),
                    'travel_time_min': round(actual_time, 1),
                    'speed_kmh': round(speed, 1)
                })
            
            return {
                'hourly_data': hourly_data,
                'peak_hours': sorted(hourly_data, key=lambda x: x['congestion_level'], reverse=True)[:3],
                'best_hours': sorted(hourly_data, key=lambda x: x['congestion_level'])[:3]
            }
                    'action': 'Alternative Route Check',
                    'description': "Monitor real-time traffic for potential delays",
                    'priority': 'medium'
                }
            ]
        }
        
        return recommendation
    
    def get_traffic_analysis(self, source, destination):
        """Get traffic analysis for visualization"""
        route_data = self.traffic_data[
            (self.traffic_data['source'] == source) & 
            (self.traffic_data['destination'] == destination)
        ]
        
        # If no data, generate quick estimate
        if route_data.empty:
            # Generate hourly estimates on the fly
            hourly_data = []
            for hour in range(24):
                congestion = self._get_congestion_level(hour)
                distance = random.uniform(10, 40)
                base_time = distance * 2.0
                actual_time = base_time * (1 + congestion * 0.5)
                speed = distance / (actual_time / 60)
                
                hourly_data.append({
                    'hour': hour,
                    'congestion_level': round(congestion, 2),
                    'travel_time_min': round(actual_time, 1),
                    'speed_kmh': round(speed, 1)
                })
            
            return {
                'hourly_data': hourly_data,
                'peak_hours': sorted(hourly_data, key=lambda x: x['congestion_level'], reverse=True)[:3],
                'best_hours': sorted(hourly_data, key=lambda x: x['congestion_level'])[:3]
            }
        
        return {
            'hourly_data': route_data[['hour', 'congestion_level', 'travel_time_min', 'speed_kmh']].to_dict('records'),
            'peak_hours': route_data.nlargest(3, 'congestion_level')[['hour', 'congestion_level']].to_dict('records'),
            'best_hours': route_data.nsmallest(3, 'congestion_level')[['hour', 'congestion_level']].to_dict('records')
        }

def create_location_map(selected_source=None, selected_dest=None):
    """Create an interactive map with location markers"""
    if not MAP_AVAILABLE:
        return None
    
    # Center map on NYC
    m = folium.Map(
        location=[40.7128, -74.0060],
        zoom_start=11,
        tiles="OpenStreetMap"
    )
    
    # Add markers for all locations
    for location, coords in LOCATION_COORDS.items():
        color = 'red' if location == selected_source else 'blue' if location == selected_dest else 'green'
        folium.Marker(
            coords,
            popup=f"<b>{location}</b>",
            tooltip=location,
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # Add route line if both locations selected
    if selected_source and selected_dest and selected_source != selected_dest:
        source_coords = LOCATION_COORDS[selected_source]
        dest_coords = LOCATION_COORDS[selected_dest]
        
        folium.PolyLine(
            locations=[source_coords, dest_coords],
            weight=4,
            color='orange', with priorities
            priority_dict = {
                'time': time_priority,
  Interactive Map Section (Simplified)
st.markdown("### Route Visualization")
st.markdown("**Location Map:** Select locations from dropdowns above to see route details")

# Create a simple scatter plot map using plotly
if source != destination:
    source_coords = LOCATION_COO with priorities
            priority_dict = {
                'time': time_priority,
                'environmental': eco_priority,
                'comfort': comfort_priority
            }
            recommendation = advisor.get_route_recommendation(source, destination, time_str, priority_dict
    
    # Create map data
    map_df = pd.DataFrame({
        'Location': [source, destination],
        'Latitude': [source_coords[0], dest_coords[0]], 
        'Longitude': [source_coords[1], dest_coords[1]],
        'Type': ['Source', 'Destination']
    })
    
    # Add other locations
    other_locations = [loc for loc in LOCATIONS if loc not in [source, destination]][:10]  # Limit to 10 for clarity
    for loc in other_locations:
        coords = LOCATION_COORDS[loc]
        new_row = pd.DataFrame({
            'Location': [loc],
            'Latitude': [coords[0]],
            'Longitude': [coords[1]],
            'Type': ['Other']
        })
        map_df = pd.concat([map_df, new_row], ignore_index=True)
    
    # Create interactive map
    fig = px.scatter_mapbox(
        map_df,
        lat='Latitude',
        lon='Longitude', 
        color='Type',
        hover_name='Location',
        color_discrete_map={'Source': 'red', 'Destination': 'blue', 'Other': 'green'},
        mapbox_style='open-street-map',
        zoom=10,
        height=400,
        title=f"Route from {source} to {destination}"
    )
    
    # Add route line
    fig.add_scattermapbox(
        lat=[source_coords[0], dest_coords[0]],
        lon=[source_coords[1], dest_coords[1]],
        mode='lines',
        line=dict(width=3, color='orange'),
        name='Route'
    )
    
    st.plotly_chart(fig, use_container_width=True)

#               'environmental': eco_priority,
                'comfort': comfort_priority
            }
            recommendation = advisor.get_route_recommendation(source, destination, time_str, priority_dict
        ).add_to(m)
    
    return m

# Initialize the advisor
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
    time_priority = st.selectbox("Time Priority", ["Level 1 (Low)", "Level 2 (Medium)", "Level 3 (High)", "Level 4 (Critical)"], index=2)
    eco_priority = st.selectbox("Environmental Priority", ["Level 1 (Low)", "Level 2 (Medium)", "Level 3 (High)", "Level 4 (Critical)"], index=1)
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
    
    # Alternative: Time slider (commented out for now)
    # hour = st.slider("Departure Hour", 0, 23, datetime.now().hour)
    # minute = st.slider("Departure Minute", 0, 59, datetime.now().minute, step=15)
    # preferred_time = f"{hour:02d}:{minute:02d}"
    
    time_str = preferred_time.strftime("%H:%M")

# Interactive Map Section
if MAP_AVAILABLE:
    st.markdown("### Interactive Route Map")
    st.markdown("**Red marker:** Source | **Blue marker:** Destination | **Green markers:** Other locations")
    
    # Create and display map
    route_map = create_location_map(source, destination)
    if route_map:
        map_data = st_folium(route_map, width=700, height=400)
        
        # Check if user clicked on map
        if map_data['last_object_clicked_popup']:
            clicked_location = map_data['last_object_clicked_popup']
            st.info(f"You clicked on: {clicked_location}")

# Analysis button
if st.button("Get Traffic Advisory", type="primary", use_container_width=True):
    if source == destination:
        st.error("Source and destination cannot be the same!")
    else:
        with st.spinner("Analyzing traffic patterns..."):
            # Get recommendation
            recommendation = advisor.get_route_recommendation(source, destination, time_str)
            
            if 'error' in recommendation:
                st.error(f"{recommendation['error']}")
            else:
                # Display results
                st.markdown("## Traffic Advisory Results")
                
                # Primary recommendation
                primary = recommendation['primary_recommendation']
                
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
                
                # Traffic analysis visualization
                analysis = advisor.get_traffic_analysis(source, destination)
                if analysis:
                    st.markdown("### Traffic Analysis")
                    
                    # Create hourly traffic chart
                    hourly_df = pd.DataFrame(analysis['hourly_data'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.line(hourly_df, x='hour', y='congestion_level', 
                                     title="Hourly Congestion Levels",
                                     labels={'hour': 'Hour of Day', 'congestion_level': 'Congestion Level'})
                        fig.update_traces(line_color='#ff6b6b')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(hourly_df, x='hour', y='travel_time_min',
                                    title="Travel Time by Hour",
                                    labels={'hour': 'Hour of Day', 'travel_time_min': 'Travel Time (min)'})
                        fig.update_traces(marker_color='#4ecdc4')
                        st.plotly_chart(fig, use_container_width=True)
                
                # Alternative options
                if recommendation['alternative_options']:
                    st.markdown("### Alternative Departure Times")
                    for i, alt in enumerate(recommendation['alternative_options']):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{alt['departure_time']}**")
                        with col2:
                            st.write(f"Travel: {alt['travel_time_min']:.0f} min")
                        with col3:
                            status_color = {"Low": "green", "Medium": "orange", "High": "red", "Severe": "darkred"}
                            color = status_color.get(alt['traffic_status'], "blue")
                            st.markdown(f"<span style='color:{color}'>{alt['traffic_status']}</span>", unsafe_allow_html=True)
                
                # Insights
                st.markdown("### Traffic Insights")
                for insight in recommendation['traffic_insights']:
                    st.write(f"• {insight}")
                
                # Sustainability tips
                st.markdown("### Sustainability Tips")
                for tip in recommendation['sustainability_insights']['improvement_opportunities']:
                    st.write(f"• {tip}")
                
                # Action items
                st.markdown("### Action Items")
                for action in recommendation['action_items']:
                    st.write(f"**{action['action']}**: {action['description']} (Priority: {action['priority']})")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<strong>AI Traffic Advisory Agent</strong><br>
Traffic optimization for reduced congestion and environmental impact
</div>
""", unsafe_allow_html=True)