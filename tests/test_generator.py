"""
test_generator.py - Unit tests for password generator
Run with: python -m pytest tests/ -v
"""

import pytest
from password_generator.generator import generate_password, generate_multiple
from password_generator.strength import check_strength
import string


# ─────────────────────────────────────────────
# generate_password tests
# ─────────────────────────────────────────────

class TestGeneratePassword:

    def test_default_length(self):
        pwd = generate_password()
        assert len(pwd) == 12

    def test_custom_length(self):
        pwd = generate_password(length=20)
        assert len(pwd) == 20

    def test_minimum_length(self):
        pwd = generate_password(length=4)
        assert len(pwd) == 4

    def test_length_too_short_raises(self):
        with pytest.raises(ValueError):
            generate_password(length=3)

    def test_only_digits(self):
        pwd = generate_password(
            use_uppercase=False, use_lowercase=False,
            use_digits=True, use_symbols=False
        )
        assert all(c in string.digits for c in pwd)

    def test_only_uppercase(self):
        pwd = generate_password(
            use_uppercase=True, use_lowercase=False,
            use_digits=False, use_symbols=False
        )
        assert all(c in string.ascii_uppercase for c in pwd)

    def test_no_character_set_raises(self):
        with pytest.raises(ValueError):
            generate_password(
                use_uppercase=False, use_lowercase=False,
                use_digits=False, use_symbols=False
            )

    def test_exclude_ambiguous(self):
        ambiguous = set("0Ol1I")
        for _ in range(50):
            pwd = generate_password(length=16, exclude_ambiguous=True)
            assert not any(c in ambiguous for c in pwd)

    def test_contains_all_types(self):
        """Password with all types should contain at least one of each."""
        pwd = generate_password(length=16)
        assert any(c in string.ascii_uppercase for c in pwd)
        assert any(c in string.ascii_lowercase for c in pwd)
        assert any(c in string.digits for c in pwd)
        assert any(c in string.punctuation for c in pwd)


# ─────────────────────────────────────────────
# generate_multiple tests
# ─────────────────────────────────────────────

class TestGenerateMultiple:

    def test_returns_correct_count(self):
        passwords = generate_multiple(5)
        assert len(passwords) == 5

    def test_all_correct_length(self):
        passwords = generate_multiple(3, length=14)
        assert all(len(p) == 14 for p in passwords)

    def test_count_zero_raises(self):
        with pytest.raises(ValueError):
            generate_multiple(0)

    def test_passwords_are_unique(self):
        """10 passwords should almost certainly be unique."""
        passwords = generate_multiple(10, length=16)
        assert len(set(passwords)) > 1


# ─────────────────────────────────────────────
# check_strength tests
# ─────────────────────────────────────────────

class TestCheckStrength:

    def test_strong_password(self):
        result = check_strength("G7!kLpW#2mQr")
        assert result["score"] >= 80
        assert "Strong" in result["label"]

    def test_weak_password(self):
        result = check_strength("abc")
        assert result["score"] < 50
        assert "Weak" in result["label"]

    def test_moderate_password(self):
        result = check_strength("Hello123")
        assert 40 <= result["score"] < 80

    def test_tips_for_missing_symbols(self):
        result = check_strength("HelloWorld123")
        assert any("special" in tip.lower() for tip in result["tips"])

    def test_tips_for_repetition(self):
        result = check_strength("aaabbbccc111")
        assert any("repeat" in tip.lower() for tip in result["tips"])

    def test_score_bounded(self):
        result = check_strength("a" * 100)
        assert 0 <= result["score"] <= 100
