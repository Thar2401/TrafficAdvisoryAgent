# Sustainability impact calculator

from typing import Dict, List
import numpy as np

from utils.config import Config

class SustainabilityCalculator:
    """
    Calculate environmental impact and sustainability metrics for routes
    """
    
    def __init__(self):
        """Initialize sustainability calculator"""
        # Emission factors (kg CO2 equivalent per km)
        self.emission_factors = {
            'car_gasoline': 0.180,     # Average car
            'car_diesel': 0.165,       # Diesel car
            'car_electric': 0.050,     # Electric car (grid average)
            'public_transport': 0.040, # Bus/subway average
            'bicycle': 0.000,          # Zero emissions
            'walking': 0.000           # Zero emissions
        }
        
        # Energy consumption factors (kWh per km)
        self.energy_factors = {
            'car_gasoline': 0.65,      # Gasoline energy content
            'car_diesel': 0.60,        # Diesel efficiency
            'car_electric': 0.20,      # Electric efficiency
            'public_transport': 0.15,  # Shared efficiency
            'bicycle': 0.00,
            'walking': 0.00
        }
        
        # Cost factors (currency per km)
        self.cost_factors = {
            'car_gasoline': 0.25,      # Including fuel, maintenance
            'car_diesel': 0.22,        # Slightly more efficient
            'car_electric': 0.15,      # Lower operating costs
            'public_transport': 0.08,  # Subsidized public transport
            'bicycle': 0.02,           # Maintenance only
            'walking': 0.00            # Free!
        }
    
    def calculate_route_impact(self, distance_km: float, 
                             travel_mode: str = 'car_gasoline') -> Dict:
        """
        Calculate environmental impact for a specific route and mode
        
        Args:
            distance_km: Route distance in kilometers
            travel_mode: Mode of transportation
            
        Returns:
            Dict: Impact metrics
        """
        if travel_mode not in self.emission_factors:
            travel_mode = 'car_gasoline'  # Default fallback
        
        co2_emission = distance_km * self.emission_factors[travel_mode]
        energy_consumption = distance_km * self.energy_factors[travel_mode]
        cost = distance_km * self.cost_factors[travel_mode]
        
        return {
            'travel_mode': travel_mode,
            'distance_km': distance_km,
            'co2_emission_kg': round(co2_emission, 3),
            'energy_consumption_kwh': round(energy_consumption, 2),
            'estimated_cost': round(cost, 2),
            'sustainability_score': self._calculate_sustainability_score(travel_mode)
        }
    
    def _calculate_sustainability_score(self, travel_mode: str) -> float:
        """
        Calculate sustainability score (0-100, higher is better)
        
        Args:
            travel_mode: Transportation mode
            
        Returns:
            float: Sustainability score
        """
        # Base scores for different modes
        sustainability_scores = {
            'walking': 100.0,
            'bicycle': 95.0,
            'public_transport': 80.0,
            'car_electric': 70.0,
            'car_diesel': 40.0,
            'car_gasoline': 35.0
        }
        
        return sustainability_scores.get(travel_mode, 35.0)
    
    def compare_transportation_modes(self, distance_km: float) -> List[Dict]:
        """
        Compare environmental impact across different transportation modes
        
        Args:
            distance_km: Route distance in kilometers
            
        Returns:
            List[Dict]: Comparison results sorted by sustainability
        """
        comparisons = []
        
        for mode in self.emission_factors.keys():
            impact = self.calculate_route_impact(distance_km, mode)
            comparisons.append(impact)
        
        # Sort by sustainability score (descending)
        comparisons.sort(key=lambda x: x['sustainability_score'], reverse=True)
        
        return comparisons
    
    def calculate_congestion_impact(self, base_impact: Dict, 
                                   congestion_score: float) -> Dict:
        """
        Adjust environmental impact based on traffic congestion
        
        Args:
            base_impact: Base impact calculation
            congestion_score: Congestion level (0.0-1.0)
            
        Returns:
            Dict: Adjusted impact metrics
        """
        # Congestion increases fuel consumption and emissions
        congestion_multiplier = 1.0 + (congestion_score * 0.4)  # Up to 40% increase
        
        adjusted_impact = base_impact.copy()
        adjusted_impact.update({
            'co2_emission_kg': round(base_impact['co2_emission_kg'] * congestion_multiplier, 3),
            'energy_consumption_kwh': round(base_impact['energy_consumption_kwh'] * congestion_multiplier, 2),
            'estimated_cost': round(base_impact['estimated_cost'] * congestion_multiplier, 2),
            'congestion_penalty': round((congestion_multiplier - 1.0) * 100, 1),  # Percentage increase
            'congestion_score': congestion_score
        })\n        \n        return adjusted_impact\n    \n    def calculate_route_alternatives_sustainability(self, route_evaluations: List[Dict]) -> Dict:\n        \"\"\"\n        Calculate sustainability metrics for route alternatives\n        \n        Args:\n            route_evaluations: List of route evaluation results\n            \n        Returns:\n            Dict: Sustainability comparison and recommendations\n        \"\"\"\n        sustainability_results = []\n        \n        for evaluation in route_evaluations:\n            # Calculate base car impact\n            base_impact = self.calculate_route_impact(\n                evaluation['distance_km'], 'car_gasoline'\n            )\n            \n            # Adjust for congestion\n            congestion_impact = self.calculate_congestion_impact(\n                base_impact, evaluation['congestion_score']\n            )\n            \n            # Add route information\n            sustainability_results.append({\n                **evaluation,\n                **congestion_impact,\n                'base_co2_kg': base_impact['co2_emission_kg'],\n                'congestion_co2_kg': congestion_impact['co2_emission_kg']\n            })\n        \n        # Find best and worst options\n        best_environmental = min(sustainability_results, \n                               key=lambda x: x['co2_emission_kg'])\n        worst_environmental = max(sustainability_results, \n                                key=lambda x: x['co2_emission_kg'])\n        \n        # Calculate potential savings\n        max_co2 = worst_environmental['co2_emission_kg']\n        min_co2 = best_environmental['co2_emission_kg']\n        potential_savings = max_co2 - min_co2\n        \n        return {\n            'route_sustainability': sustainability_results,\n            'best_environmental_option': best_environmental,\n            'worst_environmental_option': worst_environmental,\n            'potential_co2_savings_kg': round(potential_savings, 3),\n            'potential_savings_percentage': round((potential_savings / max_co2) * 100, 1) if max_co2 > 0 else 0\n        }\n    \n    def generate_sustainability_recommendations(self, distance_km: float,\n                                              current_co2_kg: float) -> List[str]:\n        \"\"\"\n        Generate actionable sustainability recommendations\n        \n        Args:\n            distance_km: Route distance\n            current_co2_kg: Current route CO2 emissions\n            \n        Returns:\n            List[str]: List of recommendations\n        \"\"\"\n        recommendations = []\n        \n        # Compare with alternative modes\n        alternatives = self.compare_transportation_modes(distance_km)\n        \n        # Walking/cycling recommendations\n        if distance_km <= 2.0:\n            recommendations.append(\n                f\"✨ Consider walking ({distance_km:.1f} km) - Zero emissions and great exercise!\"\n            )\n        elif distance_km <= 8.0:\n            recommendations.append(\n                f\"🚲 Consider cycling ({distance_km:.1f} km) - Save {current_co2_kg:.2f} kg CO2!\"\n            )\n        \n        # Public transport recommendation\n        if distance_km > 3.0:\n            public_transport_co2 = distance_km * self.emission_factors['public_transport']\n            savings = current_co2_kg - public_transport_co2\n            if savings > 0:\n                recommendations.append(\n                    f\"🚌 Use public transport - Save {savings:.2f} kg CO2 ({savings/current_co2_kg*100:.0f}% reduction)\"\n                )\n        \n        # Electric vehicle recommendation\n        electric_co2 = distance_km * self.emission_factors['car_electric']\n        electric_savings = current_co2_kg - electric_co2\n        if electric_savings > 0:\n            recommendations.append(\n                f\"⚡ Switch to electric vehicle - Save {electric_savings:.2f} kg CO2 annually\"\n            )\n        \n        # Time-shifting recommendation\n        recommendations.append(\n            \"⏰ Travel during off-peak hours to reduce fuel consumption from traffic delays\"\n        )\n        \n        # Carpooling recommendation\n        if distance_km > 5.0:\n            carpool_savings = current_co2_kg * 0.5  # Assume 2-person carpool\n            recommendations.append(\n                f\"👥 Consider carpooling - Share the trip and save {carpool_savings:.2f} kg CO2\"\n            )\n        \n        return recommendations\n    \n    def calculate_annual_impact(self, daily_routes: List[Dict], \n                              days_per_year: int = 250) -> Dict:\n        \"\"\"\n        Calculate annual environmental impact for regular routes\n        \n        Args:\n            daily_routes: List of daily route evaluations\n            days_per_year: Number of travel days per year\n            \n        Returns:\n            Dict: Annual impact projection\n        \"\"\"\n        total_daily_co2 = sum(route['co2_emission_kg'] for route in daily_routes)\n        total_daily_distance = sum(route['distance_km'] for route in daily_routes)\n        total_daily_cost = sum(route.get('estimated_cost', 0) for route in daily_routes)\n        \n        annual_co2 = total_daily_co2 * days_per_year\n        annual_distance = total_daily_distance * days_per_year\n        annual_cost = total_daily_cost * days_per_year\n        \n        # Calculate equivalent metrics\n        trees_to_offset = annual_co2 / 21.8  # Average tree absorbs 21.8 kg CO2/year\n        gasoline_equivalent = annual_co2 / 2.31  # kg CO2 per liter gasoline\n        \n        return {\n            'daily_co2_kg': round(total_daily_co2, 2),\n            'daily_distance_km': round(total_daily_distance, 1),\n            'daily_cost': round(total_daily_cost, 2),\n            'annual_co2_kg': round(annual_co2, 1),\n            'annual_distance_km': round(annual_distance, 1),\n            'annual_cost': round(annual_cost, 2),\n            'trees_needed_to_offset': round(trees_to_offset, 1),\n            'gasoline_equivalent_liters': round(gasoline_equivalent, 1),\n            'days_per_year': days_per_year\n        }"