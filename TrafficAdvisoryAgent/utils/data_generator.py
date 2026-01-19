# Simulated traffic data generation for Traffic Advisory Agent

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import List, Dict
import os

from .config import Config

class TrafficDataGenerator:
    """
    Generate simulated traffic data for testing and development
    """
    
    def __init__(self, locations: List[str] = None):
        """
        Initialize data generator
        
        Args:
            locations: List of location names, defaults to Config.DEMO_LOCATIONS
        """
        self.locations = locations or Config.DEMO_LOCATIONS
        self.random_seed = Config.TRAFFIC_PREDICTION_MODEL['random_state']
        
        # Set random seeds for reproducibility
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
    
    def generate_routes(self, num_routes: int = 100) -> List[Dict]:
        """
        Generate route combinations between locations
        
        Args:
            num_routes: Number of unique routes to generate
            
        Returns:
            List[Dict]: List of route dictionaries
        """
        routes = []
        route_id = 0
        
        # Generate all possible combinations, then sample randomly
        possible_routes = []
        for source in self.locations:
            for destination in self.locations:
                if source != destination:
                    possible_routes.append((source, destination))
        
        # Sample routes (with replacement if needed)
        selected_routes = random.choices(possible_routes, k=num_routes)
        
        for source, destination in selected_routes:
            # Calculate realistic distance (5-50 km)
            base_distance = random.uniform(5, 50)
            
            route = {
                'route_id': f'R{route_id:04d}',
                'source': source,
                'destination': destination,
                'distance_km': round(base_distance, 2)
            }
            
            routes.append(route)
            route_id += 1
        
        return routes
    
    def generate_traffic_patterns(self, routes: List[Dict], 
                                 days: int = 30) -> pd.DataFrame:
        """
        Generate traffic patterns for routes over specified time period
        
        Args:
            routes: List of route dictionaries
            days: Number of days to generate data for
            
        Returns:
            pd.DataFrame: Complete traffic dataset
        """
        data_records = []
        
        for day in range(days):
            day_of_week = day % 7
            
            for hour in range(24):
                for route in routes:
                    # Generate traffic data for this route at this time
                    traffic_data = self._generate_hourly_traffic(
                        route, hour, day_of_week
                    )
                    
                    data_records.append(traffic_data)
        
        return pd.DataFrame(data_records)
    
    def _generate_hourly_traffic(self, route: Dict, hour: int, 
                               day_of_week: int) -> Dict:
        """
        Generate traffic data for a specific route at a specific time
        
        Args:
            route: Route dictionary
            hour: Hour of day (0-23)
            day_of_week: Day of week (0=Monday, 6=Sunday)
            
        Returns:
            Dict: Complete traffic data record
        """
        # Base congestion patterns
        congestion_score = self._calculate_congestion_score(hour, day_of_week)
        
        # Add route-specific variation
        route_factor = self._get_route_factor(route['source'], route['destination'])
        congestion_score *= route_factor
        congestion_score = min(1.0, max(0.0, congestion_score))
        
        # Calculate dependent metrics
        traffic_level = Config.get_traffic_level_from_score(congestion_score)
        avg_speed = self._calculate_speed(congestion_score)
        travel_time = (route['distance_km'] / avg_speed) * 60  # minutes
        fuel_consumption = self._calculate_fuel_consumption(
            route['distance_km'], avg_speed
        )
        co2_emission = fuel_consumption * Config.CO2_EMISSION_FACTOR
        
        return {
            'route_id': route['route_id'],
            'source': route['source'],
            'destination': route['destination'],
            'distance_km': route['distance_km'],
            'hour': hour,
            'day_of_week': day_of_week,
            'traffic_level': traffic_level,
            'congestion_score': round(congestion_score, 3),
            'avg_speed_kmh': round(avg_speed, 1),
            'travel_time_min': round(travel_time, 1),
            'fuel_consumption_l': round(fuel_consumption, 3),
            'co2_emission_kg': round(co2_emission, 3)
        }
    
    def _calculate_congestion_score(self, hour: int, day_of_week: int) -> float:
        """
        Calculate base congestion score based on time patterns
        
        Args:
            hour: Hour of day (0-23)
            day_of_week: Day of week (0=Monday, 6=Sunday)
            
        Returns:
            float: Base congestion score (0.0-1.0)
        """
        # Weekend pattern (lower congestion)
        if day_of_week in [5, 6]:  # Saturday, Sunday
            if 10 <= hour <= 20:  # Moderate activity during day
                return random.uniform(0.3, 0.6)
            else:
                return random.uniform(0.1, 0.3)
        
        # Weekday pattern
        if 7 <= hour <= 9:  # Morning rush
            return random.uniform(0.7, 1.0)
        elif 17 <= hour <= 19:  # Evening rush
            return random.uniform(0.6, 0.9)
        elif 10 <= hour <= 16:  # Daytime moderate
            return random.uniform(0.4, 0.7)
        elif 20 <= hour <= 22:  # Evening moderate
            return random.uniform(0.3, 0.6)
        else:  # Night/early morning
            return random.uniform(0.1, 0.3)
    
    def _get_route_factor(self, source: str, destination: str) -> float:
        """
        Get route-specific congestion factor based on location types
        
        Args:
            source: Source location
            destination: Destination location
            
        Returns:
            float: Route factor multiplier
        """
        # Define high-traffic locations
        high_traffic_locations = [
            'Downtown', 'Airport', 'Business District', 
            'Shopping Mall', 'Train Station'
        ]
        
        factor = 1.0
        
        # Increase factor if either location is high-traffic
        if source in high_traffic_locations:
            factor *= 1.2
        if destination in high_traffic_locations:
            factor *= 1.2
        
        # Add random variation
        factor *= random.uniform(0.8, 1.2)
        
        return factor
    
    def _calculate_speed(self, congestion_score: float) -> float:
        """
        Calculate average speed based on congestion
        
        Args:
            congestion_score: Congestion level (0.0-1.0)
            
        Returns:
            float: Average speed in km/h
        """
        # Speed decreases with congestion
        # Free flow: ~60 km/h, Heavy congestion: ~15 km/h
        max_speed = 60.0
        min_speed = 15.0
        
        speed = max_speed - (congestion_score * (max_speed - min_speed))
        
        # Add some random variation
        speed *= random.uniform(0.9, 1.1)
        
        return max(min_speed, min(max_speed, speed))
    
    def _calculate_fuel_consumption(self, distance_km: float, 
                                  avg_speed_kmh: float) -> float:
        """
        Calculate fuel consumption based on distance and speed
        
        Args:
            distance_km: Route distance in kilometers
            avg_speed_kmh: Average speed in km/h
            
        Returns:
            float: Fuel consumption in liters
        """
        # Base consumption increases at very low and very high speeds
        base_consumption = Config.FUEL_CONSUMPTION_BASE
        
        # Optimal speed around 50 km/h
        if avg_speed_kmh < 30:
            factor = 1.3  # Stop-and-go traffic
        elif avg_speed_kmh > 80:
            factor = 1.2  # High-speed consumption
        else:
            factor = 1.0
        
        return distance_km * base_consumption * factor
    
    def save_dataset(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save generated dataset to file
        
        Args:
            df: DataFrame to save
            filename: Optional filename, defaults to timestamped name
            
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"traffic_data_{timestamp}.csv"
        
        # Ensure data directory exists
        os.makedirs(Config.SIMULATED_DATA_DIR, exist_ok=True)
        
        filepath = os.path.join(Config.SIMULATED_DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        
        return filepath
    
    def generate_complete_dataset(self, num_routes: int = 50, 
                                days: int = 30) -> pd.DataFrame:
        """
        Generate complete traffic dataset
        
        Args:
            num_routes: Number of unique routes
            days: Number of days of data
            
        Returns:
            pd.DataFrame: Complete traffic dataset
        """
        print(f"Generating {num_routes} routes...")
        routes = self.generate_routes(num_routes)
        
        print(f"Generating traffic patterns for {days} days...")
        dataset = self.generate_traffic_patterns(routes, days)
        
        print(f"Generated {len(dataset)} traffic records")
        return dataset