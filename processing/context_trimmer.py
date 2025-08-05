
def trim_context(context: str, max_chars: int = 12000) -> str:
    """
    Trimt de context op maximaal aantal tekens, met behoud van paragraafstructuur.
    """
    regels = context.split("\n")
    samengevoegd = ""
    for regel in regels:
        if len(samengevoegd) + len(regel) + 1 > max_chars:
            break
        samengevoegd += regel + "\n"
    return samengevoegd.strip()
