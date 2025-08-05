
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def fuzzy_search(vraag, context_lijst, threshold=70):
    matches = []
    for blok in context_lijst:
        score = fuzz.partial_ratio(vraag.lower(), blok.lower())
        if score >= threshold:
            matches.append((score, blok))
    matches.sort(reverse=True)
    return "\n".join([blok for score, blok in matches[:3]])
