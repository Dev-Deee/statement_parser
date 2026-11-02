SOFT_HYPHEN = "\xad"
ELLIPSIS = "\u2026"  # the single "…" character banks use for cut-off text


def clean_cell(text: str | None) -> str:
    """Turn soft hyphens into real ones and collapse line breaks and spaces."""
    if text is None:
        return ""
    return " ".join(text.replace(SOFT_HYPHEN, "-").split())
