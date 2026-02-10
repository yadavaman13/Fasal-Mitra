import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Bug, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import ImageUpload from '../components/disease/ImageUpload';
import DetectionResults from '../components/disease/DetectionResults';
import TreatmentPlan from '../components/disease/TreatmentPlan';
import { VoiceSummary } from '../components/voice';
import '../styles/disease-detection.css';
import '../styles/pages.css';
import '../styles/soil-analysis-clean.css';

const DiseaseDetection = () => {
    const { t } = useTranslation(['pages', 'common']);
    const [selectedImage, setSelectedImage] = useState(null);
    const [cropType, setCropType] = useState('Rice');
    const [location, setLocation] = useState('');
    const [isDetecting, setIsDetecting] = useState(false);
    const [detectionResult, setDetectionResult] = useState(null);
    const [error, setError] = useState(null);

    const cropOptions = [
        'Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato', 'Maize', 'Sugarcane',
        'Soybean', 'Barley', 'Mustard', 'Groundnut', 'Sunflower'
    ];

    const handleImageSelect = (file) => {
        setSelectedImage(file);
        setDetectionResult(null);
        setError(null);
    };

    const handleDetect = async () => {
        if (!selectedImage) {
            setError(t('pages:diseaseDetection.pleaseSelectImage'));
            return;
        }

        setIsDetecting(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedImage);
            formData.append('crop_type', cropType);
            if (location.trim()) {
                formData.append('location', location);
            }

            // Add timeout to prevent hanging forever
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

            const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
            const response = await fetch(`${baseUrl}/api/v1/disease/detect`, {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            const data = await response.json();

            if (data.success) {
                setDetectionResult(data.data);
            } else {
                setError(data.message || 'Detection failed');
            }
        } catch (err) {
            if (err.name === 'AbortError') {
                setError('Request timed out. Please ensure the backend server is running at http://localhost:8000');
            } else if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
                setError('Cannot connect to server. Please start the backend server: cd fasal-mitra/server && python run.py');
            } else {
                setError('Failed to detect disease. Please try again.');
            }
            console.error('Detection error:', err);
        } finally {
            setIsDetecting(false);
        }
    };

    const handleReset = () => {
        setSelectedImage(null);
        setDetectionResult(null);
        setError(null);
        setLocation('');
    };

    return (
        <div className="disease-detection-app">
            <div className="detection-container">
                {/* Minimal Header */}
                <div className="app-header">
                    <div className="header-content">
                        <Bug className="app-icon" />
                        <h1 className="app-title">Disease Detection</h1>
                    </div>
                    <p className="app-subtitle">Upload a plant image for instant AI-powered disease analysis</p>
                </div>

                {/* Main Detection Interface */}
                <div className="detection-interface">
                    {/* Crop Selection */}
                    <div className="form-fields">
                        <div className="form-field">
                            <label className="field-label">
                                Select Crop Type
                            </label>
                            <select
                                value={cropType}
                                onChange={(e) => setCropType(e.target.value)}
                                className="field-input"
                            >
                                {cropOptions.map(crop => (
                                    <option key={crop} value={crop}>
                                        {crop}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Upload Section */}
                    <div className="upload-zone">
                        <ImageUpload
                            onImageSelect={handleImageSelect}
                            selectedImage={selectedImage}
                        />
                    </div>

                    {/* Action Controls */}
                    <div className="control-panel">
                        <button
                            onClick={handleDetect}
                            disabled={!selectedImage || isDetecting}
                            className="detect-button"
                        >
                            {isDetecting ? (
                                <>
                                    <Loader2 className="spin-icon" />
                                    <span>Analyzing...</span>
                                </>
                            ) : (
                                <>
                                    <Bug className="button-icon" />
                                    <span>Detect Disease</span>
                                </>
                            )}
                        </button>

                        {(selectedImage || detectionResult) && (
                            <button
                                onClick={handleReset}
                                className="reset-button"
                            >
                                <span>Reset</span>
                            </button>
                        )}
                    </div>

                    {/* Error Display */}
                    {error && (
                        <div className="error-notification">
                            <AlertCircle className="error-icon" />
                            <span>{error}</span>
                        </div>
                    )}
                </div>

                {/* Results Section */}
                {detectionResult && (
                    <div className="results-panel">
                        {/* Results Header */}
                        <div className="results-header">
                            <div className="results-title">
                                <CheckCircle className="results-icon" />
                                <h2>Analysis Complete</h2>
                            </div>
                        </div>

                        {/* Voice Summary */}
                        <div className="voice-section">
                            <VoiceSummary
                                result={detectionResult}
                                resultType="diseaseDetection"
                                title="Listen to Summary"
                                showTitle={true}
                                compact={false}
                                className="disease-voice-summary"
                            />
                        </div>

                        {/* Results Content */}
                        <div className="results-grid">
                            <DetectionResults result={detectionResult} />
                            <TreatmentPlan 
                                treatmentPlan={detectionResult.treatment_plan}
                                severity={detectionResult.estimated_severity}
                                recommendations={detectionResult.recommendations}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DiseaseDetection;