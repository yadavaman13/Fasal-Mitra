"""
Chatbot Service

AI-powered farming assistant using Google Gemini API
"""

import os
from typing import Optional, Dict, List
import logging
from functools import lru_cache
from datetime import datetime
import uuid
import time

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Chatbot will use fallback mode.")

from app.config import settings
from app.models.chatbot import (
    ChatbotQueryRequest,
    ExplainTermRequest
)

logger = logging.getLogger(__name__)


class ChatbotService:
    """AI-powered farming chatbot service"""
    
    # Counter-question triggers - questions that need more details from farmer
    COUNTER_QUESTION_TRIGGERS = {
        'yield': {
            'patterns': ['calculate yield', 'estimate yield', 'predict yield', 'yield of my farm', 
                        'how much yield', 'expected yield', 'yield calculation', 'mera yield',
                        'पैदावार', 'उपज', 'ઉપજ', 'விளைச்சல்'],
            'response': """To calculate your farm's yield accurately, I need some details:

**Please provide:**
• 🌾 **Crop name**: What crop are you growing?
• 📏 **Farm area**: What is your farm size (in acres or hectares)?
• 📍 **Location**: Which district/state is your farm in?
• 🌱 **Soil type**: Sandy, loamy, clayey, or black soil?
• 💧 **Irrigation**: Rainfed, drip, sprinkler, or flood irrigation?
• 📅 **Sowing date**: When did you sow the crop?

Share these details and I'll help estimate your yield! 🌾"""
        },
        'fertilizer': {
            'patterns': ['fertilizer dose', 'how much fertilizer', 'fertilizer for my', 
                        'fertilizer calculation', 'fertilizer requirement', 'which fertilizer',
                        'खाद', 'उर्वरक', 'ખાતર', 'உரம்'],
            'response': """To recommend the right fertilizer amount, I need:

**Please share:**
• 🌱 **Crop name**: What are you growing?
• 📏 **Farm area**: How big is your field (acres/hectares)?
• 🧪 **Soil pH**: Do you know your soil pH level? (If not, that's okay)
• 🌿 **Growth stage**: Seedling, vegetative, flowering, or maturity?
• 🔄 **Previous crop**: What did you grow last season?
• 💧 **Irrigation type**: How do you water your crops?

With these details, I'll give you precise fertilizer recommendations! 🌿"""
        },
        'irrigation': {
            'patterns': ['water requirement', 'how much water', 'irrigation schedule', 
                        'when to water', 'watering my', 'irrigation for',
                        'पानी', 'सिंचाई', 'પાણી', 'நீர்'],
            'response': """For proper irrigation guidance, please tell me:

**I need to know:**
• 🌱 **Crop name**: What crop are you growing?
• 🏜️ **Soil type**: Sandy, loamy, or clayey?
• ☀️ **Current weather**: Is it hot, humid, or dry in your area?
• 🌿 **Growth stage**: Seedling, flowering, or maturity?
• 💧 **Current method**: Drip, sprinkler, flood, or rainfed?
• 📍 **Location**: Your district/state?

Share these and I'll create a perfect watering schedule for you! 💧"""
        },
        'pesticide': {
            'patterns': ['which pesticide', 'spray for', 'pest control', 'insect attack', 
                        'disease treatment', 'pest on my', 'insects eating',
                        'कीटनाशक', 'दवाई', 'જંતુનાશક', 'பூச்சிக்கொல்லி'],
            'response': """To recommend the right treatment, I need:

**Please describe:**
• 🌱 **Crop name**: Which crop is affected?
• 🔍 **Symptoms**: What do you see? (spots, wilting, holes, insects?)
• 📊 **Affected area**: How much of the field is affected? (%, or area)
• 🌿 **Crop stage**: Seedling, vegetative, flowering, or fruiting?
• 💊 **Previous treatment**: Have you tried anything already?
• 📷 **Photo**: Can you describe the pest/disease appearance?

Share details or describe symptoms clearly for accurate advice! 🔬"""
        },
        'seed': {
            'patterns': ['how much seed', 'seed rate', 'seed quantity', 'seeds needed', 
                        'seed calculation', 'बीज', 'બીજ', 'விதை'],
            'response': """To calculate seed requirement, please share:

**I need:**
• 🌱 **Crop name**: What do you want to plant?
• 📏 **Farm area**: What is your field size?
• 🌾 **Planting method**: Broadcast, line sowing, or transplanting?
• 🏷️ **Variety**: Which seed variety (if known)?
• 📐 **Spacing**: What row/plant spacing will you use?

I'll calculate the exact seed quantity you need! 🌱"""
        },
        'profit': {
            'patterns': ['profit calculation', 'how much profit', 'calculate profit', 
                        'income from', 'earnings from', 'cost benefit',
                        'मुनाफा', 'लाभ', 'નફો', 'லாபம்'],
            'response': """To estimate your profit, I need:

**Please provide:**
• 🌾 **Crop name**: What are you growing?
• 📏 **Farm area**: How big is your field?
• 💰 **Input costs**: Approximate expenses for seeds, fertilizers, labor, irrigation?
• 📊 **Expected yield**: What yield do you expect (quintal/acre)?
• 🏪 **Market price**: Current selling price in your area (₹/quintal)?

Share these for a detailed profit analysis! 💰"""
        },
        'weather': {
            'patterns': ['weather for my', 'rain forecast', 'when will it rain', 
                        'weather in my area', 'मौसम', 'હવામાન', 'வானிலை'],
            'response': """For accurate weather information, please tell me:

**I need:**
• 📍 **Location**: Your district and state?
• 🌾 **Crop (optional)**: What are you growing? (for crop-specific advice)
• 📅 **Planning for**: Next few days or seasonal forecast?

Share your location and I'll provide weather updates! ☀️🌧️"""
        }
    }
    
    def __init__(self):
        self.enabled = False
        self.model = None
        self.last_request_time = None
        self.min_request_interval = 2  # seconds between requests
        self.response_cache = {}  # Cache for consistent responses
        self.cache_max_size = 200  # Maximum cache entries
        
        # Generation config for consistent responses (temperature=0 = deterministic)
        self.generation_config = None
        if GEMINI_AVAILABLE:
            self.generation_config = genai.types.GenerationConfig(
                temperature=0,  # Zero temperature for deterministic/consistent responses
                top_p=1,
                top_k=1,
                max_output_tokens=800
            )
        
        # Initialize Gemini if available
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                # Using Gemini Flash Latest (best balance of speed and quota)
                self.model = genai.GenerativeModel('gemini-flash-latest')
                self.enabled = True
                logger.info("✅ Gemini API configured successfully with gemini-flash-latest (temperature=0 for consistency)")
            except Exception as e:
                logger.error(f"Error configuring Gemini API: {str(e)}")
                self.enabled = False
        else:
            logger.warning("Chatbot disabled - Gemini API key not configured")
    
    def _check_counter_question(self, question: str) -> Optional[str]:
        """Check if the question requires counter-questions for more details"""
        question_lower = question.lower()
        
        for trigger_type, trigger_data in self.COUNTER_QUESTION_TRIGGERS.items():
            for pattern in trigger_data['patterns']:
                if pattern.lower() in question_lower:
                    logger.info(f"Counter-question triggered for: {trigger_type}")
                    return trigger_data['response']
        
        return None
    
    def _get_cache_key(self, question: str, language: str) -> str:
        """Generate cache key from question and language"""
        # Normalize the question for caching
        normalized = question.lower().strip()
        return f"{language}:{normalized}"
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Get cached response if available"""
        if cache_key in self.response_cache:
            logger.info(f"Cache hit for question")
            return self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: str):
        """Cache a response for future use"""
        # Limit cache size
        if len(self.response_cache) >= self.cache_max_size:
            # Remove oldest entries (first 20%)
            keys_to_remove = list(self.response_cache.keys())[:int(self.cache_max_size * 0.2)]
            for key in keys_to_remove:
                del self.response_cache[key]
        
        self.response_cache[cache_key] = response
    
    async def ask_question(self, request: ChatbotQueryRequest) -> Dict:
        """Answer a farming question with consistent responses and interactive counter-questions"""
        
        if not self.enabled:
            return self._fallback_response(request.question)
        
        try:
            # Step 1: Check if this question needs counter-questions for more details
            counter_question = self._check_counter_question(request.question)
            if counter_question:
                return {
                    "response_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "question": request.question,
                    "answer": counter_question,
                    "language": request.language,
                    "confidence": 1.0,  # High confidence for predefined responses
                    "related_topics": [],
                    "sources": ["FasalMitra Interactive Assistant"],
                    "session_id": request.session_id,
                    "requires_input": True  # Flag indicating we need more info
                }
            
            # Step 2: Check cache for consistent responses to same questions
            cache_key = self._get_cache_key(request.question, request.language)
            cached_answer = self._get_cached_response(cache_key)
            
            if cached_answer:
                return {
                    "response_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "question": request.question,
                    "answer": cached_answer,
                    "language": request.language,
                    "confidence": 0.95,  # Higher confidence for cached responses
                    "related_topics": self._extract_related_topics(cached_answer),
                    "sources": ["AI-Generated", "Cached Response"],
                    "session_id": request.session_id
                }
            
            # Step 3: Rate limiting before API call
            self._wait_for_rate_limit()
            
            # Step 4: Create context-aware prompt
            prompt = self._create_question_prompt(request)
            
            # Step 5: Generate response with temperature=0 for consistency
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            answer_text = response.text
            
            # Step 6: Cache the response for future consistency
            self._cache_response(cache_key, answer_text)
            
            result = {
                "response_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "question": request.question,
                "answer": answer_text,
                "language": request.language,
                "confidence": 0.85,
                "related_topics": self._extract_related_topics(answer_text),
                "sources": ["AI-Generated", "Agricultural Knowledge Base"],
                "session_id": request.session_id
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Error in chatbot query: {str(e)}")
            return self._fallback_response(request.question)
    
    async def explain_term(self, request: ExplainTermRequest) -> Dict:
        """Explain a farming term"""
        
        if not self.enabled:
            return self._fallback_term_explanation(request.term)
        
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Create explanation prompt
            prompt = self._create_explanation_prompt(request)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            result = {
                "term": request.term,
                "explanation": response.text,
                "examples": self._extract_examples(response.text),
                "related_terms": self._extract_related_terms(request.term),
                "language": request.language,
                "measurement_method": None,
                "learning_resources": [
                    "Local agricultural extension office",
                    "Agricultural universities",
                    "Online farming courses"
                ]
            }
            
            return result
        
        except Exception as e:
            logger.error(f"Error explaining term: {str(e)}")
            return self._fallback_term_explanation(request.term)
    
    def get_status(self) -> Dict:
        """Get chatbot service status"""
        return {
            "enabled": self.enabled,
            "gemini_available": GEMINI_AVAILABLE,
            "api_key_configured": bool(settings.GEMINI_API_KEY),
            "model": "gemini-flash-latest" if self.enabled else None,
            "status": "operational" if self.enabled else "fallback_mode"
        }
    
    def _create_question_prompt(self, request: ChatbotQueryRequest) -> str:
        """Create context-aware prompt for questions"""
        
        # Language-specific instructions
        language_map = {
            'hi': 'Hindi (हिंदी)',
            'en': 'English',
            'ta': 'Tamil (தமிழ்)',
            'te': 'Telugu (తెలుగు)',
            'mr': 'Marathi (मराठी)',
            'bn': 'Bengali (বাংলা)',
            'gu': 'Gujarati (ગુજરાતી)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'ml': 'Malayalam (മലയാളം)',
            'pa': 'Punjabi (ਪੰਜਾਬੀ)'
        }
        
        language_name = language_map.get(request.language, 'English')
        
        prompt = f"""You are FasalMitra AI - an expert agricultural advisor for Indian farmers.

