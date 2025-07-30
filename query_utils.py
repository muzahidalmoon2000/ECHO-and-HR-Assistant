import re

def extract_year_and_core_intent(query: str):
    year_match = re.search(r'\b(19|20)\d{2}\b', query)
    year = year_match.group() if year_match else None
    words = query.split()
    if year:
        words.remove(year)
    core = " ".join(words)
    return year, core

def generate_query_batches(core_intent: str):
    words = core_intent.lower().split()
    batches = [
        core_intent,
        words[0],
        " ".join(words[1:]) if len(words) > 1 else "",
        words[1] if len(words) > 1 else "",
        words[2] if len(words) > 2 else ""
    ]
    return list(dict.fromkeys([b for b in batches if b]))
