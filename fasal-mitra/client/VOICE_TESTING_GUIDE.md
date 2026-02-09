# 🧪 Voice Feature Testing Guide

## Prerequisites
- ✅ Chrome or Edge browser (Recommended)
- ✅ Working microphone
- ✅ Dev server running on http://localhost:5173

## Quick Test Steps

### Test 1: Voice Input (Basic)
1. Open http://localhost:5173 in Chrome
2. Click the FasalMitra chatbot icon (bottom-right)
3. Click the 🎤 microphone button
4. **Allow microphone permission** when prompted
5. Speak clearly: "What is crop rotation?"
6. Wait 1-2 seconds
7. ✅ Expected: Text appears in input, auto-sends

### Test 2: Voice Output
1. In the chatbot, click the 🔊 speaker icon
2. ✅ Icon should become filled (Volume2)
3. Ask any question (type or voice)
4. ✅ Expected: Hear AI response read aloud
5. Click 🔊 again to disable

### Test 3: Error Handling
1. Click microphone without speaking
2. ✅ Expected: "No speech detected" error (auto-clears in 3 seconds)
3. Deny microphone permission
4. ✅ Expected: "Microphone access denied" error
5. Try clicking mic again after allowing permission
6. ✅ Expected: Works normally

### Test 4: Field Help Modal
1. Go to "Yield Prediction" page
2. Click **?** icon next to "Crop" field
3. Modal opens with voice buttons
4. Test mic and speaker same as above
5. ✅ Expected: Same functionality as main chatbot

### Test 5: Visual Feedback
1. Click microphone
2. ✅ Check for:
   - "Listening..." message appears
   - Mic icon changes to MicOff
   - Button has green background
   - Ripple animation visible
   - Input field disabled

### Test 6: Mobile Testing (Optional)
1. Open on Android Chrome
2. Test voice features
3. ✅ Expected: Works same as desktop
4. iOS Safari: Limited support (voice output only)

## Common Issues & Solutions

### Issue: "Voice recognition failed"
**Solution:**
- Ensure using Chrome or Edge
- Check microphone permissions in browser settings
- Click lock icon → Microphone → Allow
- Refresh page

### Issue: No microphone button visible
**Solution:**
- Browser doesn't support Web Speech API
- Use Chrome or Edge
- Check console for errors

### Issue: Permission denied error
**Solution:**
1. Click lock icon in address bar
2. Set Microphone to "Allow"
3. Refresh page
4. Try microphone again

### Issue: Voice stops immediately
**Solution:**
- Speak clearly and continuously
- Reduce background noise
- Check microphone is working (Settings → Sound → Test)

### Issue: No audio from AI response
**Solution:**
- Check system volume
- Ensure speaker icon is filled (active)
- Try different browser
- Check speaker/headphone connection

## Browser Console Checks

### Open Browser Console
- Press F12 or Right-click → Inspect
- Go to "Console" tab

### What to Look For
✅ **No red errors** related to voice
✅ See: "Speech recognition error: [type]" for debugging
✅ Check network tab for chatbot API calls

### Expected Console Logs
```
Starting voice recognition...
Speech recognized: "your question"
Sending to chatbot API...
Response received
Speaking response...
```

## Feature Checklist

### Voice Input ✅
- [ ] Mic button appears
- [ ] Click activates listening
- [ ] "Listening..." message shows
- [ ] Mic icon changes to MicOff
- [ ] Green background when active
- [ ] Ripple animation visible
- [ ] Speech converts to text
- [ ] Text appears in input field
- [ ] Auto-sends after 300ms
- [ ] Errors clear after 3 seconds

### Voice Output ✅
- [ ] Speaker button appears
- [ ] Click toggles voice output
- [ ] Icon changes when enabled (filled)
- [ ] AI responses speak aloud
- [ ] Can stop by clicking again
- [ ] Natural voice quality
- [ ] Correct language (English)

### Error Handling ✅
- [ ] "No speech detected" - clears in 3s
- [ ] "Microphone access denied" - clear message
- [ ] "Microphone not found" - helpful
- [ ] "Network error" - appropriate
- [ ] Errors don't persist forever
- [ ] Can retry after error

### Visual Polish ✅
- [ ] Animations smooth
- [ ] Colors match theme (#99BC85)
- [ ] Responsive on mobile
- [ ] Icons scale properly
- [ ] Feedback messages clear
- [ ] Layout doesn't break

## Performance Checks

### Speed
- Voice recognition: < 2 seconds ✅
- Text-to-speech: Instant ✅
- No lag in UI ✅

### Memory
- No memory leaks ✅
- Cleanup on unmount ✅
- Efficient re-renders ✅

## Success Criteria

### ✅ PASS if:
1. Can speak a question and get AI response
2. Can hear AI response when voice output enabled
3. Errors are clear and auto-dismiss
4. Works in ChatbotWidget AND FieldHelpModal
5. No console errors
6. Animations are smooth
7. Mobile responsive

### ❌ FAIL if:
1. Microphone button doesn't appear (Chrome/Edge)
2. Speech not recognized consistently
3. Errors persist forever
4. Voice output doesn't play
5. Console shows errors
6. Layout breaks on mobile

## Advanced Testing

### Multi-Language (Optional)
Currently set to 'en-IN'. To test Hindi:
1. Edit ChatbotWidget.jsx
2. Change: `const [voiceLanguage, setVoiceLanguage] = useState('hi-IN');`
3. Speak in Hindi
4. Check recognition accuracy

### Stress Testing
1. Click mic rapidly 10 times
2. ✅ Should not crash
3. Speak very long questions
4. ✅ Should handle gracefully

### Edge Cases
1. Empty speech (silence)
2. Background noise
3. Multiple users speaking
4. Very fast speech
5. Very slow speech

## Debugging Commands

### Check Browser Support
```javascript
// Paste in browser console
console.log('SpeechRecognition:', !!(window.SpeechRecognition || window.webkitSpeechRecognition));
console.log('SpeechSynthesis:', !!window.speechSynthesis);
```

### Test Voice Directly
```javascript
// Test TTS
speechSynthesis.speak(new SpeechSynthesisUtterance('Hello farmer!'));

// Check voices
console.log(speechSynthesis.getVoices());
```

## Report Template

### Test Report
```
Date: ___________
Browser: ___________
OS: ___________

Voice Input: ☐ Pass ☐ Fail
Voice Output: ☐ Pass ☐ Fail
Error Handling: ☐ Pass ☐ Fail
Visual Feedback: ☐ Pass ☐ Fail
Mobile: ☐ Pass ☐ Fail ☐ N/A

Issues Found:
1. ___________
2. ___________

Notes:
___________
```

## Next Steps After Testing

### If All Tests Pass ✅
- Mark feature as production-ready
- Update README with voice features
- Train users on voice usage
- Monitor usage analytics

### If Tests Fail ❌
- Document specific failures
- Check browser console for errors
- Review error messages
- Test in different browser
- Check microphone hardware

## Support Resources

- **Browser Console**: F12 → Console tab
- **Microphone Settings**: Browser Settings → Privacy → Microphone
- **Documentation**: See VOICE_FEATURE_DOCUMENTATION.md
- **Quick Start**: See VOICE_QUICK_START.md

---

**Testing Time Estimate:** 10-15 minutes for full test suite

**Ready to test! 🚀**
