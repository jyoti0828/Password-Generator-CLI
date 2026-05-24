"""
password_generator - A CLI tool to generate secure passwords.
"""

from .generator import generate_password, generate_multiple
from .strength import check_strength
from .utils import save_to_file, copy_to_clipboard

__all__ = [
    "generate_password",
    "generate_multiple",
    "check_strength",
    "save_to_file",
    "copy_to_clipboard",
]
