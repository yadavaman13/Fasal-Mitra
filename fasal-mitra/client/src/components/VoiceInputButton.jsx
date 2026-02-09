import React from 'react';
import { Mic, Square } from 'lucide-react';
import '../styles/voice-input.css';

/**
 * Voice Input Button Component
 * 
 * Displays a microphone button to start voice recognition
 * Shows a stop button when actively listening
 */
const VoiceInputButton = ({ 
    isListening, 
    isSupported, 
    onStartListening,
    onStopListening, 
    disabled = false 
}) => {
    if (!isSupported) {
        return null; // Don't show button if not supported
    }

    const handleClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        if (disabled) return;
        
        if (isListening && onStopListening) {
            onStopListening();
        } else if (!isListening && onStartListening) {
            onStartListening();
        }
    };

    return (
        <button
            type="button"
            onClick={handleClick}
            disabled={disabled}
            className={`voice-input-btn ${isListening ? 'listening recording' : ''}`}
            aria-label={isListening ? "Stop recording" : "Click to speak"}
            title={isListening ? "Stop recording" : "Click to speak"}
        >
            {isListening ? (
                <>
                    <Square className="voice-icon stop-icon" />
                    <span className="listening-pulse"></span>
                </>
            ) : (
                <Mic className="voice-icon" />
            )}
        </button>
    );
};

export default VoiceInputButton;
