"""
strength.py - Password strength analysis
"""

import re
import string


def check_strength(password: str) -> dict:
    """
    Analyze the strength of a given password.

    Args:
        password: The password string to evaluate.

    Returns:
        A dict with 'score' (0-100), 'label', and 'tips' list.
    """
    score = 0
    tips = []

    # Length scoring
    length = len(password)
    if length >= 8:
        score += 20
    elif length >= 6:
        score += 10
    else:
        tips.append("Use at least 8 characters.")

    if length >= 12:
        score += 10
    if length >= 16:
        score += 10

    # Character variety
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(rf"[{re.escape(string.punctuation)}]", password))

    if has_upper:
        score += 15
    else:
        tips.append("Add uppercase letters (A-Z).")

    if has_lower:
        score += 15
    else:
        tips.append("Add lowercase letters (a-z).")

    if has_digit:
        score += 15
    else:
        tips.append("Add digits (0-9).")

    if has_symbol:
        score += 15
    else:
        tips.append("Add special characters (!@#$...).")

    # Penalize repetition
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        tips.append("Avoid repeating characters (e.g. aaa, 111).")

    # Penalize sequential patterns
    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde)", password.lower()):
        score -= 10
        tips.append("Avoid sequential patterns (e.g. 123, abc).")

    score = max(0, min(score, 100))

    if score >= 80:
        label = "Strong 💪"
    elif score >= 50:
        label = "Moderate ⚠️"
    else:
        label = "Weak ❌"

    return {"score": score, "label": label, "tips": tips}
