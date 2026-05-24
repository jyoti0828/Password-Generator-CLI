"""
utils.py - Utility functions (file saving, clipboard, display)
"""

import os
from datetime import datetime


def save_to_file(passwords: list[str], filepath: str = "passwords.txt") -> str:
    """
    Save a list of passwords to a text file with timestamps.

    Args:
        passwords: List of password strings to save.
        filepath: Destination file path.

    Returns:
        Absolute path to the saved file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"# Passwords generated on {timestamp}\n"]
    lines += [f"{pwd}\n" for pwd in passwords]

    with open(filepath, "a", encoding="utf-8") as f:
        f.writelines(lines)

    return os.path.abspath(filepath)


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard using pyperclip.

    Args:
        text: String to copy.

    Returns:
        True if successful, False if pyperclip is unavailable.
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        return False
    except Exception:
        return False
