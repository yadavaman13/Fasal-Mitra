"""
Data Loading and Processing Module

Handles loading and preprocessing of agricultural datasets for the farming advisory system.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

class DataLoader:
    """Centralized data loading and preprocessing for farming advisory system."""
    
    def __init__(self, data_dir=".."):  # Look in parent directory by default
        self.data_dir = Path(__file__).parent.parent.parent / data_dir if data_dir == ".." else Path(data_dir)
        self.crop_data = None
        self.soil_data = None
        self.weather_data = None
        self.merged_data = None
        
    def load_datasets(self):
        """Load all three core datasets."""
        print("Loading agricultural datasets...")
        
        # Load crop yield data
        crop_file = self.data_dir / "data/raw/crop_yield.csv"
        if crop_file.exists():
            self.crop_data = pd.read_csv(crop_file)
            print(f"✅ Loaded crop data: {len(self.crop_data):,} records")
        else:
            raise FileNotFoundError(f"Crop yield data not found: {crop_file}")
            
        # Load soil data
        soil_file = self.data_dir / "data/raw/state_soil_data.csv"
        if soil_file.exists():
            self.soil_data = pd.read_csv(soil_file)
            print(f"✅ Loaded soil data: {len(self.soil_data):,} records")
        else:
            raise FileNotFoundError(f"Soil data not found: {soil_file}")
            
        # Load weather data
        weather_file = self.data_dir / "data/raw/state_weather_data_1997_2020.csv"
        if weather_file.exists():
            self.weather_data = pd.read_csv(weather_file)
            print(f"✅ Loaded weather data: {len(self.weather_data):,} records")
        else:
            raise FileNotFoundError(f"Weather data not found: {weather_file}")
    
    def merge_datasets(self):
        """Merge all datasets into one master dataset for ML."""
        if not all([self.crop_data is not None, self.soil_data is not None, self.weather_data is not None]):
            self.load_datasets()
            
        print("Merging datasets...")
        
        # Merge crop with weather (on state + year)
        merged = self.crop_data.merge(
            self.weather_data, 
            on=['state', 'year'], 
            how='left'
        )
        
        # Merge with soil (on state only - soil data is constant across years)
        merged = merged.merge(
            self.soil_data, 
            on='state', 
            how='left'
        )
        
        self.merged_data = merged
        print(f"✅ Merged dataset: {len(merged):,} records")
        
        # Check for missing values
        missing = merged.isna().sum().sum()
        if missing > 0:
            print(f"⚠️ Warning: {missing} missing values detected")
        else:
            print("✅ No missing values - perfect merge!")
            
        return merged
    
    def get_crop_list(self):
        """Get list of all available crops."""
        if self.crop_data is None:
            self.load_datasets()
        return sorted(self.crop_data['crop'].unique())
    
    def get_state_list(self):
        """Get list of all available states."""
        if self.crop_data is None:
            self.load_datasets()
        return sorted(self.crop_data['state'].unique())
    
    def get_season_list(self):
        """Get list of all available seasons."""
        if self.crop_data is None:
            self.load_datasets()
        return sorted(self.crop_data['season'].str.strip().unique())
    
    def get_data_summary(self):
        """Get summary statistics of the dataset."""
        if self.merged_data is None:
            self.merge_datasets()
            
        return {
            'total_records': len(self.merged_data),
            'crops': self.merged_data['crop'].nunique(),
            'states': self.merged_data['state'].nunique(),
            'years': f"{self.merged_data['year'].min()}-{self.merged_data['year'].max()}",
            'seasons': self.merged_data['season'].nunique(),
            'avg_yield': round(self.merged_data['yield'].mean(), 2),
            'yield_range': f"{self.merged_data['yield'].min():.1f}-{self.merged_data['yield'].max():.1f}"
        }
    
    def filter_data(self, crop=None, state=None, season=None, years=None):
        """Filter merged dataset based on criteria."""
        if self.merged_data is None:
            self.merge_datasets()
            
        data = self.merged_data.copy()
        
        if crop:
            data = data[data['crop'] == crop]
        if state:
            data = data[data['state'] == state]
        if season:
            data = data[data['season'].str.strip() == season.strip()]
        if years:
            if isinstance(years, (list, tuple)):
                data = data[data['year'].between(years[0], years[1])]
            else:
                data = data[data['year'] == years]
                
        return data

# Global instance
data_loader = DataLoader()