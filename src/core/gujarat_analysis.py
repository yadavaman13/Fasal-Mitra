"""
Gujarat-Specific Agricultural Analysis
Integrates Gujarat Foodgrains and Oilseeds data with existing system
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class GujaratDataLoader:
    """Load and process Gujarat-specific datasets"""
    
    def __init__(self):
        self.foodgrains = None
        self.oilseeds = None
        self.combined_gujarat = None
        
    def load_gujarat_data(self):
        """Load Gujarat-specific datasets"""
        print("📂 Loading Gujarat-specific datasets...")
        
        # Load foodgrains data
        self.foodgrains = pd.read_csv('data/gujarat/Foodgrains1.csv')
        print(f"✅ Loaded Gujarat Foodgrains: {len(self.foodgrains)} records")
        
        # Load oilseeds data
        self.oilseeds = pd.read_csv('data/gujarat/oilseeds1.csv')
        print(f"✅ Loaded Gujarat Oilseeds: {len(self.oilseeds)} records")
        
        # Clean and standardize data
        self._clean_data()
        
        # Combine datasets
        self._combine_datasets()
        
        return self.combined_gujarat
    
    def _clean_data(self):
        """Clean and standardize column names"""
        # Clean foodgrains
        self.foodgrains.columns = self.foodgrains.columns.str.strip()
        self.foodgrains['Crop'] = self.foodgrains['Crop'].str.strip()
        
        # Remove summary rows
        self.foodgrains = self.foodgrains[~self.foodgrains['Crop'].str.contains('Total', na=False)]
        self.foodgrains = self.foodgrains.dropna(subset=['Sr. No.'])
        
        # Clean oilseeds
        self.oilseeds.columns = self.oilseeds.columns.str.strip()
        self.oilseeds['Crops'] = self.oilseeds['Crops'].str.strip()
        self.oilseeds = self.oilseeds[~self.oilseeds['Crops'].str.contains('Total', na=False)]
        self.oilseeds = self.oilseeds.dropna(subset=['Sr. No.'])
        
        # Rename for consistency
        self.oilseeds.rename(columns={'Crops': 'Crop'}, inplace=True)
        
    def _combine_datasets(self):
        """Combine foodgrains and oilseeds into single Gujarat dataset"""
        # Add crop category
        self.foodgrains['Category'] = self.foodgrains['Crop'].apply(self._categorize_foodgrain)
        self.oilseeds['Category'] = 'Oilseeds'
        
        # Combine
        self.combined_gujarat = pd.concat([self.foodgrains, self.oilseeds], ignore_index=True)
        
        # Add state column
        self.combined_gujarat['State'] = 'Gujarat'
        
        # Standardize column names to match main dataset
        self.combined_gujarat.rename(columns={
            'Area': 'area_gujarat',
            'Production': 'production_gujarat', 
            'Yield': 'yield_gujarat'
        }, inplace=True)
        
        print(f"✅ Combined Gujarat dataset: {len(self.combined_gujarat)} crops")
        
    def _categorize_foodgrain(self, crop):
        """Categorize foodgrain crops"""
        cereals = ['Rice', 'Wheat', 'Jowar', 'Bajra', 'Maize', 'Ragi', 'Small Millets']
        pulses = ['Tur (Red Gram)', 'Udad', 'Mung (Green Gram)', 'Math', 'Gram', 'Other Pulses']
        
        if crop in cereals:
            return 'Cereals'
        elif crop in pulses:
            return 'Pulses'
        else:
            return 'Other Foodgrains'
    
    def get_crop_stats(self, crop_name):
        """Get statistics for a specific crop in Gujarat"""
        crop_data = self.combined_gujarat[self.combined_gujarat['Crop'] == crop_name]
        
        if crop_data.empty:
            return None
        
        return {
            'crop': crop_name,
            'state': 'Gujarat',
            'area': float(crop_data['area_gujarat'].values[0]),
            'production': float(crop_data['production_gujarat'].values[0]),
            'yield': float(crop_data['yield_gujarat'].values[0]),
            'category': crop_data['Category'].values[0]
        }
    
    def get_all_crops(self):
        """Get list of all crops available in Gujarat data"""
        return sorted(self.combined_gujarat['Crop'].unique().tolist())
    
    def get_category_summary(self):
        """Get summary statistics by crop category"""
        summary = self.combined_gujarat.groupby('Category').agg({
            'area_gujarat': 'sum',
            'production_gujarat': 'sum',
            'yield_gujarat': 'mean'
        }).round(2)
        
        summary['crop_count'] = self.combined_gujarat.groupby('Category').size()
        
        return summary


class GujaratEnhancedPredictor:
    """Enhanced predictor with Gujarat-specific data integration"""
    
    def __init__(self, main_data_loader, gujarat_loader):
        self.main_data = main_data_loader
        self.gujarat_data = gujarat_loader
        self.model = None
        self.label_encoders = {}
        
    def prepare_gujarat_enhanced_dataset(self):
        """Merge main dataset with Gujarat-specific data"""
        print("\n🔄 Preparing Gujarat-enhanced dataset...")
        
        # Get main data for Gujarat
        gujarat_main = self.main_data.merged_data[
            self.main_data.merged_data['state'] == 'Gujarat'
        ].copy()
        
        print(f"Main dataset - Gujarat records: {len(gujarat_main)}")
        
        # Standardize crop names for merging
        gujarat_main['crop_clean'] = gujarat_main['crop'].str.strip().str.title()
        self.gujarat_data.combined_gujarat['crop_clean'] = (
            self.gujarat_data.combined_gujarat['Crop'].str.strip().str.title()
        )
        
        # Merge datasets
        enhanced = gujarat_main.merge(
            self.gujarat_data.combined_gujarat[['crop_clean', 'yield_gujarat', 'Category']],
            on='crop_clean',
            how='left'
        )
        
        print(f"✅ Enhanced dataset created: {len(enhanced)} records")
        print(f"   Records with Gujarat-specific data: {enhanced['yield_gujarat'].notna().sum()}")
        
        return enhanced
    
    def train_gujarat_specific_model(self):
        """Train model specifically optimized for Gujarat"""
        print("\n🧠 Training Gujarat-specific ML model...")
        
        enhanced_data = self.prepare_gujarat_enhanced_dataset()
        
        # Features for prediction
        categorical_features = ['crop', 'season']
        numerical_features = ['area', 'fertilizer', 'pesticide', 
                             'avg_temp_c', 'total_rainfall_mm', 'avg_humidity_percent',
                             'N', 'P', 'K', 'pH']
        
        # Add Gujarat-specific yield as feature if available
        enhanced_data['has_gujarat_data'] = enhanced_data['yield_gujarat'].notna().astype(int)
        numerical_features.append('has_gujarat_data')
        
        all_features = categorical_features + numerical_features
        
        # Prepare data
        X = enhanced_data[all_features].copy()
        y = enhanced_data['yield'].values
        
        # Encode categorical variables
        for col in categorical_features:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=200,  # More trees for Gujarat-specific model
            max_depth=20,
            min_samples_split=3,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X, y)
        
        # Calculate accuracy
        score = self.model.score(X, y)
        print(f"✅ Gujarat-specific model trained!")
        print(f"   Model R² score: {score:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': all_features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📊 Top 5 Important Features for Gujarat:")
        for idx, row in feature_importance.head(5).iterrows():
            print(f"   {row['feature']}: {row['importance']:.4f}")
        
        return score
    
    def predict_with_gujarat_context(self, crop, season, fertilizer, area=1.0):
        """Make prediction with Gujarat-specific context"""
        
        if self.model is None:
            raise Exception("Model not trained. Call train_gujarat_specific_model() first.")
        
        # Get Gujarat-specific data for this crop
        gujarat_stats = self.gujarat_data.get_crop_stats(crop)
        
        # Get average weather and soil for Gujarat
        gujarat_avg = self.main_data.merged_data[
            self.main_data.merged_data['state'] == 'Gujarat'
        ].mean()
        
        # Prepare input
        input_data = pd.DataFrame([{
            'crop': crop,
            'season': season,
            'area': area,
            'fertilizer': fertilizer,
            'pesticide': gujarat_avg['pesticide'],
            'avg_temp_c': gujarat_avg['avg_temp_c'],
            'total_rainfall_mm': gujarat_avg['total_rainfall_mm'],
            'avg_humidity_percent': gujarat_avg['avg_humidity_percent'],
            'N': gujarat_avg['N'],
            'P': gujarat_avg['P'],
            'K': gujarat_avg['K'],
            'pH': gujarat_avg['pH'],
            'has_gujarat_data': 1 if gujarat_stats else 0
        }])
        
        # Encode categorical variables
        for col in ['crop', 'season']:
            if col in self.label_encoders:
                try:
                    input_data[col] = self.label_encoders[col].transform([input_data[col].values[0]])
                except:
                    # If crop not in training data, use most similar
                    input_data[col] = 0
        
        # Predict
        prediction = self.model.predict(input_data)[0]
        
        result = {
            'predicted_yield': round(prediction, 2),
            'crop': crop,
            'season': season,
            'fertilizer': fertilizer,
            'area': area,
            'has_gujarat_specific_data': gujarat_stats is not None
        }
        
        # Add Gujarat benchmark if available
        if gujarat_stats:
            result['gujarat_benchmark'] = gujarat_stats['yield']
            result['vs_gujarat_average'] = round(prediction - gujarat_stats['yield'], 2)
        
        return result


class GujaratAnalyzer:
    """Comprehensive analysis for Gujarat agriculture"""
    
    def __init__(self, gujarat_loader, main_data_loader):
        self.gujarat_data = gujarat_loader
        self.main_data = main_data_loader
        
    def compare_with_national_average(self, crop):
        """Compare Gujarat performance with national average"""
        
        # Gujarat data
        gujarat_stats = self.gujarat_data.get_crop_stats(crop)
        if not gujarat_stats:
            return {'error': f'No Gujarat data for {crop}'}
        
        # National data
        national_data = self.main_data.merged_data[
            self.main_data.merged_data['crop'].str.strip().str.title() == crop.title()
        ]
        
        if national_data.empty:
            return {'error': f'No national data for {crop}'}
        
        national_avg = national_data['yield'].mean()
        national_max = national_data['yield'].max()
        
        comparison = {
            'crop': crop,
            'gujarat_yield': gujarat_stats['yield'],
            'national_average': round(national_avg, 2),
            'national_max': round(national_max, 2),
            'gujarat_vs_national': round(gujarat_stats['yield'] - national_avg, 2),
            'performance_percentile': self._calculate_percentile(
                gujarat_stats['yield'], national_data['yield'].values
            ),
            'recommendation': self._generate_recommendation(
                gujarat_stats['yield'], national_avg, national_max
            )
        }
        
        return comparison
    
    def _calculate_percentile(self, value, distribution):
        """Calculate percentile rank"""
        return round((distribution < value).sum() / len(distribution) * 100, 1)
    
    def _generate_recommendation(self, gujarat_yield, national_avg, national_max):
        """Generate recommendation based on comparison"""
        if gujarat_yield >= national_avg * 1.2:
            return "🏆 Excellent! Gujarat is performing significantly above national average"
        elif gujarat_yield >= national_avg:
            return "✅ Good! Gujarat is above national average"
        elif gujarat_yield >= national_avg * 0.8:
            return "⚠️ Fair - Gujarat is slightly below national average. Focus on improvement"
        else:
            return "🔴 Below average - Significant improvement needed. Study best practices"
    
    def get_top_performing_crops(self, top_n=5):
        """Get top performing crops in Gujarat by yield"""
        top_crops = self.gujarat_data.combined_gujarat.nlargest(top_n, 'yield_gujarat')
        
        return top_crops[['Crop', 'yield_gujarat', 'Category']].to_dict('records')
    
    def get_improvement_opportunities(self):
        """Identify crops with improvement potential"""
        opportunities = []
        
        for crop in self.gujarat_data.get_all_crops():
            comparison = self.compare_with_national_average(crop)
            
            if 'error' not in comparison:
                if comparison['gujarat_vs_national'] < 0:
                    gap = abs(comparison['gujarat_vs_national'])
                    opportunities.append({
                        'crop': crop,
                        'yield_gap': gap,
                        'improvement_potential': round((gap / comparison['gujarat_yield']) * 100, 1),
                        'national_average': comparison['national_average']
                    })
        
        return sorted(opportunities, key=lambda x: x['improvement_potential'], reverse=True)


def initialize_gujarat_system():
    """Initialize complete Gujarat-enhanced system"""
    print("="*60)
    print("🌾 INITIALIZING GUJARAT-ENHANCED FARMING SYSTEM 🌾")
    print("="*60)
    
    # Load main data
    from src.core.farming_system import DataLoader as MainDataLoader
    main_loader = MainDataLoader()
    main_loader.load_all()
    main_loader.merge_datasets()
    
    # Load Gujarat data
    gujarat_loader = GujaratDataLoader()
    gujarat_loader.load_gujarat_data()
    
    # Initialize enhanced predictor
    predictor = GujaratEnhancedPredictor(main_loader, gujarat_loader)
    predictor.train_gujarat_specific_model()
    
    # Initialize analyzer
    analyzer = GujaratAnalyzer(gujarat_loader, main_loader)
    
    print("\n" + "="*60)
    print("✅ SYSTEM READY!")
    print("="*60)
    
    return {
        'main_data': main_loader,
        'gujarat_data': gujarat_loader,
        'predictor': predictor,
        'analyzer': analyzer
    }


if __name__ == "__main__":
    # Initialize system
    system = initialize_gujarat_system()
    
    # Display Gujarat crop summary
    print("\n📊 GUJARAT CROP CATEGORY SUMMARY:")
    print("="*60)
    summary = system['gujarat_data'].get_category_summary()
    print(summary)
    
    # Display top performing crops
    print("\n🏆 TOP 5 PERFORMING CROPS IN GUJARAT:")
    print("="*60)
    top_crops = system['analyzer'].get_top_performing_crops(5)
    for i, crop in enumerate(top_crops, 1):
        print(f"{i}. {crop['Crop']:20s} - Yield: {crop['yield_gujarat']:.2f} quintal/ha ({crop['Category']})")
    
    # Display improvement opportunities
    print("\n🎯 IMPROVEMENT OPPORTUNITIES:")
    print("="*60)
    opportunities = system['analyzer'].get_improvement_opportunities()[:5]
    for opp in opportunities:
        print(f"• {opp['crop']:20s} - Gap: {opp['yield_gap']:.2f} quintal/ha ({opp['improvement_potential']:.1f}% potential)")
    
    # Example prediction
    print("\n🔮 EXAMPLE: Gujarat Wheat Prediction")
    print("="*60)
    wheat_prediction = system['predictor'].predict_with_gujarat_context(
        crop='Wheat',
        season='Rabi',
        fertilizer=30000,
        area=1.0
    )
    print(f"Predicted Yield: {wheat_prediction['predicted_yield']:.2f} quintal/ha")
    if 'gujarat_benchmark' in wheat_prediction:
        print(f"Gujarat Benchmark: {wheat_prediction['gujarat_benchmark']:.2f} quintal/ha")
        print(f"Difference: {wheat_prediction['vs_gujarat_average']:+.2f} quintal/ha")
