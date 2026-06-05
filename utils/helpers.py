"""
helpers.py
──────────
Utility functions for emergency keyword detection and response formatting.
"""

import re

# Emergency keywords that trigger immediate alert (multilingual)
EMERGENCY_KEYWORDS = [
    # English
    "heart attack", "cardiac arrest", "chest pain shortness of breath",
    "can't breathe", "cannot breathe", "not breathing", "unconscious",
    "stroke", "face drooping", "arm weakness", "speech difficulty",
    "severe bleeding", "poisoning", "overdose", "suicide", "suicidal",
    "seizure", "anaphylaxis", "severe allergic reaction",
    # Tamil
    "மாரடைப்பு", "மூச்சு திணறல்", "நினைவிழந்து",
    # Hindi
    "दिल का दौरा", "सांस नहीं आ रही", "बेहोश", "जहर",
    # French
    "crise cardiaque", "ne respire pas", "inconscient",
    # Spanish
    "ataque al corazón", "no puede respirar", "inconsciente",
]

# Non-medical keywords to block
NON_MEDICAL_PATTERNS = [
    # People / celebrities
    r"who is ", r"who was ", r"who are ",
    r"tell me about [a-z]+ [a-z]+",
    # Sports
    r"cricket", r"football", r"soccer", r"tennis", r"ipl", r"world cup",
    r"virat", r"kohli", r"dhoni", r"messi", r"ronaldo", r"sachin",
    # Politics
    r"prime minister", r"president", r"politician", r"election",
    r"government", r"minister", r"modi", r"biden", r"trump",
    # Entertainment
    r"actor", r"actress", r"movie", r"film", r"song", r"singer",
    r"music", r"album", r"celebrity", r"hero", r"heroine",
    # General knowledge
    r"capital of", r"history of", r"geography",
    r"what is the currency", r"population of",
    # Technology (non-medical)
    r"coding", r"programming", r"software", r"hardware",
    r"python language", r"javascript", r"chatgpt", r"artificial intelligence",
    # Finance
    r"stock market", r"crypto", r"bitcoin", r"investment", r"share price",
    # Weather / news
    r"weather", r"news today", r"latest news",
]


def is_non_medical(text: str) -> bool:
    """
    Check if the user's input is a non-medical question.

    Args:
        text: Raw user input string.

    Returns:
        True if non-medical topic detected, False otherwise.
    """
    text_lower = text.lower()
    for pattern in NON_MEDICAL_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def is_emergency(text: str) -> bool:
    """
    Check if the user's input contains emergency keywords.

    Args:
        text: Raw user input string.

    Returns:
        True if emergency keywords detected, False otherwise.
    """
    text_lower = text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True

    # Pattern: chest pain AND (breathless / shortness)
    chest_pain = bool(re.search(r"chest\s*(pain|tight|pressure)", text_lower))
    breathless = bool(re.search(r"(breath|breath(ing)?|shortness)", text_lower))
    if chest_pain and breathless:
        return True

    return False


def format_disclaimer() -> str:
    """Return the standard medical disclaimer string."""
    return (
        "⚠️ *Disclaimer: This is not a substitute for professional medical advice. "
        "Always consult a qualified healthcare professional for proper diagnosis and treatment.*"
    )


def clean_response_for_display(text: str) -> str:
    """
    Convert markdown-style bold (**text**) to HTML <b> tags for Streamlit display.

    Args:
        text: Response text with markdown formatting.

    Returns:
        HTML-safe string.
    """
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = text.replace("\n", "<br>")
    return text