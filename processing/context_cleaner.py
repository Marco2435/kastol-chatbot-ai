
def clean_context(tekst):
    """
    Verwijdert overbodige spaties, lege regels en nietszeggende stukjes uit tekstblokken.
    """
    regels = tekst.splitlines()
    schone_regels = [r.strip() for r in regels if r.strip()]
    return "\n".join(schone_regels)
