# Route optimization and alternative route finding

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from geopy.distance import geodesic
import random

from utils.config import Config

class RouteOptimizer:
    """
    Find optimal routes and suggest alternatives based on traffic conditions
    """
    
    def __init__(self, traffic_data: pd.DataFrame = None):
        """
        Initialize route optimizer
        
        Args:
            traffic_data: Historical traffic data for optimization
        """
        self.traffic_data = traffic_data
        self.location_coordinates = self._initialize_demo_coordinates()
    
    def _initialize_demo_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """
        Initialize demo coordinates for sample locations
        
        Returns:
            Dict[str, Tuple[float, float]]: Location to (lat, lon) mapping
        """
        # Sample coordinates for demo locations (roughly around a city)
        base_lat, base_lon = 40.7128, -74.0060  # NYC as example
        
        coordinates = {}
        for i, location in enumerate(Config.DEMO_LOCATIONS):
            # Spread locations in a rough grid pattern
            lat_offset = (i % 4 - 1.5) * 0.1  # Vary latitude
            lon_offset = (i // 4 - 1.5) * 0.1  # Vary longitude
            
            coordinates[location] = (
                base_lat + lat_offset,
                base_lon + lon_offset
            )
        
        return coordinates
    
    def calculate_distance(self, source: str, destination: str) -> float:
        """
        Calculate distance between two locations
        
        Args:
            source: Source location name
            destination: Destination location name
            
        Returns:
            float: Distance in kilometers
        """
        if source in self.location_coordinates and destination in self.location_coordinates:
            source_coords = self.location_coordinates[source]
            dest_coords = self.location_coordinates[destination]
            return geodesic(source_coords, dest_coords).kilometers
        else:
            # Fallback: random realistic distance
            return random.uniform(5.0, 40.0)
    
    def find_alternative_routes(self, source: str, destination: str,
                               max_alternatives: int = None) -> List[Dict]:
        """
        Find alternative routes between source and destination
        
        Args:
            source: Source location
            destination: Destination location
            max_alternatives: Maximum number of alternatives to return
            
        Returns:
            List[Dict]: List of alternative route options
        """
        if max_alternatives is None:
            max_alternatives = Config.MAX_ALTERNATIVE_ROUTES
        
        alternatives = []
        
        # Direct route
        direct_distance = self.calculate_distance(source, destination)
        alternatives.append({
            'route_type': 'direct',
            'description': f'{source} → {destination}',
            'waypoints': [source, destination],
            'distance_km': round(direct_distance, 2),
            'route_factor': 1.0
        })
        
        # Alternative routes via intermediate locations
        intermediate_locations = [loc for loc in Config.DEMO_LOCATIONS 
                                if loc not in [source, destination]]
        
        for waypoint in intermediate_locations[:max_alternatives-1]:
            # Calculate distance via waypoint
            dist_to_waypoint = self.calculate_distance(source, waypoint)
            dist_from_waypoint = self.calculate_distance(waypoint, destination)
            total_distance = dist_to_waypoint + dist_from_waypoint
            
            # Skip routes that are too long compared to direct route
            if total_distance <= direct_distance * 1.5:
                alternatives.append({
                    'route_type': 'via_waypoint',
                    'description': f'{source} → {waypoint} → {destination}',
                    'waypoints': [source, waypoint, destination],
                    'distance_km': round(total_distance, 2),
                    'route_factor': total_distance / direct_distance
                })
        
        # Sort by distance and limit results
        alternatives = sorted(alternatives, key=lambda x: x['distance_km'])[:max_alternatives]
        
        return alternatives
    
    def evaluate_route_at_time(self, route: Dict, hour: int, 
                              day_of_week: int,
                              traffic_predictor=None) -> Dict:
        """
        Evaluate a route's performance at a specific time
        
        Args:
            route: Route dictionary from find_alternative_routes
            hour: Hour of day (0-23)
            day_of_week: Day of week (0-6)
            traffic_predictor: Optional traffic prediction model
            
        Returns:
            Dict: Route evaluation results
        """
        source = route['waypoints'][0]
        destination = route['waypoints'][-1]
        distance = route['distance_km']
        
        # Predict congestion if predictor is available
        if traffic_predictor and traffic_predictor.is_trained:
            try:
                prediction = traffic_predictor.predict_congestion_level(
                    source, destination, hour, day_of_week, distance
                )
                congestion_score = prediction['congestion_score']
                traffic_level = prediction['traffic_level']
            except Exception:
                # Fallback to historical data or estimation
                congestion_score = self._estimate_congestion(hour, day_of_week)
                traffic_level = Config.get_traffic_level_from_score(congestion_score)
        else:
            congestion_score = self._estimate_congestion(hour, day_of_week)
            traffic_level = Config.get_traffic_level_from_score(congestion_score)
        
        # Apply route factor (longer routes may have different congestion)
        route_factor = route.get('route_factor', 1.0)
        if route_factor > 1.2:  # Significantly longer route
            congestion_score *= 0.9  # Assume slightly less congested
        
        congestion_score = min(1.0, max(0.0, congestion_score))
        
        # Calculate performance metrics
        base_speed = 50.0  # km/h base speed
        congestion_penalty = congestion_score * 0.7  # Up to 70% speed reduction
        avg_speed = base_speed * (1 - congestion_penalty)
        avg_speed = max(15.0, avg_speed)  # Minimum speed
        
        travel_time = (distance / avg_speed) * 60  # minutes
        fuel_consumption = distance * Config.FUEL_CONSUMPTION_BASE * (1 + congestion_score * 0.3)
        co2_emission = fuel_consumption * Config.CO2_EMISSION_FACTOR
        
        return {
            **route,
            'hour': hour,
            'day_of_week': day_of_week,
            'congestion_score': round(congestion_score, 3),
            'traffic_level': traffic_level,
            'avg_speed_kmh': round(avg_speed, 1),
            'travel_time_min': round(travel_time, 1),
            'fuel_consumption_l': round(fuel_consumption, 3),
            'co2_emission_kg': round(co2_emission, 3)
        }
    
    def _estimate_congestion(self, hour: int, day_of_week: int) -> float:
        """
        Estimate congestion based on time patterns (fallback method)
        
        Args:
            hour: Hour of day (0-23)
            day_of_week: Day of week (0-6)
            
        Returns:
            float: Estimated congestion score
        """
        # Weekend pattern
        if day_of_week in [5, 6]:
            if 10 <= hour <= 20:
                return random.uniform(0.3, 0.5)
            else:
                return random.uniform(0.1, 0.3)
        
        # Weekday pattern
        if 7 <= hour <= 9:  # Morning rush
            return random.uniform(0.7, 0.9)
        elif 17 <= hour <= 19:  # Evening rush
            return random.uniform(0.6, 0.8)
        elif 10 <= hour <= 16:  # Daytime
            return random.uniform(0.4, 0.6)
        elif 20 <= hour <= 22:  # Evening
            return random.uniform(0.3, 0.5)
        else:  # Night/early morning
            return random.uniform(0.1, 0.3)
    
    def optimize_travel_time(self, source: str, destination: str,
                           preferred_hour: int = None,
                           day_of_week: int = None,
                           traffic_predictor=None) -> Dict:
        """
        Find optimal travel time for a route
        
        Args:
            source: Source location
            destination: Destination location
            preferred_hour: Preferred departure hour (optional)
            day_of_week: Day of week (optional)
            traffic_predictor: Traffic prediction model (optional)
            
        Returns:
            Dict: Optimization results with recommendations
        """
        # Use current day/hour if not specified
        if day_of_week is None:
            day_of_week = 1  # Tuesday as default
        
        # Test different hours around preferred time
        test_hours = []
        if preferred_hour is not None:
            # Test 3 hours before and after preferred time
            for offset in range(-3, 4):
                test_hour = (preferred_hour + offset) % 24
                test_hours.append(test_hour)
        else:
            # Test key hours throughout the day
            test_hours = [6, 8, 10, 12, 14, 16, 18, 20]
        
        # Get alternative routes
        routes = self.find_alternative_routes(source, destination)
        
        # Evaluate all route-time combinations
        evaluations = []\n        for route in routes:\n            for hour in test_hours:\n                evaluation = self.evaluate_route_at_time(\n                    route, hour, day_of_week, traffic_predictor\n                )\n                evaluations.append(evaluation)\n        \n        # Find best options based on different criteria\n        best_time = min(evaluations, key=lambda x: x['travel_time_min'])\n        best_fuel = min(evaluations, key=lambda x: x['fuel_consumption_l'])\n        best_co2 = min(evaluations, key=lambda x: x['co2_emission_kg'])\n        \n        # Filter to low-congestion options\n        low_congestion = [e for e in evaluations \n                         if e['congestion_score'] < Config.CONGESTION_THRESHOLD]\n        \n        recommendations = {\n            'source': source,\n            'destination': destination,\n            'preferred_hour': preferred_hour,\n            'day_of_week': day_of_week,\n            'best_time': best_time,\n            'best_fuel_efficiency': best_fuel,\n            'best_environmental': best_co2,\n            'low_congestion_options': low_congestion[:3],  # Top 3\n            'all_evaluations': evaluations\n        }\n        \n        return recommendations\n    \n    def get_route_summary(self, evaluation: Dict) -> str:\n        \"\"\"\n        Generate human-readable route summary\n        \n        Args:\n            evaluation: Route evaluation result\n            \n        Returns:\n            str: Formatted route summary\n        \"\"\"\n        hour_12 = evaluation['hour'] % 12\n        if hour_12 == 0:\n            hour_12 = 12\n        ampm = 'AM' if evaluation['hour'] < 12 else 'PM'\n        \n        return (\n            f\"{evaluation['description']} at {hour_12}:00 {ampm}\\n\"\n            f\"Distance: {evaluation['distance_km']} km\\n\"\n            f\"Travel Time: {evaluation['travel_time_min']} min\\n\"\n            f\"Traffic Level: {evaluation['traffic_level']}\\n\"\n            f\"Fuel: {evaluation['fuel_consumption_l']} L\\n\"\n            f\"CO2: {evaluation['co2_emission_kg']} kg\"\n        )"