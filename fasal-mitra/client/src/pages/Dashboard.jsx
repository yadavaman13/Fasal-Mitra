import React from 'react';
import { Sprout, Beaker, Bug, TrendingUp } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import { WeatherDashboard } from '../components/weather';
import ChatbotWidget from '../components/ChatbotWidget';
import '../styles/dashboard.css';

const Dashboard = () => {
    const features = [
        {
            icon: Sprout,
            title: 'Crop Yield',
            description: 'Predict how much your crops will produce this season using smart technology.',
            path: '/yield-prediction',
        },
        {
            icon: Beaker,
            title: 'Soil Check',
            description: 'Test your soil and get recommendations for better crop growth.',
            path: '/soil-analysis',
        },
        {
            icon: Bug,
            title: 'Disease Help',
            description: 'Take crop photos to identify diseases and get treatment advice.',
            path: '/disease-detection',
        },
        {
            icon: TrendingUp,
            title: 'Improve Farm',
            description: 'Compare your farm performance and find ways to grow more.',
            path: '/gap-analysis',
        },
    ];

    return (
        <div className="dashboard-container">
            {/* Main Content - Weather + Features */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="dashboard-main-layout">
                    {/* Left - Weather Section */}
                    <div className="dashboard-weather-section">
                        <WeatherDashboard />
                    </div>
                    
                    {/* Right - Features Section */}
                    <div className="dashboard-features-section">
                        <div className="features-header">
                            <h2 className="features-title">
                                Farm Tools
                            </h2>
                            <p className="features-subtitle">
                                Smart tools for better farming
                            </p>
                        </div>

                        <div className="features-grid">
                            {features.map((feature, index) => (
                                <FeatureCard
                                    key={index}
                                    icon={feature.icon}
                                    title={feature.title}
                                    description={feature.description}
                                    path={feature.path}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Section */}
            <div className="bg-white border-t border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
                        <div>
                            <div className="dashboard-stats-value">55+</div>
                            <div className="dashboard-stats-label">Crops Supported</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">30+</div>
                            <div className="dashboard-stats-label">States Covered</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">97.5%</div>
                            <div className="dashboard-stats-label">ML Accuracy</div>
                        </div>
                        <div>
                            <div className="dashboard-stats-value">24/7</div>
                            <div className="dashboard-stats-label">AI Support</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Chatbot Widget */}
            <ChatbotWidget />
        </div>
    );
};

export default Dashboard;
