# Traffic congestion prediction model

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from typing import Dict, Tuple, Optional
import joblib
import os

from utils.config import Config

class TrafficPredictor:
    """
    Machine learning model for predicting traffic congestion
    """
    
    def __init__(self):
        """Initialize the traffic predictor"""
        self.model = None
        self.label_encoders = {}
        self.feature_columns = None
        self.is_trained = False
        
        # Model configuration
        self.model_params = Config.TRAFFIC_PREDICTION_MODEL
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for machine learning
        
        Args:
            df: Raw traffic dataset
            
        Returns:
            pd.DataFrame: Processed features
        """
        # Create a copy to avoid modifying original data
        data = df.copy()
        
        # Encode categorical variables
        categorical_columns = ['source', 'destination', 'traffic_level']
        
        for col in categorical_columns:
            if col in data.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    data[f'{col}_encoded'] = self.label_encoders[col].fit_transform(data[col])
                else:
                    # Handle unseen categories during prediction
                    unique_values = set(data[col].unique())
                    known_values = set(self.label_encoders[col].classes_)
                    new_values = unique_values - known_values
                    
                    if new_values:
                        # Add new categories to encoder
                        all_values = list(known_values) + list(new_values)
                        self.label_encoders[col].classes_ = np.array(all_values)
                    
                    data[f'{col}_encoded'] = self.label_encoders[col].transform(data[col])
        
        # Create time-based features
        data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
        data['is_rush_hour'] = ((data['hour'].between(7, 9)) | 
                               (data['hour'].between(17, 19))).astype(int)
        
        # Create cyclical features for time
        data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
        data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
        data['day_sin'] = np.sin(2 * np.pi * data['day_of_week'] / 7)
        data['day_cos'] = np.cos(2 * np.pi * data['day_of_week'] / 7)
        
        # Select feature columns
        feature_cols = [
            'distance_km', 'hour', 'day_of_week',
            'source_encoded', 'destination_encoded',
            'is_weekend', 'is_rush_hour',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
        ]
        
        # Filter to only include available columns
        available_cols = [col for col in feature_cols if col in data.columns]
        self.feature_columns = available_cols
        
        return data[available_cols]
    
    def train(self, df: pd.DataFrame, target_column: str = 'congestion_score') -> Dict:
        """
        Train the traffic prediction model
        
        Args:
            df: Training dataset
            target_column: Column to predict
            
        Returns:
            Dict: Training metrics and information
        """
        # Prepare features and target
        X = self.prepare_features(df)
        y = df[target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.model_params['test_size'],
            random_state=self.model_params['random_state']
        )
        
        # Initialize and train model
        self.model = RandomForestRegressor(
            n_estimators=self.model_params['n_estimators'],
            random_state=self.model_params['random_state'],
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        metrics = {
            'train_mse': mean_squared_error(y_train, train_pred),
            'test_mse': mean_squared_error(y_test, test_pred),
            'train_r2': r2_score(y_train, train_pred),
            'test_r2': r2_score(y_test, test_pred),
            'feature_importance': dict(zip(X.columns, self.model.feature_importances_)),
            'n_samples': len(df),
            'n_features': len(self.feature_columns)
        }
        
        return metrics
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict traffic congestion for given routes/times
        
        Args:
            df: Dataset with route and time information
            
        Returns:
            np.ndarray: Predicted congestion scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Prepare features
        X = self.prepare_features(df)
        
        # Make predictions
        predictions = self.model.predict(X)
        
        # Ensure predictions are within valid range [0, 1]
        predictions = np.clip(predictions, 0.0, 1.0)
        
        return predictions
    
    def predict_congestion_level(self, source: str, destination: str, 
                                hour: int, day_of_week: int,
                                distance_km: float = None) -> Dict:
        """
        Predict congestion for a specific route and time
        
        Args:
            source: Source location
            destination: Destination location  
            hour: Hour of day (0-23)
            day_of_week: Day of week (0-6)
            distance_km: Distance in km (estimated if not provided)
            
        Returns:
            Dict: Prediction results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Estimate distance if not provided
        if distance_km is None:
            distance_km = np.random.uniform(5, 30)  # Default reasonable range
        
        # Create input dataframe
        input_data = pd.DataFrame([{
            'source': source,
            'destination': destination,
            'hour': hour,
            'day_of_week': day_of_week,
            'distance_km': distance_km,
            'traffic_level': 'medium'  # Placeholder, will be updated
        }])
        
        # Make prediction
        congestion_score = self.predict(input_data)[0]
        traffic_level = Config.get_traffic_level_from_score(congestion_score)
        
        return {
            'congestion_score': round(congestion_score, 3),
            'traffic_level': traffic_level,
            'source': source,
            'destination': destination,
            'hour': hour,
            'day_of_week': day_of_week,
            'distance_km': distance_km
        }
    
    def get_feature_importance(self) -> Optional[Dict]:
        """
        Get feature importance from trained model
        
        Returns:
            Optional[Dict]: Feature importance scores
        """
        if not self.is_trained or self.model is None:
            return None
        
        return dict(zip(self.feature_columns, self.model.feature_importances_))
    
    def save_model(self, filepath: str = None) -> str:
        """
        Save trained model to file
        
        Args:
            filepath: Path to save model, defaults to models directory
            
        Returns:
            str: Path where model was saved
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        if filepath is None:
            os.makedirs("models", exist_ok=True)
            filepath = "models/traffic_predictor.pkl"
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'model_params': self.model_params
        }
        
        joblib.dump(model_data, filepath)
        return filepath
    
    def load_model(self, filepath: str) -> None:
        """
        Load trained model from file
        
        Args:
            filepath: Path to saved model
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.model_params = model_data['model_params']
        self.is_trained = True