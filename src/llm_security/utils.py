"""Text normalization helpers for LLM output comparison."""

_CURLY_REPLACEMENTS = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u00a0": " ",
}


def normalize(text: str) -> str:
    """Normalize LLM output for reliable comparison."""
    for curly, straight in _CURLY_REPLACEMENTS.items():
        text = text.replace(curly, straight)
    return text.lower().strip()