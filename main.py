#!/usr/bin/env python3
"""
main.py - CLI entry point for the Password Generator Tool

Usage:
    python main.py                        # Generate 1 password (defaults)
    python main.py -l 16                  # 16-character password
    python main.py -l 20 -c 5            # 5 passwords of length 20
    python main.py --no-symbols           # Exclude special characters
    python main.py --no-uppercase         # Exclude uppercase letters
    python main.py --exclude-ambiguous    # Exclude 0, O, l, 1, I
    python main.py -l 16 --save          # Save to passwords.txt
    python main.py -l 16 --copy          # Copy first password to clipboard
    python main.py --check "MyP@ssw0rd"  # Check strength of a password
"""

import argparse
import sys

from password_generator import (
    generate_password,
    generate_multiple,
    check_strength,
    save_to_file,
    copy_to_clipboard,
)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def print_banner():
    print("\n" + "=" * 50)
    print("   🔐  Password Generator CLI Tool")
    print("=" * 50)


def print_strength(password: str):
    result = check_strength(password)
    print(f"\n  Strength : {result['label']}  ({result['score']}/100)")
    if result["tips"]:
        print("  Tips     :")
        for tip in result["tips"]:
            print(f"    • {tip}")


# ─────────────────────────────────────────────
# Argument Parser
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="passgen",
        description="🔐 Generate secure, customizable passwords from the command line.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        metavar="N",
        help="Length of the password (default: 12, min: 4)",
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        metavar="N",
        help="Number of passwords to generate (default: 1)",
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters (A-Z)",
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters (a-z)",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits (0-9)",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude special characters (!@#$...)",
    )
    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="Exclude visually ambiguous characters (0, O, l, 1, I)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save generated password(s) to passwords.txt",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the first generated password to clipboard",
    )
    parser.add_argument(
        "--check",
        type=str,
        metavar="PASSWORD",
        help="Check the strength of a given password (skips generation)",
    )

    return parser


# ─────────────────────────────────────────────
# Main Logic
# ─────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    print_banner()

    # ── Strength check mode ──────────────────
    if args.check:
        print(f"\n  Checking : {args.check}")
        print_strength(args.check)
        print()
        return

    # ── Validate options ─────────────────────
    if args.length < 4:
        print("\n  ❌  Error: Password length must be at least 4.")
        sys.exit(1)

    if args.count < 1:
        print("\n  ❌  Error: Count must be at least 1.")
        sys.exit(1)

    options = {
        "length": args.length,
        "use_uppercase": not args.no_uppercase,
        "use_lowercase": not args.no_lowercase,
        "use_digits": not args.no_digits,
        "use_symbols": not args.no_symbols,
        "exclude_ambiguous": args.exclude_ambiguous,
    }

    # ── Generate passwords ───────────────────
    try:
        passwords = generate_multiple(args.count, **options)
    except ValueError as e:
        print(f"\n  ❌  Error: {e}")
        sys.exit(1)

    print(f"\n  Generated {args.count} password(s) [length={args.length}]:\n")
    for i, pwd in enumerate(passwords, start=1):
        label = f"  [{i}]" if args.count > 1 else "  Password"
        print(f"{label}  →  {pwd}")

    # Show strength for single password
    if args.count == 1:
        print_strength(passwords[0])

    # ── Copy to clipboard ────────────────────
    if args.copy:
        success = copy_to_clipboard(passwords[0])
        if success:
            print("\n  ✅  First password copied to clipboard!")
        else:
            print("\n  ⚠️   Clipboard copy failed. Install pyperclip: pip install pyperclip")

    # ── Save to file ─────────────────────────
    if args.save:
        filepath = save_to_file(passwords)
        print(f"\n  💾  Saved to: {filepath}")

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
