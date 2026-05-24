"""
generator.py - Core password generation logic
"""

import random
import string


def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """
    Generate a secure random password based on given options.

    Args:
        length: Length of the password (min 4)
        use_uppercase: Include uppercase letters (A-Z)
        use_lowercase: Include lowercase letters (a-z)
        use_digits: Include digits (0-9)
        use_symbols: Include special characters (!@#$...)
        exclude_ambiguous: Exclude visually similar chars (0, O, l, 1, I)

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If no character set is selected or length is too short.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    character_pool = ""
    guaranteed_chars = []

    AMBIGUOUS = set("0Ol1I")

    def clean(chars: str) -> str:
        if exclude_ambiguous:
            return "".join(c for c in chars if c not in AMBIGUOUS)
        return chars

    if use_uppercase:
        pool = clean(string.ascii_uppercase)
        character_pool += pool
        guaranteed_chars.append(random.choice(pool))

    if use_lowercase:
        pool = clean(string.ascii_lowercase)
        character_pool += pool
        guaranteed_chars.append(random.choice(pool))

    if use_digits:
        pool = clean(string.digits)
        character_pool += pool
        guaranteed_chars.append(random.choice(pool))

    if use_symbols:
        pool = clean(string.punctuation)
        character_pool += pool
        guaranteed_chars.append(random.choice(pool))

    if not character_pool:
        raise ValueError("At least one character type must be selected.")

    # Fill remaining characters randomly
    remaining_length = length - len(guaranteed_chars)
    random_chars = [random.choice(character_pool) for _ in range(remaining_length)]

    # Combine and shuffle to avoid predictable positions
    password_list = guaranteed_chars + random_chars
    random.shuffle(password_list)

    return "".join(password_list)


def generate_multiple(count: int, **kwargs) -> list[str]:
    """
    Generate multiple passwords with the same settings.

    Args:
        count: Number of passwords to generate
        **kwargs: Options passed to generate_password()

    Returns:
        List of generated passwords.
    """
    if count < 1:
        raise ValueError("Count must be at least 1.")
    return [generate_password(**kwargs) for _ in range(count)]
