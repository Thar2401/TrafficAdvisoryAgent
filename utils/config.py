# Configuration settings for Traffic Advisory Agent

from datetime import datetime
import os

class Config:
    """
    Configuration class for Traffic Advisory Agent
    """
    
    # Data paths
    DATA_DIR = "data"
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    SIMULATED_DATA_DIR = os.path.join(DATA_DIR, "simulated")
    
    # Model parameters
    TRAFFIC_PREDICTION_MODEL = {
        'random_state': 42,
        'test_size': 0.2,
        'n_estimators': 100
    }
    
    # Route optimization settings
    MAX_ALTERNATIVE_ROUTES = 5
    CONGESTION_THRESHOLD = 0.7
    
    # Time settings
    HOURS_IN_DAY = 24
    DAYS_IN_WEEK = 7
    
    # Traffic levels
    TRAFFIC_LEVELS = {
        'low': (0.0, 0.3),
        'medium': (0.3, 0.6), 
        'high': (0.6, 0.8),
        'severe': (0.8, 1.0)
    }
    
    # Sustainability metrics
    FUEL_CONSUMPTION_BASE = 0.08  # L/km
    CO2_EMISSION_FACTOR = 2.31    # kg CO2/L fuel
    
    # UI settings
    STREAMLIT_CONFIG = {
        'page_title': 'Traffic Advisory Agent',
        'page_icon': '🚦',
        'layout': 'wide'
    }
    
    # Sample locations for demo
    DEMO_LOCATIONS = [
        'Downtown',
        'Airport',
        'University',
        'Shopping Mall',
        'Business District',
        'Residential Area A',
        'Residential Area B',
        'Industrial Zone',
        'Hospital',
        'Train Station'
    ]
    
    @staticmethod
    def get_traffic_level_from_score(score):
        """Convert congestion score to traffic level"""
        for level, (min_val, max_val) in Config.TRAFFIC_LEVELS.items():
            if min_val <= score < max_val:
                return level
        return 'severe'  # Default for score >= 0.8