# 🚀 Quick Start - Disease Detection System

## ⚡ One-Command Start

### Windows:
```powershell
cd fasal-mitra
.\START_DISEASE_DETECTION.bat
```

### Manual Start:

**Terminal 1 - Backend:**
```powershell
cd fasal-mitra\server
python run.py
```

**Terminal 2 - Frontend:**
```powershell
cd fasal-mitra\client
npm run dev
```

---

## 🌐 Access URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## ✅ Test the System

```powershell
# Run comprehensive tests
python fasal-mitra\test_disease_detection.py
```

---

## 🎯 What You Can Do

1. **Upload Plant Images** → Get disease detection
2. **View Treatment Plans** → AI-powered recommendations
3. **Browse Disease Database** → Learn about plant diseases
4. **Access API** → Integrate with other applications

---

## 📚 Documentation

- **Execution Plan**: `DISEASE_DETECTION_EXECUTION_PLAN.md`
- **Complete Guide**: `DISEASE_DETECTION_COMPLETE.md`
- **Hackathon Reference**: `HACKATHON_QUICK_REFERENCE.md`

---

## 🐛 Troubleshooting

### Backend won't start?
```powershell
cd fasal-mitra\server
pip install -r requirements.txt
python run.py
```

### Frontend won't start?
```powershell
cd fasal-mitra\client
npm install
npm run dev
```

### Model not loading?
- Check file exists: `server\app\models\ml\plant_disease_recog_model_pwp.keras`
- Should be ~45MB

---

## 🎓 For Hackathon Judges

**Quick Demo**: Upload any plant leaf image → Get instant disease detection with AI-powered treatment advice

**Tech Stack**:
- Frontend: React 18 + Vite
- Backend: FastAPI (Python)
- ML: TensorFlow/Keras (39 disease classes)
- AI: Google Gemini API (optional)

**Key Features**:
- ✅ Real ML model (not hardcoded)
- ✅ Production-ready architecture
- ✅ AI-powered personalized advice
- ✅ Mobile-responsive UI
- ✅ Comprehensive error handling

---

**Need help?** Check the documentation files or visit http://localhost:8000/docs
