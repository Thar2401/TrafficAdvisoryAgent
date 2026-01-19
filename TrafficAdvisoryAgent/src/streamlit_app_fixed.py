# Streamlit web application for Traffic Advisory Agent

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the traffic agent
try:
    from src.traffic_agent import TrafficAdvisoryAgent
    from utils.config import Config
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all dependencies are installed and the project structure is correct.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Traffic Advisory Agent",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.insight-box {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
    margin: 0.5rem 0;
}
.recommendation-box {
    background-color: #e8f5e8;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 0.5rem 0;
}
.warning-box {
    background-color: #fff3cd;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'last_recommendations' not in st.session_state:
    st.session_state.last_recommendations = None
if 'agent_initialized' not in st.session_state:
    st.session_state.agent_initialized = False

def initialize_agent():
    """Initialize the traffic agent"""
    if not st.session_state.agent_initialized:
        with st.spinner('🚦 Initializing AI Traffic Agent... This may take a moment.'):
            try:
                st.session_state.agent = TrafficAdvisoryAgent(auto_load_data=True)
                st.session_state.agent_initialized = True
                return True
            except Exception as e:
                st.error(f"Failed to initialize agent: {str(e)}")
                st.error("Please check that all data files are present and dependencies are installed.")
                return False
    return True

def display_main_header():
    """Display the main application header"""
    st.markdown('<h1 class="main-header">🚦 AI-Based Traffic Advisory Agent</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem;'>🎯 <strong>SDG 11: Sustainable Cities and Communities</strong> - Optimizing urban mobility for a sustainable future</p>", unsafe_allow_html=True)
    st.markdown("---")

def display_sidebar():
    """Display sidebar with controls and information"""
    st.sidebar.image("https://via.placeholder.com/200x100/1f77b4/white?text=Traffic+Agent", width=200)
    
    st.sidebar.markdown("## 🎛️ Control Panel")
    
    # Agent status
    if st.session_state.agent_initialized:
        st.sidebar.success("✅ Agent Ready")
        
        # Display agent status
        if st.sidebar.button("📊 Show Agent Status"):
            try:
                status = st.session_state.agent.get_agent_status()
                st.sidebar.json(status)
            except Exception as e:
                st.sidebar.error(f"Error getting status: {e}")
    else:
        st.sidebar.error("❌ Agent Not Initialized")
    
    st.sidebar.markdown("---")
    
    # User preferences
    st.sidebar.markdown("### ⚙️ Optimization Preferences")
    
    travel_time_weight = st.sidebar.slider("Travel Time Priority", 0.0, 1.0, 0.4, 0.1)
    congestion_weight = st.sidebar.slider("Congestion Avoidance", 0.0, 1.0, 0.3, 0.1)
    fuel_weight = st.sidebar.slider("Fuel Efficiency", 0.0, 1.0, 0.2, 0.1)
    env_weight = st.sidebar.slider("Environmental Impact", 0.0, 1.0, 0.1, 0.1)
    
    # Normalize weights
    total_weight = travel_time_weight + congestion_weight + fuel_weight + env_weight
    if total_weight > 0:
        user_preferences = {
            'travel_time': travel_time_weight / total_weight,
            'congestion': congestion_weight / total_weight,
            'fuel_efficiency': fuel_weight / total_weight,
            'environmental_impact': env_weight / total_weight
        }
    else:
        user_preferences = None
    
    st.sidebar.markdown("---")
    
    # About section
    st.sidebar.markdown("### 📖 About")
    st.sidebar.info("""
    This AI agent helps optimize your travel routes considering:
    - 🚦 Real-time traffic patterns
    - ⛽ Fuel efficiency
    - 🌱 Environmental impact
    - ⏰ Time optimization
    
    **Sustainable Development Goal 11**: Making cities inclusive, safe, resilient and sustainable.
    """)
    
    return user_preferences

def display_route_planner():
    """Display the main route planning interface"""
    st.markdown("## 🗺️ Route Planner")
    
    if not st.session_state.agent_initialized:
        st.warning("⚠️ Please wait while the agent initializes...")
        return None, None, None
    
    try:
        # Get available locations
        available_locations = st.session_state.agent.perception.get_available_locations()
    except Exception as e:
        st.error(f"Error getting locations: {e}")
        return None, None, None
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        source = st.selectbox(
            "📍 From (Source)",
            available_locations,
            index=0 if available_locations else None,
            help="Select your starting location"
        )
    
    with col2:
        destination = st.selectbox(
            "🎯 To (Destination)", 
            available_locations,
            index=1 if len(available_locations) > 1 else 0,
            help="Select your destination"
        )
    
    with col3:
        preferred_time = st.time_input(
            "🕐 Preferred Time",
            value=datetime.now().time(),
            help="Your preferred departure time"
        )
    
    return source, destination, preferred_time.strftime("%H:%M")

def process_route_request(source, destination, preferred_time, user_preferences):
    """Process the route request and display results"""
    if not all([source, destination]):
        st.warning("Please select both source and destination.")
        return
    
    if source == destination:
        st.error("Source and destination cannot be the same!")
        return
    
    # Process request button
    if st.button("🚀 Get Traffic Advisory", type="primary"):
        with st.spinner('🔄 Analyzing traffic patterns and optimizing routes...'):
            try:
                # Process the request
                recommendations = st.session_state.agent.process_request(
                    source=source,
                    destination=destination,
                    preferred_time=preferred_time,
                    user_preferences=user_preferences
                )
                
                st.session_state.last_recommendations = recommendations
                
                if 'error' in recommendations:
                    st.error(f"❌ {recommendations['error']}")
                    return
                
                display_recommendations(recommendations)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

def display_recommendations(recommendations):
    """Display the traffic recommendations"""
    st.markdown("## 🎯 Traffic Advisory Results")
    
    # Primary recommendation
    primary = recommendations.get('primary_recommendation', {})
    
    if 'error' not in primary and primary:
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.markdown("### 🌟 **Primary Recommendation**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🛣️ Route", 
                primary.get('route_description', 'N/A'),
                help="Recommended route"
            )
        
        with col2:
            st.metric(
                "🕐 Departure", 
                primary.get('recommended_departure', 'N/A'),
                help="Optimal departure time"
            )
        
        with col3:
            travel_metrics = primary.get('travel_metrics', {})
            travel_time = travel_metrics.get('estimated_travel_time_min', 'N/A')
            st.metric(
                "⏱️ Travel Time", 
                f"{travel_time} min" if travel_time != 'N/A' else travel_time,
                help="Estimated travel duration"
            )
        
        with col4:
            traffic_level = travel_metrics.get('traffic_level', 'N/A')
            st.metric(
                "🚦 Traffic Level", 
                traffic_level.title() if traffic_level != 'N/A' else traffic_level,
                help="Expected traffic conditions"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No primary recommendation available.")
    
    # Display basic recommendation info if available
    if recommendations:
        st.success("✅ Analysis completed successfully!")
        st.json(recommendations)

def main():
    """Main application function"""
    # Initialize agent
    initialize_success = initialize_agent()
    
    # Display header
    display_main_header()
    
    # Display sidebar and get preferences
    user_preferences = display_sidebar()
    
    if not initialize_success:
        st.error("⚠️ Unable to initialize the Traffic Advisory Agent. Please check the setup and try again.")
        st.info("Make sure all required files are present in the project directory.")
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["🗺️ Route Planner", "📊 Results"])
    
    with tab1:
        # Main route planning interface
        source, destination, preferred_time = display_route_planner()
        
        if st.session_state.agent_initialized and source and destination:
            process_route_request(source, destination, preferred_time, user_preferences)
    
    with tab2:
        # Display last results
        st.markdown("## 📋 Last Results")
        
        if st.session_state.last_recommendations:
            st.markdown("### 📄 Last Recommendation Results")
            
            # Display results
            st.json(st.session_state.last_recommendations)
            
            # Download button
            if st.button("📥 Download JSON"):
                json_data = json.dumps(st.session_state.last_recommendations, indent=2, default=str)
                st.download_button(
                    label="Download JSON Report",
                    data=json_data,
                    file_name=f"traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        else:
            st.info("🔍 No results to display. Please run a route analysis first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        🌍 <strong>Contributing to SDG 11: Sustainable Cities and Communities</strong><br>
        AI-powered traffic optimization for reduced congestion and environmental impact
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()