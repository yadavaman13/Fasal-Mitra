# 🐛 Voice Feature Debug Guide

## Quick Debugging Steps

### Step 1: Open Browser Console
1. Press **F12** (or Right-click → Inspect)
2. Click on the **Console** tab
3. Keep it open while testing

### Step 2: Click the Microphone Button
- You should see console logs appear:
  - `startListening called { isSupported: true, isListening: false }`
  - `Starting speech recognition...`
  - `✅ Speech recognition started`

### Step 3: Check What You See

#### ✅ **If you see these logs:**
```
startListening called { isSupported: true, isListening: false }
Starting speech recognition...
✅ Speech recognition started
```
**Good!** Voice is working. Now speak and you should see:
```
✅ Speech recognized: "your text here"
```

#### ❌ **If you see:**
```
❌ Speech recognition error: not-allowed
```
**Fix:** Allow microphone permission
1. Click the 🔒 lock icon in address bar
2. Set Microphone → Allow
3. Refresh page (Ctrl+R)
4. Try again

#### ❌ **If you see:**
```
startListening called { isSupported: false, isListening: false }
Speech recognition not supported
```
**Fix:** You're using Firefox or Safari
- Switch to **Chrome** or **Edge**
- Voice recognition only works in these browsers

#### ❌ **If you see:**
```
startListening called { isSupported: true, isListening: true }
Cannot start: { hasRecognition: true, isListening: true }
```
**Fix:** Already listening
- Wait a moment and try again
- Or refresh the page

#### ❌ **If you see nothing in console:**
**Fix:** Check if the button is actually being clicked
1. Add a test: Click the button and see if anything logs
2. Check if the chatbot is actually open
3. Refresh the page completely

### Step 4: Test Microphone Permissions Directly

Open this in console:
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log('✅ Microphone access granted'))
  .catch(err => console.error('❌ Microphone access denied:', err));
```

### Step 5: Test Speech Recognition Directly

Open this in console:
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.onstart = () => console.log('✅ STARTED');
  recognition.onresult = (e) => console.log('✅ RESULT:', e.results[0][0].transcript);
  recognition.onerror = (e) => console.error('❌ ERROR:', e.error);
  recognition.start();
  console.log('Recognition object created and started');
} else {
  console.error('❌ Speech Recognition NOT supported');
}
```

Speak after running this. You should see your text in console.

## Common Fixes

### Fix 1: Refresh the Page
```
Ctrl + Shift + R (Windows)
Cmd + Shift + R (Mac)
```

### Fix 2: Allow Microphone
1. Click 🔒 in address bar
2. Microphone → Allow
3. Refresh page

### Fix 3: Check Browser
- ✅ Use Chrome or Edge
- ❌ Firefox doesn't support speech recognition
- ⚠️ Safari has limited support

### Fix 4: Check HTTPS
Some browsers require HTTPS for microphone access.
If on localhost, it should work.

### Fix 5: Clear Errors
The error banner should auto-clear in 3 seconds now.
If not, click the mic button again.

## What to Report

If it's still not working, copy this from your console:

1. **Browser Info:**
   ```javascript
   navigator.userAgent
   ```

2. **Speech Support:**
   ```javascript
   console.log({
     SpeechRecognition: !!(window.SpeechRecognition || window.webkitSpeechRecognition),
     SpeechSynthesis: !!window.speechSynthesis
   });
   ```

3. **Any Error Messages:**
   - Copy all red errors from console
   - Copy any yellow warnings

4. **Console Logs:**
   - Copy the logs when you click the mic button

## Quick Test Command

Paste this entire block in console and click the mic button:

```javascript
console.clear();
console.log('=== VOICE DEBUG TEST ===');
console.log('Browser:', navigator.userAgent);
console.log('Speech Recognition:', !!(window.SpeechRecognition || window.webkitSpeechRecognition));
console.log('Speech Synthesis:', !!window.speechSynthesis);
console.log('=== Now click the microphone button ===');
```

Then click the mic and send me what appears!

---

**Most Common Issue:** Microphone permission not granted.
**Most Common Fix:** Click lock icon → Allow microphone → Refresh