LANGUAGE: Respond in {language_name}

USER QUESTION: {request.question}

CONTEXT: {request.context or 'General farming inquiry'}

CRITICAL RESPONSE GUIDELINES:

1. **BE INTERACTIVE & HELPFUL**:
   - If the question is VAGUE or needs SPECIFIC data (like calculations), ASK for details first
   - For calculation questions (yield, profit, fertilizer dose), ask: "To help you accurately, please share: [list specific parameters needed]"
   - Always engage like a friendly farming expert who wants to help

2. **WHEN TO ASK CLARIFYING QUESTIONS**:
   - Yield calculation → Ask for: crop, area, location, soil type, irrigation method
   - Fertilizer dose → Ask for: crop, area, soil pH, growth stage
   - Profit estimation → Ask for: crop, area, input costs, expected yield, market price
   - Disease/pest → Ask for: crop name, symptoms, affected area, photos if possible
   - Weather advice → Ask for: location, crop being grown

3. **BE CONCISE**: Keep responses SHORT (max 150 words) and focused on KEY POINTS only

4. **STRUCTURE WELL**: Use this format:
   - Start with a brief direct answer (1-2 sentences)
   - Key Points: Use bullet points (•) with emojis for visual clarity
   - Add practical tips if space allows
   - End with YouTube search hint if relevant

