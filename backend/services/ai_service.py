import os
import logging
import base64
import json
from typing import List
import google.generativeai as genai

# Configure Google Generative AI with API key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY not found. Set it in .env file")
genai.configure(api_key=GEMINI_API_KEY)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "hi": "Hindi",
    "ar": "Arabic",
    "zh": "Chinese",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ta": "Tamil",
    "te": "Telugu",
    "ko": "Korean"
}

def extract_json_from_response(text: str) -> dict:
    """Extract and parse JSON from AI response"""
    text = text.strip()
    
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0].strip()
    elif '```' in text:
        text = text.split('```')[1].split('```')[0].strip()
    
    if not text.startswith('{'):
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
    
    text = text.strip()
    
    if not text:
        raise ValueError("Empty response after JSON extraction")
    
    return json.loads(text)

def get_image_mime_type(image_bytes: bytes) -> str:
    """Detect image MIME type from magic bytes"""
    if image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif image_bytes.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    elif image_bytes.startswith(b'RIFF') and len(image_bytes) > 12 and image_bytes[8:12] == b'WEBP':
        return 'image/webp'
    elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):
        return 'image/gif'
    return 'image/png' # fallback

async def analyze_prescription_image(image_base64: str, preferred_language: str) -> dict:
    """Analyze prescription image using Gemini Vision"""
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_base64)
        
        # Detect MIME type from bytes
        mime_type = get_image_mime_type(image_bytes)
        
        # Create image part for Gemini
        image_part = {
            'mime_type': mime_type,
            'data': image_bytes
        }
        
        prompt = """Analyze this prescription image. It may be in ANY language.
 
Return ONLY valid JSON (no markdown):
{
    "detected_language": "language code (en/es/hi/ar/zh/fr/de/pt/ru/ja/ta/te/ko)",
    "detected_language_name": "language name",
    "extracted_text": "full original text from prescription",
    "medications": [
        {
            "name": "medication name in original language",
            "name_english": "medication name in English",
            "dosage": "dosage amount",
            "frequency": "frequency",
            "timing": ["morning", "evening"],
            "duration": "duration if specified",
            "with_food": true/false
        }
    ]
}
 
If unclear, return: {"detected_language": "unknown", "detected_language_name": "Unknown", "extracted_text": "Unable to read", "medications": []}"""
        
        response = model.generate_content([prompt, image_part])
        result = extract_json_from_response(response.text)
        
        if 'extracted_text' not in result:
            result['extracted_text'] = 'No text extracted'
        if 'medications' not in result:
            result['medications'] = []
        if 'detected_language' not in result:
            result['detected_language'] = 'unknown'
        if 'detected_language_name' not in result:
            result['detected_language_name'] = 'Unknown'
            
        return result
    except Exception as e:
        logging.error(f"Prescription analysis error: {str(e)}")
        raise

async def generate_medication_explanation(
    med_name: str, 
    dosage: str, 
    frequency: str, 
    target_language: str
) -> dict:
    """Generate plain language explanation with Nudge Theory"""
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""For medication '{med_name}' (dosage: '{dosage}', frequency: {frequency}):
 
Provide explanation in {SUPPORTED_LANGUAGES.get(target_language, 'English')}:
1. Simple explanation (what it does, 2-3 sentences)
2. Why timing matters (Nudge Theory)
3. Dosage safety reminder
 
Return ONLY valid JSON:
{
    "plain_explanation": "simple explanation",
    "why_timing_matters": "why timing is important",
    "dosage_safety_reminder": "safety reminder"
}"""
        
        response = model.generate_content(prompt)
        result = extract_json_from_response(response.text)
        
        if 'plain_explanation' not in result:
            result['plain_explanation'] = f"This medication is prescribed for your health condition."
        if 'why_timing_matters' not in result:
            result['why_timing_matters'] = "Taking medication at the right time helps maintain consistent levels."
        if 'dosage_safety_reminder' not in result:
            result['dosage_safety_reminder'] = "Always follow the prescribed dosage exactly."
            
        return result
    except Exception as e:
        logging.error(f"Explanation generation error: {str(e)}")
        return {
            'plain_explanation': f"This medication is prescribed for your health.",
            'why_timing_matters': "Timing helps maintain steady medication levels.",
            'dosage_safety_reminder': "Always follow the prescribed dosage exactly."
        }

async def check_drug_interactions(
    medication_name: str, 
    current_medications: List[str], 
    language: str
) -> dict:
    """Check for drug interactions"""
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""Check if '{medication_name}' has contraindications with: {', '.join(current_medications)}.
 
Provide in {SUPPORTED_LANGUAGES.get(language, 'English')}.
 
Return ONLY valid JSON:
{
    "has_contraindications": true/false,
    "warnings": ["list of warnings"],
    "recommendations": "recommendations"
}"""
        
        response = model.generate_content(prompt)
        result = extract_json_from_response(response.text)
        return result
    except Exception as e:
        logging.error(f"Contraindication check error: {str(e)}")
        raise
