"""
Multi-Scenario Outcome Predictor

Provides farmers with multiple "what-if" scenarios for different farming decisions,
comparing outcomes across different strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class MultiScenarioPredictor:
    """Predicts outcomes for multiple farming scenarios."""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
    def train_prediction_model(self):
        """Train the ML model for yield prediction."""
        print("Training multi-scenario prediction model...")
        
        if self.data_loader.merged_data is None:
            self.data_loader.merge_datasets()
            
        data = self.data_loader.merged_data.dropna()
        
        # Define features for prediction
        categorical_features = ['crop', 'state', 'season']
        numerical_features = ['area', 'fertilizer', 'pesticide', 'avg_temp_c', 
                            'total_rainfall_mm', 'avg_humidity_percent', 'N', 'P', 'K', 'pH']
        
        self.feature_columns = categorical_features + numerical_features
        
        # Prepare features
        X = data[self.feature_columns].copy()
        y = data['yield'].values
        
        # Encode categorical variables
        for col in categorical_features:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
            
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"✅ Model trained successfully!")
        print(f"   Training R²: {train_score:.3f}")
        print(f"   Testing R²: {test_score:.3f}")
        
        self.is_trained = True
        return test_score
    
    def create_scenarios(self, base_params: Dict) -> List[Dict]:
        """Create multiple scenarios based on different farming strategies."""
        
        scenarios = []
        
        # Base scenario
        base_scenario = base_params.copy()
        base_scenario['scenario_name'] = 'Current Practice'
        base_scenario['scenario_type'] = 'baseline'
        base_scenario['description'] = 'Your current farming approach'
        scenarios.append(base_scenario)
        
        # Fertilizer optimization scenarios
        base_fertilizer = base_params.get('fertilizer', 25000)
        
        # Reduced fertilizer scenario
        reduced_fert = base_params.copy()
        reduced_fert['fertilizer'] = base_fertilizer * 0.85  # 15% reduction
        reduced_fert['scenario_name'] = 'Reduced Fertilizer'
        reduced_fert['scenario_type'] = 'cost_saving'
        reduced_fert['description'] = '15% less fertilizer - cost savings vs yield trade-off'
        scenarios.append(reduced_fert)
        
        # Increased fertilizer scenario
        increased_fert = base_params.copy()
        increased_fert['fertilizer'] = base_fertilizer * 1.2  # 20% increase
        increased_fert['scenario_name'] = 'Enhanced Fertilizer'
        increased_fert['scenario_type'] = 'yield_maximizing'
        increased_fert['description'] = '20% more fertilizer - maximize yield approach'
        scenarios.append(increased_fert)
        
        # Season variation scenarios (if season can be varied)
        if 'season' in base_params:
            current_season = base_params['season']
            available_seasons = self._get_available_seasons(base_params['crop'], base_params['state'])
            
            for season in available_seasons:
                if season != current_season:
                    season_scenario = base_params.copy()
                    season_scenario['season'] = season
                    season_scenario['scenario_name'] = f'{season} Season'
                    season_scenario['scenario_type'] = 'timing_variation'
                    season_scenario['description'] = f'Plant in {season} season instead'
                    scenarios.append(season_scenario)
        
        # Precision farming scenario (optimal inputs based on historical data)
        optimal_scenario = self._create_optimal_scenario(base_params)
        if optimal_scenario:
            scenarios.append(optimal_scenario)
        
        # Risk-averse scenario (conservative inputs)
        conservative_scenario = self._create_conservative_scenario(base_params)
        if conservative_scenario:
            scenarios.append(conservative_scenario)
        
        return scenarios[:6]  # Limit to 6 scenarios for UI clarity
    
    def _get_available_seasons(self, crop: str, state: str) -> List[str]:
        """Get available seasons for a crop-state combination."""
        data = self.data_loader.filter_data(crop=crop, state=state)
        return data['season'].str.strip().unique().tolist()
    
    def _create_optimal_scenario(self, base_params: Dict) -> Dict:
        """Create scenario with optimal inputs based on historical best performers."""
        
        # Get top 10% performers for this crop-state combination
        data = self.data_loader.filter_data(
            crop=base_params['crop'],
            state=base_params['state'],
            season=base_params.get('season')
        )
        
        if data.empty:
            return None
            
        top_performers = data[data['yield'] >= data['yield'].quantile(0.9)]
        
        if len(top_performers) < 3:  # Need at least 3 records for reliable averages
            return None
        
        optimal_scenario = base_params.copy()
        optimal_scenario['fertilizer'] = round(top_performers['fertilizer'].median())
        optimal_scenario['pesticide'] = round(top_performers['pesticide'].median())
        optimal_scenario['scenario_name'] = 'Top Performer Strategy'
        optimal_scenario['scenario_type'] = 'optimized'
        optimal_scenario['description'] = 'Based on top 10% performers in your region'
        
        return optimal_scenario
    
    def _create_conservative_scenario(self, base_params: Dict) -> Dict:
        """Create conservative scenario with lower inputs but more predictable outcomes."""
        
        conservative_scenario = base_params.copy()
        conservative_scenario['fertilizer'] = base_params.get('fertilizer', 25000) * 0.9
        conservative_scenario['pesticide'] = base_params.get('pesticide', 500) * 0.8
        conservative_scenario['scenario_name'] = 'Conservative Approach'
        conservative_scenario['scenario_type'] = 'risk_averse'
        conservative_scenario['description'] = 'Lower inputs, more predictable outcomes'
        
        return conservative_scenario
    
    def predict_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """Predict outcomes for all scenarios."""
        
        if not self.is_trained:
            self.train_prediction_model()
        
        results = []
        
        for scenario in scenarios:
            # Prepare input for prediction
            input_data = self._prepare_input_for_prediction(scenario)
            
            if input_data is None:
                continue
                
            # Make prediction
            predicted_yield = self.model.predict([input_data])[0]
            
            # Calculate confidence intervals using model uncertainty
            prediction_std = self._calculate_prediction_uncertainty(input_data)
            confidence_lower = predicted_yield - 1.96 * prediction_std
            confidence_upper = predicted_yield + 1.96 * prediction_std
            
            # Calculate additional metrics
            result = scenario.copy()
            result['predicted_yield'] = round(predicted_yield, 2)
            result['confidence_interval'] = {
                'lower': round(max(0, confidence_lower), 2),
                'upper': round(confidence_upper, 2)
            }
            result['yield_range'] = f"{result['confidence_interval']['lower']:.1f} - {result['confidence_interval']['upper']:.1f}"
            result['risk_level'] = self._assess_risk_level(prediction_std, predicted_yield)
            result['estimated_profit'] = self._estimate_profit(scenario, predicted_yield)
            
            results.append(result)
        
        # Sort by predicted yield (descending)
        results.sort(key=lambda x: x['predicted_yield'], reverse=True)
        
        return results
    
    def _prepare_input_for_prediction(self, scenario: Dict) -> List:
        """Prepare scenario parameters for model prediction."""
        
        try:
            # Create input array matching training features
            input_row = []
            
            # Categorical features
            for col in ['crop', 'state', 'season']:
                if col in scenario and col in self.label_encoders:
                    encoded_value = self._safe_transform(self.label_encoders[col], scenario[col])
                    input_row.append(encoded_value)
                else:
                    return None  # Missing required feature
            
            # Numerical features
            numerical_features = ['area', 'fertilizer', 'pesticide', 'avg_temp_c', 
                                'total_rainfall_mm', 'avg_humidity_percent', 'N', 'P', 'K', 'pH']
            
            for col in numerical_features:
                if col in scenario:
                    input_row.append(float(scenario[col]))
                else:
                    # Use default values from historical data for missing features
                    default_value = self._get_default_value(col, scenario)
                    input_row.append(default_value)
            
            return input_row
            
        except Exception as e:
            print(f"Error preparing input for scenario: {e}")
            return None
    
    def _safe_transform(self, encoder, value):
        """Safely transform categorical value, handling unseen categories."""
        try:
            return encoder.transform([str(value)])[0]
        except ValueError:
            # Return the most common category if unseen
            return 0
    
    def _get_default_value(self, feature: str, scenario: Dict) -> float:
        """Get default value for missing features based on historical data."""
        
        # Try to get values specific to crop/state
        data = self.data_loader.filter_data(
            crop=scenario.get('crop'),
            state=scenario.get('state')
        )
        
        if not data.empty and feature in data.columns:
            return float(data[feature].median())
        
        # Fallback to global defaults
        defaults = {
            'area': 1000,
            'fertilizer': 25000,
            'pesticide': 500,
            'avg_temp_c': 25.0,
            'total_rainfall_mm': 1000.0,
            'avg_humidity_percent': 70.0,
            'N': 75,
            'P': 35,
            'K': 30,
            'pH': 6.5
        }
        
        return defaults.get(feature, 0.0)
    
    def _calculate_prediction_uncertainty(self, input_data: List) -> float:
        """Calculate prediction uncertainty using model variance."""
        
        # Get predictions from all trees in random forest
        tree_predictions = []
        for tree in self.model.estimators_:
            pred = tree.predict([input_data])[0]
            tree_predictions.append(pred)
        
        # Calculate standard deviation of predictions
        return np.std(tree_predictions)
    
    def _assess_risk_level(self, uncertainty: float, predicted_yield: float) -> str:
        """Assess risk level based on prediction uncertainty."""
        
        if predicted_yield == 0:
            return 'high'
            
        coefficient_of_variation = uncertainty / predicted_yield
        
        if coefficient_of_variation < 0.15:
            return 'low'
        elif coefficient_of_variation < 0.3:
            return 'medium'
        else:
            return 'high'
    
    def _estimate_profit(self, scenario: Dict, predicted_yield: float) -> Dict:
        """Estimate profit based on yield and costs (simplified calculation)."""
        
        # Simplified profit calculation (would need real price data for accuracy)
        price_per_quintal = 2000  # Simplified average price
        
        # Revenue
        revenue = predicted_yield * scenario.get('area', 1) * price_per_quintal
        
        # Costs (simplified)
        fertilizer_cost = scenario.get('fertilizer', 0) * 0.02  # ₹0.02 per kg
        pesticide_cost = scenario.get('pesticide', 0) * 0.5     # ₹0.5 per kg
        other_costs = scenario.get('area', 1) * 5000           # Fixed costs per area
        
        total_costs = fertilizer_cost + pesticide_cost + other_costs
        profit = revenue - total_costs
        
        return {
            'revenue': round(revenue, 0),
            'costs': round(total_costs, 0),
            'profit': round(profit, 0),
            'profit_per_hectare': round(profit / scenario.get('area', 1), 0)
        }
    
    def compare_scenarios(self, results: List[Dict]) -> Dict:
        """Compare scenarios and provide recommendations."""
        
        if not results:
            return {'error': 'No valid scenarios to compare'}
        
        # Find best scenarios by different criteria
        best_yield = max(results, key=lambda x: x['predicted_yield'])
        best_profit = max(results, key=lambda x: x['estimated_profit']['profit'])
        lowest_risk = min(results, key=lambda x: {'low': 1, 'medium': 2, 'high': 3}[x['risk_level']])
        
        comparison = {
            'total_scenarios': len(results),
            'best_for_yield': {
                'scenario': best_yield['scenario_name'],
                'yield': best_yield['predicted_yield'],
                'improvement_over_baseline': round(best_yield['predicted_yield'] - results[-1]['predicted_yield'], 2)
            },
            'best_for_profit': {
                'scenario': best_profit['scenario_name'],
                'profit': best_profit['estimated_profit']['profit'],
                'improvement_over_baseline': round(best_profit['estimated_profit']['profit'] - results[-1]['estimated_profit']['profit'], 0)
            },
            'lowest_risk': {
                'scenario': lowest_risk['scenario_name'],
                'risk_level': lowest_risk['risk_level'],
                'yield': lowest_risk['predicted_yield']
            },
            'recommendations': self._generate_scenario_recommendations(results)
        }
        
        return comparison
    
    def _generate_scenario_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on scenario comparison."""
        
        recommendations = []
        
        # Compare baseline to best scenarios
        baseline = next((r for r in results if r['scenario_type'] == 'baseline'), results[-1])
        
        # Find significant improvements
        for result in results:
            if result['scenario_type'] == 'baseline':
                continue
                
            yield_improvement = result['predicted_yield'] - baseline['predicted_yield']
            if yield_improvement > 2:  # More than 2 quintal/ha improvement
                profit_improvement = result['estimated_profit']['profit'] - baseline['estimated_profit']['profit']
                recommendations.append(
                    f"🌟 {result['scenario_name']}: +{yield_improvement:.1f} quintal/ha "
                    f"(₹{profit_improvement:,.0f} additional profit)"
                )
        
        # Risk assessment
        high_risk_scenarios = [r for r in results if r['risk_level'] == 'high']
        if high_risk_scenarios:
            recommendations.append(
                f"⚠️ High-risk scenarios: {', '.join([s['scenario_name'] for s in high_risk_scenarios])}"
            )
        
        # Conservative recommendation
        safe_scenarios = [r for r in results if r['risk_level'] == 'low']
        if safe_scenarios:
            best_safe = max(safe_scenarios, key=lambda x: x['predicted_yield'])
            recommendations.append(
                f"🛡️ Safest option: {best_safe['scenario_name']} ({best_safe['predicted_yield']:.1f} quintal/ha, low risk)"
            )
        
        return recommendations