5. **HANDLE ALL QUESTIONS**:
   - Farming questions: Give specific, actionable advice
   - Non-farming questions: Politely redirect to farming topics
   - Unclear questions: Ask for clarification politely
   - Greetings: Respond warmly and ask how you can help with farming

6. **MAKE IT PRACTICAL**:
   - Mention costs in ₹ if relevant
   - Use simple words farmers understand
   - Focus on Indian farming conditions
   - Include seasonal advice when applicable

7. **YOUTUBE INTEGRATION**:
   - For "how-to" questions, add: "🎥 Watch: 'topic language tutorial'" at the end
   - Suggest specific search terms in user's language
   - Example: "🎥 Search YouTube: 'टमाटर की खेती हिंदी में'"

EXAMPLE INTERACTIVE RESPONSE:
Question: "How to calculate profit from my wheat crop?"
Response: "I'd love to help you calculate your wheat profit! 📊

To give you an accurate estimate, please share:
• 📏 **Farm area**: How many acres/hectares?
• 💰 **Input costs**: Seeds, fertilizers, labor, irrigation (approx ₹)
• 🌾 **Expected yield**: Quintals per acre you expect?
• 🏪 **Market price**: Current MSP or local mandi rate?

Share these details and I'll calculate your estimated profit! 💵"

