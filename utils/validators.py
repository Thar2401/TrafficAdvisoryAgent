# Input validation utilities for Traffic Advisory Agent

import re
from datetime import datetime, time
from typing import Optional, Tuple

class InputValidator:
    """
    Validation utilities for user inputs and data
    """
    
    @staticmethod
    def validate_location(location: str) -> bool:
        """
        Validate if location string is acceptable
        
        Args:
            location: Location string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not location or not isinstance(location, str):
            return False
        
        # Check length
        if len(location.strip()) < 2 or len(location.strip()) > 100:
            return False
            
        # Check for valid characters (letters, numbers, spaces, common punctuation)
        pattern = r'^[a-zA-Z0-9\s\-_.,()]+$'
        return bool(re.match(pattern, location.strip()))
    
    @staticmethod
    def validate_time_preference(time_str: str) -> Optional[int]:
        """
        Validate and convert time string to hour (0-23)
        
        Args:
            time_str: Time string in format 'HH:MM' or just 'HH'
            
        Returns:
            Optional[int]: Hour (0-23) if valid, None otherwise
        """
        if not time_str or not isinstance(time_str, str):
            return None
            
        time_str = time_str.strip()
        
        try:
            # Try parsing as HH:MM format
            if ':' in time_str:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
                return time_obj.hour
            
            # Try parsing as just hour
            hour = int(time_str)
            if 0 <= hour <= 23:
                return hour
            
        except (ValueError, TypeError):
            pass
            
        return None
    
    @staticmethod
    def validate_congestion_score(score: float) -> bool:
        """
        Validate congestion score is within valid range
        
        Args:
            score: Congestion score to validate
            
        Returns:
            bool: True if valid (0.0 <= score <= 1.0)
        """
        return isinstance(score, (int, float)) and 0.0 <= score <= 1.0
    
    @staticmethod
    def validate_route_data(route_data: dict) -> Tuple[bool, str]:
        """
        Validate route data dictionary contains required fields
        
        Args:
            route_data: Dictionary containing route information
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        required_fields = [
            'route_id', 'source', 'destination', 'distance_km',
            'hour', 'day_of_week', 'traffic_level', 'congestion_score',
            'avg_speed_kmh', 'travel_time_min', 'fuel_consumption_l',
            'co2_emission_kg'
        ]
        
        if not isinstance(route_data, dict):
            return False, "Route data must be a dictionary"
        
        # Check required fields exist
        missing_fields = [field for field in required_fields 
                         if field not in route_data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate specific field types and ranges
        validations = [
            (isinstance(route_data['route_id'], str), "route_id must be string"),
            (isinstance(route_data['source'], str), "source must be string"),
            (isinstance(route_data['destination'], str), "destination must be string"),
            (isinstance(route_data['distance_km'], (int, float)) and route_data['distance_km'] > 0, 
             "distance_km must be positive number"),
            (isinstance(route_data['hour'], int) and 0 <= route_data['hour'] <= 23, 
             "hour must be integer 0-23"),
            (isinstance(route_data['day_of_week'], int) and 0 <= route_data['day_of_week'] <= 6,
             "day_of_week must be integer 0-6"),
            (route_data['traffic_level'] in ['low', 'medium', 'high', 'severe'],
             "traffic_level must be one of: low, medium, high, severe"),
            (InputValidator.validate_congestion_score(route_data['congestion_score']),
             "congestion_score must be float 0.0-1.0"),
            (isinstance(route_data['avg_speed_kmh'], (int, float)) and route_data['avg_speed_kmh'] > 0,
             "avg_speed_kmh must be positive number"),
            (isinstance(route_data['travel_time_min'], (int, float)) and route_data['travel_time_min'] > 0,
             "travel_time_min must be positive number"),
            (isinstance(route_data['fuel_consumption_l'], (int, float)) and route_data['fuel_consumption_l'] >= 0,
             "fuel_consumption_l must be non-negative number"),
            (isinstance(route_data['co2_emission_kg'], (int, float)) and route_data['co2_emission_kg'] >= 0,
             "co2_emission_kg must be non-negative number")
        ]
        
        for is_valid, error_msg in validations:
            if not is_valid:
                return False, error_msg
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_location(location: str) -> str:
        """
        Clean and sanitize location string
        
        Args:
            location: Raw location string
            
        Returns:
            str: Sanitized location string
        """
        if not isinstance(location, str):
            return ""
        
        # Remove extra whitespace and capitalize properly
        return location.strip().title()