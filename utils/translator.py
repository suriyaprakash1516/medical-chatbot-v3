"""
translator.py - Groq (Fixed language detection)
"""

import os
import json
from typing import Tuple
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANG_NAME_MAP = {
    "en": "English", "ta": "Tamil",  "hi": "Hindi",
    "fr": "French",  "es": "Spanish","ar": "Arabic",
    "te": "Telugu",  "kn": "Kannada","ml": "Malayalam",
    "de": "German",  "zh": "Chinese","ja": "Japanese",
    "pt": "Portuguese", "ru": "Russian",
}

# ONLY pure Tanglish words that will NEVER appear in normal English sentences
TANGLISH_HINTS = [
    "enakku", "ennaku", "irukku", "iruku",
    "valikuthu", "valikudu", "thalaivali",
    "thalai vali", "vayiru", "kaichal",
    "konjam", "romba", "seri", "theriyum",
    "theriyala", "unakku", "unaku",
    "doctora", "maruthuva", "maruthuvar",
    "paakanum", "sollunga", "mudiyala",
    "aaguthu", "varutha", "peeru",
    "pidikuthu", "pidikkala", "seekiram",
    "nalla iruku", "sariya illai",
    "enna aachu", "enna problem",
]

# ONLY pure Hinglish words that won't appear in English
HINGLISH_HINTS = [
    "mujhe", "meri", "mera",
    "bahut", "thoda", "dard",
    "bukhar", "dawai", "theek nahi",
    "pet mein", "sar mein", "accha nahi",
]


def is_tanglish(text: str) -> bool:
    """Require at least 2 Tanglish word matches to avoid false positives."""
    text_lower = text.lower()
    matches = sum(1 for word in TANGLISH_HINTS if word in text_lower)
    return matches >= 2


def is_hinglish(text: str) -> bool:
    """Require at least 2 Hinglish word matches to avoid false positives."""
    text_lower = text.lower()
    matches = sum(1 for word in HINGLISH_HINTS if word in text_lower)
    return matches >= 2


def detect_and_translate(text: str) -> Tuple[str, str, str]:
    tanglish = is_tanglish(text)
    hinglish  = is_hinglish(text)

    hint = ""
    if tanglish:
        hint = "HINT: This text contains Tanglish (Tamil in English letters). Treat as Tamil."
    elif hinglish:
        hint = "HINT: This text contains Hinglish (Hindi in English letters). Treat as Hindi."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a language detection and translation assistant. "
                "Detect the ACTUAL language of the user text. "
                "If the text is plain English, return language_code 'en'. "
                "Only return 'ta' for actual Tamil or Tanglish text. "
                "Only return 'hi' for actual Hindi or Hinglish text. "
                "Always respond ONLY with a valid JSON object — no markdown, no extra text."
            ),
        },
        {
            "role": "user",
            "content": f"""{hint}

Detect the language and translate to English if needed.
Respond ONLY in this exact JSON format:
{{
  "language_code": "<ISO 639-1 code>",
  "language_name": "<language name>",
  "english_text": "<English translation or original if already English>"
}}

Examples:
"i have a fever"            → {{"language_code":"en","language_name":"English","english_text":"i have a fever"}}
"I have chest pain"         → {{"language_code":"en","language_name":"English","english_text":"I have chest pain"}}
"what is paracetamol"       → {{"language_code":"en","language_name":"English","english_text":"what is paracetamol"}}
"enakku thalai vali irukku" → {{"language_code":"ta","language_name":"Tamil","english_text":"I have a headache"}}
"vayiru romba valikudu"     → {{"language_code":"ta","language_name":"Tamil","english_text":"My stomach hurts a lot"}}
"mujhe bukhar hai"          → {{"language_code":"hi","language_name":"Hindi","english_text":"I have a fever"}}
"எனக்கு தலைவலி"            → {{"language_code":"ta","language_name":"Tamil","english_text":"I have a headache"}}
"मुझे बुखार है"             → {{"language_code":"hi","language_name":"Hindi","english_text":"I have a fever"}}
"j'ai de la fièvre"         → {{"language_code":"fr","language_name":"French","english_text":"I have a fever"}}

User text: {text}""",
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0,
        max_tokens=300,
    )

    raw = response.choices[0].message.content.strip()

    # Safely extract JSON block
    start = raw.find("{")
    end   = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return text, "English", "en"

    lang_code = result.get("language_code", "en")
    lang_name = result.get("language_name", "English")
    eng_text  = result.get("english_text", text)

    # Only override if local detector is very confident (2+ matches)
    if tanglish and lang_code == "en":
        lang_code, lang_name = "ta", "Tamil"
    elif hinglish and lang_code == "en":
        lang_code, lang_name = "hi", "Hindi"

    return eng_text, lang_name, lang_code


def translate_response(english_response: str, target_lang: str) -> str:
    # English input = English response, no translation needed
    if target_lang == "en":
        return english_response

    lang_name = LANG_NAME_MAP.get(target_lang, target_lang)

    special = ""
    if target_lang == "ta":
        special = "Use Tamil script (தமிழ்). Add Tanglish in brackets for difficult words."
    elif target_lang == "hi":
        special = "Use Devanagari script (हिंदी). Keep medical terms simple."
    elif target_lang == "ar":
        special = "Use Arabic script naturally."

    messages = [
        {
            "role": "system",
            "content": (
                f"You are a professional medical translator to {lang_name}. "
                "Return ONLY the translated text — no notes, no commentary."
            ),
        },
        {
            "role": "user",
            "content": f"""Translate this medical response to {lang_name}.

RULES:
- Preserve ALL emoji exactly (💊 🔍 ⚠️ 🏥 🚨 ✅ 📋 ⚖️ 🚫 🔄 💬 etc.)
- Preserve ALL formatting (• bullets, 1. numbered lists, **bold**)
- Simple everyday language
- Return ONLY the translated text
{special}

Text:
{english_response}""",
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2,
        max_tokens=1500,
    )

    return response.choices[0].message.content.strip()