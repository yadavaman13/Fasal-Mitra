import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook for text-to-speech using Web Speech API
 * @param {Object} options - Configuration options
 * @param {string} options.language - Language code (e.g., 'en-IN', 'hi-IN')
 * @param {number} options.rate - Speech rate (0.5 to 2, default 1)
 * @param {number} options.pitch - Speech pitch (0 to 2, default 1)
 * @param {number} options.volume - Speech volume (0 to 1, default 1)
 * @returns {Object} Text-to-speech state and controls
 */
const useTextToSpeech = ({ 
    language = 'en-IN', 
    rate = 1, 
    pitch = 1, 
    volume = 1 
} = {}) => {
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const [voices, setVoices] = useState([]);
    const utteranceRef = useRef(null);

    // Check browser support
    useEffect(() => {
        const synth = window.speechSynthesis;
        setIsSupported(!!synth);

        if (synth) {
            // Load available voices
            const loadVoices = () => {
                const availableVoices = synth.getVoices();
                setVoices(availableVoices);
            };

            loadVoices();

            // Chrome loads voices asynchronously
            if (synth.onvoiceschanged !== undefined) {
                synth.onvoiceschanged = loadVoices;
            }
        }

        return () => {
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        };
    }, []);

    const speak = (text) => {
        if (!isSupported || !text) {
            return;
        }

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utteranceRef.current = utterance;

        // Configuration
        utterance.lang = language;
        utterance.rate = rate;
        utterance.pitch = pitch;
        utterance.volume = volume;

        // Try to find a voice matching the language
        const preferredVoice = voices.find(voice => voice.lang.startsWith(language.split('-')[0]));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        // Event handlers
        utterance.onstart = () => {
            setIsSpeaking(true);
        };

        utterance.onend = () => {
            setIsSpeaking(false);
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            setIsSpeaking(false);
        };

        // Speak
        window.speechSynthesis.speak(utterance);
    };

    const stop = () => {
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
        }
    };

    const pause = () => {
        if (window.speechSynthesis && isSpeaking) {
            window.speechSynthesis.pause();
        }
    };

    const resume = () => {
        if (window.speechSynthesis) {
            window.speechSynthesis.resume();
        }
    };

    return {
        speak,
        stop,
        pause,
        resume,
        isSpeaking,
        isSupported,
        voices
    };
};

export default useTextToSpeech;
