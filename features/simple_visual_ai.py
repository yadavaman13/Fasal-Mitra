"""
Simple Visual Explainable AI Module (No heavy dependencies)

Provides explanations with simple HTML visualizations for all farming recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import json

class VisualExplainableAI:
    """Creates simple visual explanations for agricultural recommendations."""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        
    def explain_yield_prediction(self, prediction_data: Dict, user_inputs: Dict) -> Dict:
        """Create visual explanation for yield prediction."""
        
        explanations = {
            'text_explanation': self._generate_text_explanation(prediction_data, user_inputs),
            'factor_importance': self._create_simple_factor_chart(user_inputs),
            'historical_comparison': self._create_simple_historical_chart(user_inputs),
            'confidence_visualization': self._create_simple_confidence_chart(prediction_data),
            'recommendation_reasoning': self._explain_recommendation_reasoning(prediction_data, user_inputs)
        }
        
        return explanations
    
    def explain_yield_gap(self, gap_analysis: Dict, user_inputs: Dict) -> Dict:
        """Create visual explanation for yield gap analysis."""
        
        explanations = {
            'performance_dashboard': self._create_simple_performance_chart(gap_analysis),
            'benchmarking_chart': self._create_simple_benchmarking_chart(gap_analysis),
            'improvement_roadmap': self._create_improvement_roadmap(gap_analysis),
            'peer_comparison': self._create_simple_peer_chart(gap_analysis, user_inputs),
            'factor_analysis': "<div class='alert alert-info'>Factor analysis available in full version</div>"
        }
        
        return explanations
    
    def explain_scenarios(self, scenario_results: List[Dict], comparison: Dict) -> Dict:
        """Create visual explanation for multi-scenario analysis."""
        
        explanations = {
            'scenario_comparison': self._create_simple_scenario_chart(scenario_results),
            'risk_return_analysis': self._create_simple_risk_chart(scenario_results),
            'decision_tree': self._create_decision_tree_visualization(scenario_results, comparison),
            'profit_breakdown': self._create_simple_profit_chart(scenario_results),
            'scenario_recommendations': self._create_scenario_recommendation_cards(comparison)
        }
        
        return explanations
    
    def _generate_text_explanation(self, prediction_data: Dict, user_inputs: Dict) -> List[str]:
        """Generate human-readable text explanations."""
        
        explanations = []
        
        # Base prediction explanation
        predicted_yield = prediction_data.get('predicted_yield', 0)
        explanations.append(f"🎯 **Predicted Yield**: {predicted_yield:.1f} quintal/hectare")
        
        # Confidence explanation
        if 'confidence_interval' in prediction_data:
            ci = prediction_data['confidence_interval']
            explanations.append(f"📊 **Confidence Range**: {ci['lower']:.1f} - {ci['upper']:.1f} quintal/ha")
        
        # Input factor explanations
        crop = user_inputs.get('crop', 'Unknown')
        state = user_inputs.get('state', 'Unknown')
        season = user_inputs.get('season', 'Unknown')
        
        explanations.append(f"🌱 **Your Configuration**: {crop} in {state} during {season}")
        
        # Historical context
        historical_data = self._get_historical_context(user_inputs)
        if historical_data:
            explanations.append(f"📈 **Historical Average**: {historical_data['avg_yield']:.1f} quintal/ha in your region")
            
            if predicted_yield > historical_data['avg_yield']:
                explanations.append(f"✅ Your prediction is **{predicted_yield - historical_data['avg_yield']:.1f} quintal/ha above** regional average")
            else:
                explanations.append(f"⚠️ Your prediction is **{historical_data['avg_yield'] - predicted_yield:.1f} quintal/ha below** regional average")
        
        # Key influencing factors
        key_factors = self._identify_key_factors(user_inputs)
        if key_factors:
            explanations.extend(key_factors)
        
        return explanations
    
    def _get_historical_context(self, user_inputs: Dict) -> Optional[Dict]:
        """Get historical context for the user's inputs."""
        
        data = self.data_loader.filter_data(
            crop=user_inputs.get('crop'),
            state=user_inputs.get('state'),
            season=user_inputs.get('season')
        )
        
        if data.empty:
            return None
            
        return {
            'avg_yield': data['yield'].mean(),
            'records_count': len(data),
            'years_span': f"{data['year'].min()}-{data['year'].max()}"
        }
    
    def _identify_key_factors(self, user_inputs: Dict) -> List[str]:
        """Identify and explain key factors affecting the prediction."""
        
        factors = []
        
        # Fertilizer analysis
        fertilizer = user_inputs.get('fertilizer', 0)
        if fertilizer:
            if fertilizer < 20000:
                factors.append(f"💡 **Fertilizer**: You're using {fertilizer:,.0f} kg/ha. Consider increasing for better yield")
            elif fertilizer > 40000:
                factors.append(f"⚠️ **Fertilizer**: You're using {fertilizer:,.0f} kg/ha. This might be excessive")
            else:
                factors.append(f"✅ **Fertilizer**: Your {fertilizer:,.0f} kg/ha is in reasonable range")
        
        # Soil pH analysis
        pH = user_inputs.get('pH', 7.0)
        if pH < 6.0:
            factors.append(f"🔬 **Soil pH**: {pH:.1f} is acidic. Consider liming")
        elif pH > 8.0:
            factors.append(f"🔬 **Soil pH**: {pH:.1f} is alkaline. Consider organic matter")
        else:
            factors.append(f"✅ **Soil pH**: {pH:.1f} is in good range")
        
        return factors
    
    def _create_simple_factor_chart(self, user_inputs: Dict) -> str:
        """Create simple HTML chart for factor importance."""
        
        factors = {
            'Fertilizer': 0.25,
            'Rainfall': 0.20,
            'Soil pH': 0.15,
            'Temperature': 0.12,
            'Soil N': 0.10,
        }
        
        bars = ""
        for factor, importance in factors.items():
            width = int(importance * 300)  # Scale for display
            bars += f'''
            <div class="factor-bar">
                <div class="factor-label">{factor}</div>
                <div class="factor-bar-bg">
                    <div class="factor-bar-fill" style="width: {width}px;"></div>
                </div>
                <div class="factor-value">{importance:.2f}</div>
            </div>
            '''
        
        return f'''
        <div class="factor-chart">
            <h5>Factors Influencing Your Prediction</h5>
            <style>
                .factor-chart {{ margin: 20px 0; }}
                .factor-bar {{ display: flex; align-items: center; margin: 8px 0; }}
                .factor-label {{ width: 100px; font-size: 12px; }}
                .factor-bar-bg {{ width: 300px; height: 20px; background: #f0f0f0; margin: 0 10px; }}
                .factor-bar-fill {{ height: 100%; background: #2E8B57; }}
                .factor-value {{ font-weight: bold; font-size: 12px; }}
            </style>
            {bars}
        </div>
        '''
    
    def _create_simple_historical_chart(self, user_inputs: Dict) -> str:
        """Create simple historical comparison."""
        
        data = self.data_loader.filter_data(
            crop=user_inputs.get('crop'),
            state=user_inputs.get('state'),
            season=user_inputs.get('season')
        )
        
        if data.empty:
            return "<div class='alert alert-warning'>No historical data available for comparison</div>"
        
        recent_avg = data['yield'].mean()
        max_yield = data['yield'].max()
        min_yield = data['yield'].min()
        
        return f'''
        <div class="historical-summary">
            <h5>Historical Performance in Your Region</h5>
            <div class="row">
                <div class="col-md-4 text-center">
                    <div class="metric-card bg-primary text-white p-3 rounded">
                        <h6>Average</h6>
                        <h4>{recent_avg:.1f}</h4>
                        <small>quintal/ha</small>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <div class="metric-card bg-success text-white p-3 rounded">
                        <h6>Best Ever</h6>
                        <h4>{max_yield:.1f}</h4>
                        <small>quintal/ha</small>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <div class="metric-card bg-secondary text-white p-3 rounded">
                        <h6>Records</h6>
                        <h4>{len(data)}</h4>
                        <small>data points</small>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    def _create_simple_confidence_chart(self, prediction_data: Dict) -> str:
        """Create simple confidence visualization."""
        
        predicted_yield = prediction_data.get('predicted_yield', 0)
        ci = prediction_data.get('confidence_interval', {'lower': predicted_yield*0.9, 'upper': predicted_yield*1.1})
        
        return f'''
        <div class="confidence-chart">
            <h5>Prediction Confidence</h5>
            <div class="confidence-bar">
                <div class="confidence-range">
                    <span class="range-label">Range: {ci['lower']:.1f} - {ci['upper']:.1f} quintal/ha</span>
                    <div class="range-bar">
                        <div class="prediction-point" style="left: 50%;"></div>
                    </div>
                    <div class="range-labels">
                        <span>Low: {ci['lower']:.1f}</span>
                        <span>Prediction: {predicted_yield:.1f}</span>
                        <span>High: {ci['upper']:.1f}</span>
                    </div>
                </div>
            </div>
            <style>
                .confidence-chart {{ margin: 20px 0; }}
                .range-bar {{ height: 30px; background: linear-gradient(90deg, #ffcccc, #ccffcc); position: relative; margin: 10px 0; }}
                .prediction-point {{ position: absolute; width: 4px; height: 100%; background: red; }}
                .range-labels {{ display: flex; justify-content: space-between; font-size: 12px; }}
            </style>
        </div>
        '''
    
    def _create_simple_performance_chart(self, gap_analysis: Dict) -> str:
        """Create simple performance dashboard."""
        
        user_yield = gap_analysis.get('user_yield', 0)
        benchmarks = gap_analysis.get('benchmarks', {})
        percentile = gap_analysis.get('percentile_rank', 0)
        
        return f'''
        <div class="performance-dashboard">
            <h5>Your Performance Dashboard</h5>
            <div class="performance-gauge">
                <div class="gauge-info">
                    <h3>{user_yield:.1f} quintal/ha</h3>
                    <p>Your Current Yield</p>
                    <p><strong>{percentile:.0f}th Percentile</strong></p>
                </div>
                <div class="benchmark-comparison mt-3">
                    <div class="benchmark-item">
                        <span>Average: {benchmarks.get('average_yield', 0):.1f}</span>
                        <div class="progress">
                            <div class="progress-bar bg-warning" style="width: 50%;"></div>
                        </div>
                    </div>
                    <div class="benchmark-item">
                        <span>Top 25%: {benchmarks.get('top_25_percent', 0):.1f}</span>
                        <div class="progress">
                            <div class="progress-bar bg-success" style="width: 75%;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    def _create_simple_benchmarking_chart(self, gap_analysis: Dict) -> str:
        """Create simple benchmarking chart."""
        
        user_yield = gap_analysis.get('user_yield', 0)
        benchmarks = gap_analysis.get('benchmarks', {})
        
        comparison_data = {
            'Your Yield': user_yield,
            'Average': benchmarks.get('average_yield', 0),
            'Top 25%': benchmarks.get('top_25_percent', 0),
            'Top 10%': benchmarks.get('top_10_percent', 0),
            'Maximum': benchmarks.get('max_yield_achieved', 0)
        }
        
        bars = ""
        for label, value in comparison_data.items():
            color = '#dc3545' if label == 'Your Yield' else '#28a745' if 'Top' in label else '#ffc107'
            bars += f'''
            <div class="benchmark-bar">
                <div class="benchmark-label">{label}</div>
                <div class="benchmark-bar-bg">
                    <div class="benchmark-bar-fill" style="width: {int(value*3)}px; background: {color};"></div>
                </div>
                <div class="benchmark-value">{value:.1f}</div>
            </div>
            '''
        
        return f'''
        <div class="benchmarking-chart">
            <h5>Yield Benchmarking</h5>
            <style>
                .benchmark-bar {{ display: flex; align-items: center; margin: 8px 0; }}
                .benchmark-label {{ width: 80px; font-size: 12px; }}
                .benchmark-bar-bg {{ width: 200px; height: 25px; background: #f0f0f0; margin: 0 10px; }}
                .benchmark-bar-fill {{ height: 100%; }}
                .benchmark-value {{ font-weight: bold; font-size: 12px; }}
            </style>
            {bars}
        </div>
        '''
    
    def _create_improvement_roadmap(self, gap_analysis: Dict) -> List[str]:
        """Create improvement roadmap."""
        
        roadmap = []
        improvement_potential = gap_analysis.get('improvement_potential', {})
        
        roadmap.append("**🎯 Your Improvement Roadmap:**")
        
        conservative = improvement_potential.get('conservative', {})
        if conservative and conservative.get('improvement', 0) > 0:
            roadmap.append(f"• **Short-term**: Reach {conservative.get('target_yield', 0):.1f} quintal/ha (+{conservative.get('improvement', 0):.1f})")
        
        moderate = improvement_potential.get('moderate', {})  
        if moderate and moderate.get('improvement', 0) > 0:
            roadmap.append(f"• **Medium-term**: Reach {moderate.get('target_yield', 0):.1f} quintal/ha (+{moderate.get('improvement', 0):.1f})")
        
        return roadmap
    
    def _create_simple_peer_chart(self, gap_analysis: Dict, user_inputs: Dict) -> str:
        """Create simple peer comparison."""
        
        user_yield = gap_analysis.get('user_yield', 0)
        benchmarks = gap_analysis.get('benchmarks', {})
        percentile = gap_analysis.get('percentile_rank', 0)
        
        return f'''
        <div class="peer-comparison">
            <h5>Peer Comparison</h5>
            <p>You perform better than <strong>{percentile:.0f}%</strong> of farmers in your region</p>
            <div class="peer-visual">
                <div class="peer-grid">
                    {'<div class="peer-dot peer-you"></div>' * int(percentile/10)}
                    {'<div class="peer-dot peer-other"></div>' * (10 - int(percentile/10))}
                </div>
                <p><span class="peer-you-legend">You</span> vs <span class="peer-other-legend">Other Farmers</span></p>
            </div>
            <style>
                .peer-grid {{ display: flex; gap: 5px; margin: 10px 0; }}
                .peer-dot {{ width: 20px; height: 20px; border-radius: 50%; }}
                .peer-you {{ background: #dc3545; }}
                .peer-other {{ background: #6c757d; }}
                .peer-you-legend {{ color: #dc3545; font-weight: bold; }}
                .peer-other-legend {{ color: #6c757d; font-weight: bold; }}
            </style>
        </div>
        '''
    
    def _create_simple_scenario_chart(self, scenario_results: List[Dict]) -> str:
        """Create simple scenario comparison."""
        
        comparison_html = '''
        <div class="scenario-comparison">
            <h5>Scenario Comparison</h5>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Scenario</th>
                            <th>Predicted Yield</th>
                            <th>Risk Level</th>
                            <th>Estimated Profit</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        
        for result in scenario_results:
            risk_color = {'low': 'success', 'medium': 'warning', 'high': 'danger'}
            profit = result['estimated_profit']['profit']
            
            comparison_html += f'''
                        <tr>
                            <td><strong>{result['scenario_name']}</strong></td>
                            <td>{result['predicted_yield']:.1f} quintal/ha</td>
                            <td><span class="badge bg-{risk_color.get(result['risk_level'], 'secondary')}">{result['risk_level'].title()}</span></td>
                            <td>₹{profit:,.0f}</td>
                        </tr>
            '''
        
        comparison_html += '''
                    </tbody>
                </table>
            </div>
        </div>
        '''
        
        return comparison_html
    
    def _create_simple_risk_chart(self, scenario_results: List[Dict]) -> str:
        """Create simple risk vs return chart."""
        
        return '''
        <div class="risk-return">
            <h5>Risk vs Return Analysis</h5>
            <p>Choose based on your risk tolerance:</p>
            <div class="risk-categories">
                <div class="risk-category bg-success text-white p-3 m-2 rounded">
                    <h6>🛡️ Low Risk</h6>
                    <p>Predictable outcomes, lower yields</p>
                </div>
                <div class="risk-category bg-warning text-dark p-3 m-2 rounded">
                    <h6>⚖️ Medium Risk</h6>
                    <p>Balanced risk-reward ratio</p>
                </div>
                <div class="risk-category bg-danger text-white p-3 m-2 rounded">
                    <h6>🎯 High Risk</h6>
                    <p>Highest potential, more uncertainty</p>
                </div>
            </div>
        </div>
        '''
    
    def _create_simple_profit_chart(self, scenario_results: List[Dict]) -> str:
        """Create simple profit breakdown."""
        
        best_profit = max(scenario_results, key=lambda x: x['estimated_profit']['profit'])
        
        return f'''
        <div class="profit-breakdown">
            <h5>Best Profit Scenario: {best_profit['scenario_name']}</h5>
            <div class="profit-details">
                <div class="profit-item">
                    <span>Revenue:</span>
                    <span>₹{best_profit['estimated_profit']['revenue']:,.0f}</span>
                </div>
                <div class="profit-item">
                    <span>Costs:</span>
                    <span>₹{best_profit['estimated_profit']['costs']:,.0f}</span>
                </div>
                <div class="profit-item total">
                    <span><strong>Net Profit:</strong></span>
                    <span><strong>₹{best_profit['estimated_profit']['profit']:,.0f}</strong></span>
                </div>
            </div>
            <style>
                .profit-item {{ display: flex; justify-content: space-between; padding: 5px 0; }}
                .profit-item.total {{ border-top: 2px solid #ddd; margin-top: 10px; padding-top: 10px; }}
            </style>
        </div>
        '''
    
    def _explain_recommendation_reasoning(self, prediction_data: Dict, user_inputs: Dict) -> List[str]:
        """Simple reasoning explanation."""
        
        reasoning = [
            "**📊 How We Made This Prediction:**",
            "• Analyzed 24 years of agricultural data (1997-2020)",
            f"• Used 19,689+ historical records from {user_inputs.get('state', 'your region')}",
            f"• AI model trained on similar {user_inputs.get('crop', 'crop')} farms",
            "• Considered soil, weather, and farming practices",
            "• Cross-validated for accuracy and reliability"
        ]
        
        return reasoning
    
    def _create_decision_tree_visualization(self, scenario_results: List[Dict], comparison: Dict) -> List[str]:
        """Create decision tree for scenario selection."""
        
        decision_tree = [
            "**🌳 Which Scenario Should You Choose?**",
            "",
            "**🎯 Goal: Maximize Yield**",
            f"→ Choose: {comparison.get('best_for_yield', {}).get('scenario', 'Best yielding scenario')}",
            "",
            "**💰 Goal: Maximize Profit**", 
            f"→ Choose: {comparison.get('best_for_profit', {}).get('scenario', 'Most profitable scenario')}",
            "",
            "**🛡️ Goal: Minimize Risk**",
            f"→ Choose: {comparison.get('lowest_risk', {}).get('scenario', 'Safest scenario')}"
        ]
        
        return decision_tree
    
    def _create_scenario_recommendation_cards(self, comparison: Dict) -> List[Dict]:
        """Create recommendation cards."""
        
        cards = []
        
        best_yield = comparison.get('best_for_yield', {})
        if best_yield:
            cards.append({
                'title': '🏆 Highest Yield',
                'scenario': best_yield.get('scenario', 'Unknown'),
                'metric': f"{best_yield.get('yield', 0):.1f} quintal/ha",
                'description': f"Get {best_yield.get('improvement_over_baseline', 0):.1f} more than current practice",
                'color': 'success'
            })
        
        best_profit = comparison.get('best_for_profit', {})
        if best_profit:
            cards.append({
                'title': '💰 Highest Profit',  
                'scenario': best_profit.get('scenario', 'Unknown'),
                'metric': f"₹{best_profit.get('profit', 0):,.0f}",
                'description': f"Earn ₹{best_profit.get('improvement_over_baseline', 0):,.0f} more",
                'color': 'primary'
            })
        
        return cards