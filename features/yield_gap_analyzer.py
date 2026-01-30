"""
Yield Gap Analysis Feature

Compares user's potential yield with top performers in their region and identifies improvement opportunities.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
# import matplotlib.pyplot as plt
# import seaborn as sns
from pathlib import Path

class YieldGapAnalyzer:
    """Analyzes yield gaps and benchmarks against top performers."""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        
    def calculate_yield_benchmarks(self, crop: str, state: str, season: str = None) -> Dict:
        """Calculate yield benchmarks for a specific crop-state combination."""
        
        # Filter data
        data = self.data_loader.filter_data(crop=crop, state=state, season=season)
        
        if data.empty:
            return {
                'error': f'No data available for {crop} in {state}' + (f' during {season}' if season else ''),
                'available_seasons': self.data_loader.filter_data(crop=crop, state=state)['season'].str.strip().unique().tolist()
            }
        
        yields = data['yield'].values
        
        # Calculate benchmarks
        benchmarks = {
            'total_records': len(data),
            'years_covered': f"{data['year'].min()}-{data['year'].max()}",
            'average_yield': round(np.mean(yields), 2),
            'median_yield': round(np.median(yields), 2),
            'top_10_percent': round(np.percentile(yields, 90), 2),
            'top_25_percent': round(np.percentile(yields, 75), 2),
            'bottom_25_percent': round(np.percentile(yields, 25), 2),
            'max_yield_achieved': round(np.max(yields), 2),
            'min_yield_recorded': round(np.min(yields), 2),
            'yield_std': round(np.std(yields), 2),
            'consistent_high_performers': self._find_consistent_performers(data, percentile=80),
            'improvement_factors': self._analyze_improvement_factors(data)
        }
        
        return benchmarks
    
    def analyze_user_gap(self, user_yield: float, crop: str, state: str, season: str = None) -> Dict:
        """Analyze the gap between user's yield and benchmarks."""
        
        benchmarks = self.calculate_yield_benchmarks(crop, state, season)
        
        if 'error' in benchmarks:
            return benchmarks
            
        # Calculate gaps and potential
        gap_analysis = {
            'user_yield': user_yield,
            'benchmarks': benchmarks,
            'gaps': {
                'vs_average': round(benchmarks['average_yield'] - user_yield, 2),
                'vs_top_25': round(benchmarks['top_25_percent'] - user_yield, 2),
                'vs_top_10': round(benchmarks['top_10_percent'] - user_yield, 2),
                'vs_maximum': round(benchmarks['max_yield_achieved'] - user_yield, 2)
            },
            'percentile_rank': self._calculate_percentile_rank(user_yield, crop, state, season),
            'improvement_potential': self._calculate_improvement_potential(user_yield, benchmarks),
            'recommendations': self._generate_recommendations(user_yield, benchmarks, crop, state, season)
        }
        
        return gap_analysis
    
    def _find_consistent_performers(self, data: pd.DataFrame, percentile: float = 80) -> Dict:
        """Find fields/years that consistently perform in top percentile."""
        
        threshold = np.percentile(data['yield'], percentile)
        high_performers = data[data['yield'] >= threshold]
        
        return {
            'count': len(high_performers),
            'percentage': round(len(high_performers) / len(data) * 100, 1),
            'avg_yield': round(high_performers['yield'].mean(), 2),
            'characteristics': self._analyze_high_performer_characteristics(high_performers)
        }
    
    def _analyze_high_performer_characteristics(self, high_performers: pd.DataFrame) -> Dict:
        """Analyze common characteristics of high-performing records."""
        
        characteristics = {}
        
        # Fertilizer usage
        characteristics['avg_fertilizer'] = round(high_performers['fertilizer'].mean(), 0)
        characteristics['fertilizer_range'] = f"{high_performers['fertilizer'].quantile(0.25):.0f}-{high_performers['fertilizer'].quantile(0.75):.0f}"
        
        # Weather conditions
        if 'avg_temp_c' in high_performers.columns:
            characteristics['optimal_temp'] = round(high_performers['avg_temp_c'].mean(), 1)
            characteristics['optimal_rainfall'] = round(high_performers['total_rainfall_mm'].mean(), 0)
            characteristics['optimal_humidity'] = round(high_performers['avg_humidity_percent'].mean(), 1)
        
        # Soil conditions
        if 'pH' in high_performers.columns:
            characteristics['optimal_pH'] = round(high_performers['pH'].mean(), 1)
            characteristics['optimal_N'] = round(high_performers['N'].mean(), 0)
            characteristics['optimal_P'] = round(high_performers['P'].mean(), 0)
            characteristics['optimal_K'] = round(high_performers['K'].mean(), 0)
        
        return characteristics
    
    def _analyze_improvement_factors(self, data: pd.DataFrame) -> Dict:
        """Analyze factors that contribute to higher yields."""
        
        # Correlation analysis
        numeric_columns = ['fertilizer', 'pesticide', 'area']
        if 'avg_temp_c' in data.columns:
            numeric_columns.extend(['avg_temp_c', 'total_rainfall_mm', 'avg_humidity_percent'])
        if 'pH' in data.columns:
            numeric_columns.extend(['N', 'P', 'K', 'pH'])
            
        correlations = data[numeric_columns + ['yield']].corr()['yield'].drop('yield')
        
        # Top positive and negative correlations
        positive_factors = correlations[correlations > 0].sort_values(ascending=False)
        negative_factors = correlations[correlations < 0].sort_values()
        
        return {
            'top_positive_factors': positive_factors.head(3).to_dict(),
            'top_negative_factors': negative_factors.head(3).to_dict(),
            'key_insights': self._generate_factor_insights(positive_factors, negative_factors)
        }
    
    def _generate_factor_insights(self, positive_factors: pd.Series, negative_factors: pd.Series) -> List[str]:
        """Generate human-readable insights about improvement factors."""
        
        insights = []
        
        # Top positive factor
        if len(positive_factors) > 0:
            top_factor = positive_factors.index[0]
            correlation = positive_factors.iloc[0]
            insights.append(f"Increase {top_factor} for better yields (correlation: {correlation:.2f})")
        
        # Top negative factor (if significant)
        if len(negative_factors) > 0 and abs(negative_factors.iloc[0]) > 0.1:
            worst_factor = negative_factors.index[0]
            correlation = negative_factors.iloc[0]
            insights.append(f"Monitor {worst_factor} levels (negative impact: {correlation:.2f})")
        
        return insights
    
    def _calculate_percentile_rank(self, user_yield: float, crop: str, state: str, season: str = None) -> float:
        """Calculate where user's yield ranks among all records."""
        
        data = self.data_loader.filter_data(crop=crop, state=state, season=season)
        if data.empty:
            return 0.0
            
        rank = (data['yield'] < user_yield).mean() * 100
        return round(rank, 1)
    
    def _calculate_improvement_potential(self, user_yield: float, benchmarks: Dict) -> Dict:
        """Calculate realistic improvement potential and ROI estimates."""
        
        # Conservative, moderate, and aggressive improvement scenarios
        potential = {
            'conservative': {
                'target_yield': benchmarks['top_25_percent'],
                'improvement': round(benchmarks['top_25_percent'] - user_yield, 2),
                'improvement_percent': round((benchmarks['top_25_percent'] - user_yield) / user_yield * 100, 1) if user_yield > 0 else 0,
                'achievability': 'High (75% of farmers achieve this)'
            },
            'moderate': {
                'target_yield': benchmarks['top_10_percent'],
                'improvement': round(benchmarks['top_10_percent'] - user_yield, 2),
                'improvement_percent': round((benchmarks['top_10_percent'] - user_yield) / user_yield * 100, 1) if user_yield > 0 else 0,
                'achievability': 'Medium (10% of farmers achieve this)'
            },
            'aggressive': {
                'target_yield': benchmarks['max_yield_achieved'],
                'improvement': round(benchmarks['max_yield_achieved'] - user_yield, 2),
                'improvement_percent': round((benchmarks['max_yield_achieved'] - user_yield) / user_yield * 100, 1) if user_yield > 0 else 0,
                'achievability': 'Low (best case scenario)'
            }
        }
        
        return potential
    
    def _generate_recommendations(self, user_yield: float, benchmarks: Dict, crop: str, state: str, season: str) -> List[str]:
        """Generate specific recommendations based on yield gap analysis."""
        
        recommendations = []
        
        # Performance assessment
        if user_yield >= benchmarks['top_10_percent']:
            recommendations.append("🏆 Excellent! You're already in the top 10% of performers.")
        elif user_yield >= benchmarks['top_25_percent']:
            recommendations.append("👍 Good performance! You're in the top 25% range.")
        elif user_yield >= benchmarks['average_yield']:
            recommendations.append("📈 Above average, but room for improvement.")
        else:
            recommendations.append("🎯 Significant improvement potential identified.")
        
        # Specific improvement suggestions
        improvement_factors = benchmarks['improvement_factors']
        
        if improvement_factors['key_insights']:
            recommendations.extend(improvement_factors['key_insights'])
        
        # High performer characteristics
        if 'consistent_high_performers' in benchmarks:
            char = benchmarks['consistent_high_performers']['characteristics']
            if 'avg_fertilizer' in char:
                recommendations.append(f"💡 Top performers use ~{char['avg_fertilizer']:.0f} kg/ha fertilizer on average")
            if 'optimal_pH' in char:
                recommendations.append(f"🌱 Optimal soil conditions: pH {char['optimal_pH']}, N:{char['optimal_N']:.0f}, P:{char['optimal_P']:.0f}, K:{char['optimal_K']:.0f}")
        
        return recommendations
    
    def generate_visualization_data(self, user_yield: float, crop: str, state: str, season: str = None) -> Dict:
        """Generate data for creating yield comparison visualizations."""
        
        data = self.data_loader.filter_data(crop=crop, state=state, season=season)
        if data.empty:
            return {'error': 'No data available for visualization'}
        
        benchmarks = self.calculate_yield_benchmarks(crop, state, season)
        
        viz_data = {
            'user_yield': user_yield,
            'yield_distribution': data['yield'].tolist(),
            'benchmarks': {
                'average': benchmarks['average_yield'],
                'top_25': benchmarks['top_25_percent'],
                'top_10': benchmarks['top_10_percent'],
                'maximum': benchmarks['max_yield_achieved']
            },
            'yearly_trend': data.groupby('year')['yield'].mean().to_dict(),
            'percentile_rank': self._calculate_percentile_rank(user_yield, crop, state, season)
        }
        
        return viz_data