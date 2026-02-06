import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for voice recognition using Web Speech API
 * @param {Object} options - Configuration options
 * @param {string} options.language - Language code (e.g., 'en-IN', 'hi-IN')
 * @param {Function} options.onResult - Callback when speech is recognized
 * @param {Function} options.onError - Callback when error occurs
 * @returns {Object} Voice recognition state and controls
 */
const useVoiceRecognition = ({ language = 'en-IN', onResult, onError } = {}) => {
    const [isListening, setIsListening] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const [transcript, setTranscript] = useState('');
    const recognitionRef = useRef(null);
    const isStartingRef = useRef(false);
    const isStoppingRef = useRef(false);
    const onResultRef = useRef(onResult);
    const onErrorRef = useRef(onError);

    // Update refs when callbacks change (avoiding useEffect dependency issues)
    useEffect(() => {
        onResultRef.current = onResult;
        onErrorRef.current = onError;
    }, [onResult, onError]);

    // Check browser support and initialize recognition (only once)
    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        setIsSupported(!!SpeechRecognition);

        if (SpeechRecognition && !recognitionRef.current) {
            recognitionRef.current = new SpeechRecognition();
            const recognition = recognitionRef.current;

            // Configuration
            recognition.continuous = true; // Keep listening until manually stopped
            recognition.interimResults = true; // Show real-time transcription
            recognition.maxAlternatives = 1;
            recognition.lang = language;

            // Event handlers
            recognition.onstart = () => {
                console.log('✅ Speech recognition started');
                setIsListening(true);
                setTranscript('');
                isStartingRef.current = false;
            };

            recognition.onresult = (event) => {
                // Get the latest result
                const results = event.results;
                const latestResult = results[results.length - 1];
                const transcript = latestResult[0].transcript;
                const isFinal = latestResult.isFinal;
                
                console.log(isFinal ? '✅ Final result:' : '⏳ Interim result:', transcript);
                setTranscript(transcript);
                
                // Only call onResult for final results
                if (isFinal && onResultRef.current) {
                    onResultRef.current(transcript);
                }
            };

            recognition.onerror = (event) => {
                console.error('❌ Speech recognition error:', event.error);
                setIsListening(false);
                isStartingRef.current = false;
                
                // Ignore aborted errors (happens on rapid clicks or manual stop)
                if (event.error === 'aborted') {
                    console.warn('Speech recognition was aborted');
                    return;
                }

                // Handle different error types
                let errorMessage = '';
                switch (event.error) {
                    case 'no-speech':
                        errorMessage = 'No speech detected. Please try again.';
                        break;
                    case 'audio-capture':
                        errorMessage = 'Microphone not found. Please check your device.';
                        break;
                    case 'not-allowed':
                        errorMessage = 'Microphone access denied. Please allow permissions.';
                        break;
                    case 'network':
                        errorMessage = 'Network error. Please check your connection.';
                        break;
                    default:
                        errorMessage = 'Voice recognition failed. Please try again.';
                }
                
                if (onErrorRef.current) {
                    onErrorRef.current(errorMessage);
                }
            };

            recognition.onend = () => {
                console.log('ℹ️ Speech recognition ended');
                // Only update state if we're not manually stopping
                if (!isStoppingRef.current) {
                    setIsListening(false);
                }
                isStartingRef.current = false;
                isStoppingRef.current = false;
            };
        }

        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.abort();
            }
        };
    }, []); // Empty dependency - only run once

    // Update language when changed
    useEffect(() => {
        if (recognitionRef.current) {
            recognitionRef.current.lang = language;
            console.log('🌍 Language updated to:', language);
        }
    }, [language]);

    const startListening = useCallback(() => {
        console.log('🎤 startListening called', { 
            isSupported, 
            isListening, 
            isStarting: isStartingRef.current,
            hasRecognition: !!recognitionRef.current 
        });
        
        // Prevent rapid clicking
        if (isStartingRef.current || isListening) {
            console.warn('⚠️ Already starting or listening, ignoring...');
            return;
        }
        
        if (!isSupported) {
            console.error('❌ Speech recognition not supported');
            if (onErrorRef.current) {
                onErrorRef.current('Speech recognition not supported in this browser');
            }
            return;
        }

        if (!recognitionRef.current) {
            console.error('❌ Recognition object not initialized');
            return;
        }

        isStartingRef.current = true;
        
        try {
            console.log('🚀 Starting speech recognition...');
            recognitionRef.current.start();
        } catch (error) {
            console.error('❌ Error starting recognition:', error);
            isStartingRef.current = false;
            
            // Ignore "already started" errors
            if (error.name === 'InvalidStateError') {
                console.warn('⚠️ Recognition already started, ignoring');
                return;
            }
            
            if (onErrorRef.current) {
                onErrorRef.current('Unable to start voice recognition. Please try again.');
            }
        }
    }, [isSupported, isListening]);

    const stopListening = useCallback(() => {
        if (recognitionRef.current && isListening) {
            console.log('⏹️ Stopping speech recognition...');
            isStoppingRef.current = true;
            setIsListening(false); // Immediately clear listening state
            setTranscript(''); // Clear transcript
            recognitionRef.current.stop();
            isStartingRef.current = false;
        }
    }, [isListening]);

    const abortListening = useCallback(() => {
        if (recognitionRef.current) {
            console.log('🛑 Aborting speech recognition...');
            isStoppingRef.current = true;
            recognitionRef.current.abort();
            setIsListening(false);
            setTranscript('');
            isStartingRef.current = false;
        }
    }, []);

    return {
        isListening,
        isSupported,
        transcript,
        startListening,
        stopListening,
        abortListening
    };
};

export default useVoiceRecognition;
