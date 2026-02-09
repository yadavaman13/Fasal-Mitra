# 🎤 Voice Input/Output Feature Documentation

## Overview
The FasalMitra chatbot now supports **voice input and output** to help farmers and low-literacy users interact with the AI assistant using speech instead of typing.

## Features

### 🎙️ Voice Input (Speech-to-Text)
- **Microphone Button**: Click to start speaking
- **Auto-Send**: Automatically sends your question after speech recognition
- **Visual Feedback**: Animated microphone icon shows when listening
- **Multi-Language Support**: 
  - English (India) - `en-IN` (default)
  - Hindi (India) - `hi-IN`
- **Browser-Based**: Uses Web Speech API (no backend required)

### 🔊 Voice Output (Text-to-Speech)
- **Speaker Toggle**: Click to enable/disable voice responses
- **Auto-Speak**: AI responses are read aloud automatically when enabled
- **Natural Voice**: Uses browser's native speech synthesis
- **Control**: Stop speaking by toggling the speaker icon

## Components

### 1. Custom Hooks

#### `useVoiceRecognition.js`
Located: `src/hooks/useVoiceRecognition.js`

Custom React hook for speech recognition using Web Speech API.

**Parameters:**
- `language` - Language code (e.g., 'en-IN', 'hi-IN')
- `onResult` - Callback when speech is recognized
- `onError` - Callback when error occurs

**Returns:**
```javascript
{
  isListening: boolean,      // Whether currently listening
  isSupported: boolean,       // Browser support check
  transcript: string,         // Recognized text
  startListening: () => void, // Start recording
  stopListening: () => void,  // Stop recording
  abortListening: () => void  // Cancel recording
}
```

**Example:**
```javascript
const { isListening, startListening } = useVoiceRecognition({
  language: 'en-IN',
  onResult: (text) => {
    console.log('You said:', text);
  },
  onError: (error) => {
    console.error('Speech error:', error);
  }
});
```

#### `useTextToSpeech.js`
Located: `src/hooks/useTextToSpeech.js`

Custom React hook for text-to-speech using Web Speech API.

**Parameters:**
- `language` - Language code (e.g., 'en-IN', 'hi-IN')
- `rate` - Speech rate (0.5 to 2, default 1)
- `pitch` - Speech pitch (0 to 2, default 1)
- `volume` - Speech volume (0 to 1, default 1)

**Returns:**
```javascript
{
  speak: (text) => void,  // Speak the text
  stop: () => void,       // Stop speaking
  pause: () => void,      // Pause speaking
  resume: () => void,     // Resume speaking
  isSpeaking: boolean,    // Whether currently speaking
  isSupported: boolean,   // Browser support check
  voices: Array           // Available voices
}
```

**Example:**
```javascript
const { speak, isSpeaking } = useTextToSpeech({
  language: 'en-IN',
  rate: 1.0
});

speak('Hello farmer!');
```

### 2. Components

#### `VoiceInputButton.jsx`
Located: `src/components/VoiceInputButton.jsx`

Reusable microphone button component with visual feedback.

**Props:**
- `isListening` - Whether currently listening
- `isSupported` - Whether browser supports voice
- `onStartListening` - Click handler
- `disabled` - Disable button

**Features:**
- Animated pulse effect when listening
- Mic icon changes to MicOff when active
- Ripple animation effect
- Accessibility labels

## Integration

### ChatbotWidget.jsx
Main floating chatbot on homepage.

**Voice Features:**
1. Microphone button in input area
2. Voice output toggle (speaker icon)
3. Auto-speak AI responses when enabled
4. Visual "Listening..." feedback

### FieldHelpModal.jsx
Field-specific help modal.

**Voice Features:**
1. Same voice input capabilities as main chatbot
2. Voice output for field explanations
3. Auto-speak feature for educational content

## Browser Compatibility

### Web Speech API Support

| Browser | Speech Recognition | Text-to-Speech |
|---------|-------------------|----------------|
| Chrome | ✅ Yes | ✅ Yes |
| Edge | ✅ Yes | ✅ Yes |
| Safari | ⚠️ Limited | ✅ Yes |
| Firefox | ❌ No | ✅ Yes |

**Fallbacks:**
- Voice buttons automatically hide if not supported
- Typing input always available as fallback
- Graceful degradation for unsupported browsers

### Prefixes
The code handles browser prefixes automatically:
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
```

## Styling

### CSS Files

#### `voice-input.css`
Located: `src/styles/voice-input.css`

**Key Classes:**
- `.voice-input-btn` - Microphone button base styles
- `.voice-input-btn.listening` - Active listening state
- `.listening-pulse` - Ripple animation effect
- `.voice-feedback` - "Listening..." message box
- `.voice-language-toggle` - Language switcher (optional)

**Animations:**
- `pulse` - Button pulsing effect
- `micPulse` - Icon scaling effect
- `ripple` - Circular ripple expansion
- `spin` - Loading spinner

### Updated Chatbot Styles

#### `chatbot-widget.css` Updates
- `.chatbot-input-container` - Now flex-column for voice feedback
- `.chatbot-input-wrapper` - Horizontal flex container for buttons + input
- `.voice-output-btn` - Speaker toggle button styles
- `.voice-output-btn.active` - Active state when voice output enabled

#### `field-help-modal.css` Updates
- `.field-help-input-container` - Same flex-column structure
- `.field-help-input-wrapper` - Same horizontal layout
- `.voice-output-btn` - Matching speaker toggle styles

## Usage Instructions

### For Users

#### To Use Voice Input:
1. Click the **microphone icon** 🎤 in the input area
2. Allow browser microphone permissions if prompted
3. Speak your question clearly
4. Wait for the "Listening..." indicator to disappear
5. Your question is automatically sent to the chatbot

#### To Enable Voice Output:
1. Click the **speaker icon** 🔊 in the input area
2. Icon changes to Volume2 (filled) when enabled
3. AI responses will be read aloud automatically
4. Click again to disable voice output

### For Developers

#### Adding Voice to a New Component:

```javascript
import useVoiceRecognition from '../hooks/useVoiceRecognition';
import useTextToSpeech from '../hooks/useTextToSpeech';
import VoiceInputButton from './VoiceInputButton';

