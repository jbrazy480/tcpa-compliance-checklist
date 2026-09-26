"""Strict NANP syntax and common US display-format normalization."""
import re


def normalize_phone(phone: str) -> str:
    """Accept +1, 1-prefixed or ten-digit NANP numbers; reject extensions."""
    if not isinstance(phone, str) or not re.fullmatch(r"\+?[0-9 ()\.\-]+", phone):
        raise ValueError("invalid NANP phone number")
    digits = re.sub(r"[^0-9]", "", phone)
    if phone.startswith("+") and (len(digits) != 11 or not digits.startswith("1")):
        raise ValueError("invalid NANP country code")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if not re.fullmatch(r"[2-9][0-9]{2}[2-9][0-9]{6}", digits):
        raise ValueError("invalid NANP phone number")
    return "+1" + digits


def require_e164(phone: str) -> str:
    if not isinstance(phone, str) or not re.fullmatch(r"\+1[2-9][0-9]{2}[2-9][0-9]{6}", phone):
        raise ValueError("phone must be a +1 E.164 NANP number")
    return phone
