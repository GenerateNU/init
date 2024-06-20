from pyfiglet import figlet_format
from re import sub


def to_lower_kebab_case(text: str) -> str:
    text = sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = sub(r"([a-z\d])([A-Z])", r"\1_\2", text)
    return sub(r"[ _]", "-", text).lower()


def get_ascii_art(text: str) -> str:
    return figlet_format(text, font="small_slant")


class ValidationError(Exception):
    pass