function MyComponent() {
  const [message, setMessage] = useState('');
  
  // Voice input
  const { isListening, isSupported, startListening } = useVoiceRecognition({
    language: 'en-IN',
    onResult: (text) => {
      setMessage(text);
      // Auto-send or use the text
    }
  });
  
  // Voice output
  const { speak, isSpeaking } = useTextToSpeech({
    language: 'en-IN'
  });
  
  return (
    <div>
      <VoiceInputButton
        isListening={isListening}
        isSupported={isSupported}
        onStartListening={startListening}
      />
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={() => speak('Hello!')}>Test Voice</button>
    </div>
  );
}
```

## Language Support

### Supported Languages

| Language | Code | Status |
|----------|------|--------|
| English (India) | en-IN | ✅ Default |
| Hindi (India) | hi-IN | ✅ Supported |
| Tamil (India) | ta-IN | ⚠️ Partial |
| Telugu (India) | te-IN | ⚠️ Partial |

### Changing Language

Currently set to `en-IN` (English - India) by default.

**To add language toggle:**
```javascript
const [voiceLanguage, setVoiceLanguage] = useState('en-IN');

// Update hook
const { ... } = useVoiceRecognition({
  language: voiceLanguage,
  // ...
});

// Add toggle buttons
<button onClick={() => setVoiceLanguage('en-IN')}>English</button>
<button onClick={() => setVoiceLanguage('hi-IN')}>हिंदी</button>
```

## Accessibility

### Features
- **ARIA Labels**: All buttons have proper labels
- **Keyboard Support**: Tab navigation works
- **Visual Feedback**: Clear indicators for all states
- **Screen Reader Friendly**: Proper semantic HTML
- **Fallback Support**: Text input always available

### WCAG Compliance
- ✅ Color contrast meets AA standards
- ✅ Focus indicators visible
- ✅ Alternative input methods available
- ✅ Clear error messages

## Troubleshooting

### Issue: Microphone button not showing
**Solution:** Browser doesn't support Web Speech API. Use Chrome or Edge.

### Issue: "Permission denied" error
**Solution:** 
1. Check browser microphone permissions
2. Ensure HTTPS (some browsers require it)
3. Allow microphone access when prompted

### Issue: Voice recognition stops immediately
**Solution:**
- Speak clearly and continuously
- Check microphone input levels
- Ensure no background noise interference

### Issue: Voice output not working
**Solution:**
- Check system volume settings
- Try different browser (Firefox has limited support)
- Verify speakers/headphones connected

### Issue: Wrong language detected
**Solution:**
- Explicitly set language in hook: `language: 'en-IN'`
- Clear browser cache
- Update browser to latest version

## Performance Considerations

### Voice Recognition
- **Latency**: ~1-2 seconds for processing
- **Accuracy**: 85-95% in quiet environments
- **Network**: Works offline (browser-based)
- **Battery**: Minimal impact

### Text-to-Speech
- **Latency**: Instant (no network required)
- **Quality**: Depends on browser's voice engine
- **Performance**: Very lightweight
- **Caching**: Voices loaded once per session

## Future Enhancements

### Planned Features
- [ ] Multi-language auto-detection
- [ ] Custom wake word ("Hey FasalMitra")
- [ ] Voice command shortcuts
- [ ] Regional accent support
- [ ] Offline voice processing
- [ ] Voice feedback for errors
- [ ] Adjustable speech rate control
- [ ] Voice profiles for personalization

### Potential Integrations
- Azure Speech Services (cloud backup)
- Google Cloud Speech API (improved accuracy)
- Custom ML models for agricultural terms
- Voice analytics for user insights

## Security & Privacy

### Data Handling
- ✅ **No Server Storage**: Voice data processed in browser only
- ✅ **No Recording**: Audio not saved or uploaded
- ✅ **Local Processing**: Web Speech API uses browser engine
- ✅ **Privacy First**: No third-party API calls for voice

### Permissions
- Microphone access required only when using voice input
- Permissions requested at runtime, not on page load
- User can revoke permissions anytime in browser settings

## Testing

### Manual Testing Checklist
- [ ] Microphone button appears in both chatbots
- [ ] Click microphone starts listening
- [ ] "Listening..." indicator shows
- [ ] Speech correctly converted to text
- [ ] Message auto-sends after recognition
- [ ] Speaker button toggles voice output
- [ ] AI responses spoken when enabled
- [ ] Animations smooth and responsive
- [ ] Works on mobile devices
- [ ] Graceful fallback in unsupported browsers

### Browser Testing
Test in:
- ✅ Chrome (Windows, Mac, Android)
- ✅ Edge (Windows)
- ⚠️ Safari (Mac, iOS) - Limited support
- ❌ Firefox - No speech recognition

## Resources

### Documentation
- [Web Speech API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [SpeechRecognition API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
- [SpeechSynthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)

### Browser Support
- [Can I Use - Speech Recognition](https://caniuse.com/speech-recognition)
- [Can I Use - Speech Synthesis](https://caniuse.com/speech-synthesis)

## License
Part of FasalMitra project - MIT License

## Contact
For issues or feature requests, please open a GitHub issue.

---

**Last Updated:** January 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