EXAMPLE DIRECT RESPONSE:
Question: "What is NPK?"
Response: "NPK stands for the three main nutrients in fertilizers:

• **N (Nitrogen)**: For leaf growth and green color
• **P (Phosphorus)**: For root development and flowering
• **K (Potassium)**: For overall plant health and disease resistance

**Tip:** A balanced NPK (like 10-10-10) works for most crops. Check your soil test for specific needs!

🎥 Search YouTube: 'NPK fertilizer explained Hindi'"

Remember: BE INTERACTIVE when calculations are needed, DIRECT when giving information. Always stay helpful and friendly!
"""
        return prompt
    
    def _create_explanation_prompt(self, request: ExplainTermRequest) -> str:
        """Create prompt for term explanation"""
        prompt = f"""Explain the agricultural term "{request.term}" in simple language for farmers.

KEEP IT SHORT (max 100 words) and STRUCTURED:

**Definition:** One clear sentence

**Why It Matters:** How it affects farming (1-2 sentences)

**How to Measure/Identify:** Practical method

**Example:** One real-world example

**Related Terms:** 2-3 similar concepts

Add this if helpful:
🎥 For detailed tutorial, search YouTube: "{request.term} farming explanation"

Context: {request.context or 'General farming context'}

Language: {request.language}
"""
        return prompt
    
    def _wait_for_rate_limit(self):
        """Implement rate limiting"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        
        self.last_request_time = time.time()
    
    def _extract_related_topics(self, text: str) -> List[str]:
        """Extract related topics from response (simple implementation)"""
        # In production, use NLP to extract topics
        keywords = ["fertilizer", "irrigation", "pesticide", "soil", "weather", "crop rotation"]
        found_topics = [kw for kw in keywords if kw.lower() in text.lower()]
        return found_topics[:3]
    
    def _extract_examples(self, text: str) -> List[str]:
        """Extract examples from text"""
        # Simple extraction - in production, use better NLP
        return ["See explanation above for practical examples"]
    
    def _extract_related_terms(self, term: str) -> List[str]:
        """Get related terms"""
        # Predefined related terms
        related_map = {
            'pH': ['soil acidity', 'lime application', 'sulfur treatment'],
            'NPK': ['nitrogen', 'phosphorus', 'potassium', 'fertilizer'],
            'irrigation': ['water management', 'drip irrigation', 'sprinkler'],
            'yield': ['productivity', 'harvest', 'crop output']
        }
        
        for key, related in related_map.items():
            if key.lower() in term.lower():
                return related
        
        return []
    
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when Gemini is not available"""
        return {
            "response_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "question": question,
            "answer": """Thank you for your question about farming. 
            
The AI chatbot is currently unavailable. Please:
1. Contact your local agricultural extension office
2. Consult with experienced farmers in your area
3. Check government agricultural websites for guidance
4. Use other features of FasalMitra for crop and yield predictions

For immediate assistance, please enable the Gemini API by setting GEMINI_API_KEY in your environment variables.""",
            "language": "en",
            "confidence": 0.5,
            "related_topics": [],
            "sources": ["System Message"],
            "session_id": None
        }
    
    def _fallback_term_explanation(self, term: str) -> Dict:
        """Fallback term explanation"""
        common_terms = {
            'pH': 'A measure of soil acidity or alkalinity. Range: 0-14, with 7 being neutral. Most crops prefer pH 6-7.',
            'NPK': 'The three main nutrients in fertilizer: Nitrogen (N), Phosphorus (P), and Potassium (K).',
            'yield': 'The amount of crop produced per unit area, usually measured in tons per hectare.',
            'irrigation': 'The artificial application of water to crops to help growth.',
            'fertilizer': 'Substance added to soil to supply nutrients for plant growth.'
        }
        
        explanation = common_terms.get(
            term.lower(), 
            f"'{term}' is an agricultural term. Please consult agricultural resources for detailed information."
        )
        
        return {
            "term": term,
            "explanation": explanation,
            "examples": ["Contact local agricultural experts for examples"],
            "related_terms": [],
            "language": "en",
            "measurement_method": "Consult agricultural extension services",
            "learning_resources": ["Local agricultural office", "Agricultural websites"]
        }


@lru_cache()
def get_chatbot_service() -> ChatbotService:
    """Get singleton instance of chatbot service"""
    return ChatbotService()
