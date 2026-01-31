"""
AI-Powered Crop Disease Detection System

Uses computer vision to identify crop diseases, assess severity, and provide treatment recommendations.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import random
from PIL import Image
import io

class CropDiseaseDetector:
    """AI-powered crop disease detection and treatment recommendation system."""
    
    def __init__(self, data_loader=None):
        self.data_loader = data_loader
        
        # Disease database with comprehensive information
        self.disease_database = {
            'leaf_spot': {
                'name': 'Leaf Spot Disease',
                'crops_affected': ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato'],
                'symptoms': ['Brown/black spots on leaves', 'Yellowing around spots', 'Premature leaf drop'],
                'causes': ['Fungal infection', 'High humidity', 'Poor air circulation'],
                'severity_indicators': {
                    'mild': 'Few scattered spots (1-5% leaf area)',
                    'moderate': 'Multiple spots covering 5-25% leaf area',
                    'severe': 'Extensive spotting >25% leaf area, leaf yellowing'
                },
                'treatments': {
                    'mild': ['Copper-based fungicide spray', 'Improve air circulation', 'Remove affected leaves'],
                    'moderate': ['Systemic fungicide (Propiconazole)', 'Weekly spraying for 3 weeks', 'Reduce irrigation frequency'],
                    'severe': ['Immediate fungicide treatment', 'Remove severely affected plants', 'Soil treatment with beneficial microbes']
                },
                'prevention': [
                    'Crop rotation with non-host crops',
                    'Proper spacing for air circulation',
                    'Avoid overhead irrigation',
                    'Regular field sanitation',
                    'Use resistant varieties'
                ],
                'cost_estimate': {'mild': 500, 'moderate': 1500, 'severe': 3000}
            },
            
            'bacterial_blight': {
                'name': 'Bacterial Blight',
                'crops_affected': ['Rice', 'Cotton', 'Beans', 'Citrus'],
                'symptoms': ['Water-soaked lesions', 'Yellow halos around spots', 'Wilting of leaves'],
                'causes': ['Bacterial infection', 'Wounds from insects/tools', 'Wet conditions'],
                'severity_indicators': {
                    'mild': 'Few lesions on lower leaves',
                    'moderate': 'Spread to middle leaves, some yellowing',
                    'severe': 'Extensive wilting, plant death possible'
                },
                'treatments': {
                    'mild': ['Copper hydroxide spray', 'Remove infected debris', 'Improve drainage'],
                    'moderate': ['Streptomycin antibiotic', 'Copper-based bactericide', 'Enhanced sanitation'],
                    'severe': ['Immediate plant removal', 'Soil sterilization', 'Quarantine affected area']
                },
                'prevention': [
                    'Use certified disease-free seeds',
                    'Sterilize tools between plants',
                    'Avoid working in wet conditions',
                    'Control insect vectors',
                    'Proper field drainage'
                ],
                'cost_estimate': {'mild': 800, 'moderate': 2000, 'severe': 4000}
            },
            
            'powdery_mildew': {
                'name': 'Powdery Mildew',
                'crops_affected': ['Wheat', 'Barley', 'Cotton', 'Grapes', 'Cucumber'],
                'symptoms': ['White powdery coating on leaves', 'Stunted growth', 'Reduced yield'],
                'causes': ['Fungal spores', 'High humidity with dry conditions', 'Poor air circulation'],
                'severity_indicators': {
                    'mild': 'Light dusting on few leaves',
                    'moderate': 'Moderate coverage on 10-30% of plant',
                    'severe': 'Heavy white coating, leaf distortion'
                },
                'treatments': {
                    'mild': ['Sulfur-based spray', 'Baking soda solution (1%)', 'Improve air flow'],
                    'moderate': ['Systemic fungicide (Myclobutanil)', 'Weekly applications', 'Remove infected leaves'],
                    'severe': ['Triazole fungicides', 'Destroy heavily infected plants', 'Soil treatment']
                },
                'prevention': [
                    'Plant resistant varieties',
                    'Ensure proper plant spacing',
                    'Avoid late evening irrigation',
                    'Regular monitoring',
                    'Balanced fertilization'
                ],
                'cost_estimate': {'mild': 400, 'moderate': 1200, 'severe': 2500}
            },
            
            'rust_disease': {
                'name': 'Rust Disease',
                'crops_affected': ['Wheat', 'Corn', 'Coffee', 'Beans'],
                'symptoms': ['Orange/brown pustules on leaves', 'Yellowing leaves', 'Reduced photosynthesis'],
                'causes': ['Rust fungi', 'Moderate temperatures', 'High moisture'],
                'severity_indicators': {
                    'mild': 'Few pustules on lower leaves',
                    'moderate': 'Pustules on middle leaves, some yellowing',
                    'severe': 'Extensive pustules, significant yellowing'
                },
                'treatments': {
                    'mild': ['Preventive fungicide spray', 'Remove infected leaves', 'Monitor spread'],
                    'moderate': ['Triazole fungicides', 'Bi-weekly applications', 'Enhanced monitoring'],
                    'severe': ['Emergency fungicide program', 'Consider replanting', 'Quarantine measures']
                },
                'prevention': [
                    'Use rust-resistant varieties',
                    'Timely planting',
                    'Proper field sanitation',
                    'Monitor weather conditions',
                    'Balanced nutrition'
                ],
                'cost_estimate': {'mild': 600, 'moderate': 1800, 'severe': 3500}
            },
            
            'viral_mosaic': {
                'name': 'Viral Mosaic',
                'crops_affected': ['Tobacco', 'Tomato', 'Cucumber', 'Pepper'],
                'symptoms': ['Mosaic pattern on leaves', 'Stunted growth', 'Malformed fruits'],
                'causes': ['Viral infection', 'Insect vectors (aphids)', 'Contaminated tools'],
                'severity_indicators': {
                    'mild': 'Light mosaic on few leaves',
                    'moderate': 'Visible mosaic, slight stunting',
                    'severe': 'Severe mosaic, significant stunting'
                },
                'treatments': {
                    'mild': ['Remove infected plants', 'Control insect vectors', 'Tool sterilization'],
                    'moderate': ['Intensive vector control', 'Quarantine affected area', 'Remove all infected plants'],
                    'severe': ['Destroy entire crop if >30% infected', 'Soil treatment', 'Extended quarantine']
                },
                'prevention': [
                    'Use virus-free seeds/seedlings',
                    'Control aphid populations',
                    'Sterilize tools between plants',
                    'Remove weed hosts',
                    'Use reflective mulches'
                ],
                'cost_estimate': {'mild': 1000, 'moderate': 2500, 'severe': 5000}
            }
        }
        
        # Nutrient deficiency symptoms (often confused with diseases)
        self.nutrient_deficiencies = {
            'nitrogen_deficiency': {
                'name': 'Nitrogen Deficiency',
                'symptoms': ['Yellowing of older leaves', 'Stunted growth', 'Poor yield'],
                'treatment': 'Apply nitrogen fertilizer (Urea 20-30 kg/acre)',
                'cost': 800
            },
            'potassium_deficiency': {
                'name': 'Potassium Deficiency', 
                'symptoms': ['Brown leaf edges', 'Weak stems', 'Poor fruit quality'],
                'treatment': 'Apply potassium fertilizer (MOP 15-20 kg/acre)',
                'cost': 600
            }
        }
    
    def analyze_image(self, image_data, crop_type="Unknown", location="Unknown"):
        """
        Simulate AI analysis of crop disease image.
        In production, this would use a trained CNN model.
        """
        
        # Simulate image processing time
        import time
        time.sleep(1)
        
        # Simulate disease detection based on common patterns
        detected_diseases = self._simulate_disease_detection(crop_type)
        
        # Generate comprehensive analysis report
        analysis_report = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'crop_type': crop_type,
            'location': location,
            'image_quality': self._assess_image_quality(),
            'diseases_detected': detected_diseases,
            'confidence_score': round(random.uniform(0.75, 0.95), 2),
            'environmental_factors': self._assess_environmental_risk(crop_type),
            'urgency_level': self._calculate_urgency(detected_diseases)
        }
        
        return analysis_report
    
    def _simulate_disease_detection(self, crop_type):
        """Simulate realistic disease detection based on crop type and season."""
        
        # Common diseases by crop type
        crop_disease_mapping = {
            'Rice': ['leaf_spot', 'bacterial_blight'],
            'Wheat': ['rust_disease', 'powdery_mildew', 'leaf_spot'],
            'Cotton': ['bacterial_blight', 'leaf_spot'],
            'Tomato': ['leaf_spot', 'bacterial_blight', 'viral_mosaic'],
            'Potato': ['leaf_spot'],
            'Corn': ['rust_disease'],
            'Unknown': ['leaf_spot', 'powdery_mildew']
        }
        
        possible_diseases = crop_disease_mapping.get(crop_type, crop_disease_mapping['Unknown'])
        
        # Randomly select 1-2 diseases (simulate real detection)
        num_diseases = random.choices([0, 1, 2], weights=[10, 70, 20])[0]
        
        if num_diseases == 0:
            return [{'disease_id': 'healthy', 'name': 'No Disease Detected', 'severity': 'none', 'confidence': 0.9}]
        
        detected = []
        selected_diseases = random.sample(possible_diseases, min(num_diseases, len(possible_diseases)))
        
        for disease_id in selected_diseases:
            if disease_id in self.disease_database:
                severity = random.choices(['mild', 'moderate', 'severe'], weights=[50, 35, 15])[0]
                detected.append({
                    'disease_id': disease_id,
                    'name': self.disease_database[disease_id]['name'],
                    'severity': severity,
                    'confidence': round(random.uniform(0.7, 0.95), 2)
                })
        
        return detected
    
    def _assess_image_quality(self):
        """Assess the quality of the uploaded image."""
        quality_scores = ['Excellent', 'Good', 'Fair', 'Poor']
        quality = random.choices(quality_scores, weights=[20, 50, 25, 5])[0]
        
        quality_feedback = {
            'Excellent': 'Perfect lighting and focus for accurate analysis',
            'Good': 'Good image quality, analysis highly reliable', 
            'Fair': 'Acceptable quality, consider retaking in better light',
            'Poor': 'Poor image quality may affect accuracy - please retake'
        }
        
        return {
            'score': quality,
            'feedback': quality_feedback[quality]
        }
    
    def _assess_environmental_risk(self, crop_type):
        """Assess environmental factors affecting disease risk."""
        current_month = datetime.now().month
        
        # Simulate seasonal risk factors
        risk_factors = []
        
        if current_month in [6, 7, 8, 9]:  # Monsoon season
            risk_factors.extend(['High humidity', 'Excessive moisture', 'Poor drainage'])
        elif current_month in [10, 11, 12, 1]:  # Post-monsoon/winter
            risk_factors.extend(['Temperature fluctuation', 'Dew formation'])
        else:  # Summer
            risk_factors.extend(['Heat stress', 'Drought conditions'])
        
        return {
            'season': 'Monsoon' if current_month in [6,7,8,9] else 'Winter' if current_month in [10,11,12,1] else 'Summer',
            'risk_factors': risk_factors,
            'risk_level': random.choice(['Low', 'Medium', 'High'])
        }
    
    def _calculate_urgency(self, diseases):
        """Calculate urgency level based on detected diseases."""
        if not diseases or diseases[0]['disease_id'] == 'healthy':
            return 'None'
        
        max_severity = max([d.get('severity', 'mild') for d in diseases])
        
        urgency_map = {
            'mild': 'Low',
            'moderate': 'Medium', 
            'severe': 'High'
        }
        
        return urgency_map.get(max_severity, 'Low')
    
    def get_treatment_plan(self, disease_id, severity, crop_type):
        """Get detailed treatment plan for detected disease."""
        
        if disease_id == 'healthy' or disease_id not in self.disease_database:
            return {
                'immediate_actions': ['Continue regular monitoring', 'Maintain good field hygiene'],
                'treatments': [],
                'timeline': 'No treatment needed',
                'cost_estimate': 0,
                'success_rate': 100
            }
        
        disease = self.disease_database[disease_id]
        treatments = disease['treatments'].get(severity, disease['treatments']['mild'])
        cost = disease['cost_estimate'].get(severity, 500)
        
        # Generate timeline based on severity
        timeline_map = {
            'mild': '1-2 weeks',
            'moderate': '2-4 weeks', 
            'severe': '4-6 weeks'
        }
        
        success_rates = {
            'mild': random.randint(85, 95),
            'moderate': random.randint(70, 85),
            'severe': random.randint(50, 70)
        }
        
        return {
            'immediate_actions': treatments[:2],
            'treatments': treatments,
            'timeline': timeline_map.get(severity, '2-3 weeks'),
            'cost_estimate': cost,
            'success_rate': success_rates.get(severity, 75),
            'follow_up': 'Monitor weekly and document progress'
        }
    
    def get_prevention_strategies(self, crop_type, location="Unknown"):
        """Get comprehensive prevention strategies for crop health."""
        
        # Generic prevention strategies
        general_strategies = [
            '🌱 **Seed Selection**: Use certified, disease-resistant varieties',
            '🚰 **Water Management**: Implement proper irrigation scheduling', 
            '🧹 **Field Sanitation**: Remove crop debris and weeds regularly',
            '🔄 **Crop Rotation**: Follow 2-3 year rotation with non-host crops',
            '⚖️ **Balanced Nutrition**: Maintain optimal NPK levels',
            '🔍 **Regular Monitoring**: Weekly field inspections for early detection',
            '🛡️ **Integrated Pest Management**: Use biological and chemical controls wisely',
            '📅 **Timely Operations**: Follow recommended planting and harvesting schedules'
        ]
        
        # Crop-specific strategies
        crop_specific = {
            'Rice': [
                '💧 Maintain proper water levels in fields',
                '🌾 Use short-duration varieties in disease-prone areas',
                '🦆 Consider duck farming for integrated pest control'
            ],
            'Wheat': [
                '❄️ Follow recommended sowing dates to avoid rust',
                '💨 Ensure proper air circulation between plants',
                '🌡️ Monitor weather for rust-favorable conditions'
            ],
            'Cotton': [
                '🐛 Implement bollworm management strategies',
                '🌿 Use trap crops around main cotton fields',
                '💧 Avoid water stress during flowering'
            ]
        }
        
        strategies = general_strategies.copy()
        if crop_type in crop_specific:
            strategies.extend(crop_specific[crop_type])
        
        return {
            'general_strategies': general_strategies,
            'crop_specific': crop_specific.get(crop_type, []),
            'seasonal_calendar': self._generate_seasonal_calendar(crop_type),
            'monitoring_checklist': self._generate_monitoring_checklist()
        }
    
    def _generate_seasonal_calendar(self, crop_type):
        """Generate seasonal disease management calendar."""
        calendar = {
            'Pre-Planting (15-30 days before)': [
                'Soil treatment with beneficial microbes',
                'Field preparation and debris removal',
                'Seed treatment with fungicides'
            ],
            'Planting Stage (0-15 days)': [
                'Use certified disease-free seeds',
                'Optimal spacing for air circulation',
                'Soil moisture management'
            ],
            'Vegetative Stage (15-45 days)': [
                'Weekly disease monitoring',
                'Balanced fertilizer application',
                'Preventive fungicide sprays if needed'
            ],
            'Reproductive Stage (45-75 days)': [
                'Intensive monitoring for diseases',
                'Water stress management',
                'Targeted disease control measures'
            ],
            'Maturity & Harvest (75+ days)': [
                'Pre-harvest disease assessment',
                'Proper harvesting techniques',
                'Post-harvest field sanitation'
            ]
        }
        
        return calendar
    
    def _generate_monitoring_checklist(self):
        """Generate weekly monitoring checklist."""
        return [
            '👀 **Visual Inspection**: Check for spots, lesions, or unusual coloration',
            '🍃 **Leaf Health**: Examine both upper and lower leaf surfaces',
            '🌿 **Plant Vigor**: Assess overall plant health and growth',
            '💧 **Moisture Conditions**: Check soil moisture and drainage',
            '🌡️ **Weather Monitoring**: Track temperature and humidity',
            '📸 **Photo Documentation**: Record suspicious symptoms',
            '📝 **Record Keeping**: Document findings and actions taken',
            '🔄 **Treatment Follow-up**: Monitor effectiveness of treatments'
        ]
    
    def generate_expert_consultation_request(self, analysis_report):
        """Generate a structured request for expert consultation."""
        
        diseases = analysis_report['diseases_detected']
        severe_diseases = [d for d in diseases if d.get('severity') == 'severe']
        
        consultation_needed = (
            len(severe_diseases) > 0 or
            analysis_report['urgency_level'] == 'High' or
            analysis_report['confidence_score'] < 0.8
        )
        
        if not consultation_needed:
            return {'needed': False, 'message': 'Current analysis sufficient for management'}
        
        expert_request = {
            'needed': True,
            'priority': 'High' if severe_diseases else 'Medium',
            'summary': f"Disease detected in {analysis_report['crop_type']} crop",
            'key_concerns': [
                f"Detected: {', '.join([d['name'] for d in diseases])}",
                f"Severity: {', '.join([d['severity'] for d in diseases])}",
                f"Confidence: {analysis_report['confidence_score']}"
            ],
            'questions_for_expert': [
                'Please confirm the disease identification',
                'Are the recommended treatments appropriate?',
                'Any additional management strategies needed?',
                'Prevention measures for future crops?'
            ],
            'estimated_consultation_fee': random.randint(500, 1500),
            'recommended_expert_types': ['Plant Pathologist', 'Agricultural Extension Officer']
        }
        
        return expert_request