def rank_files_by_intent_and_year(files, year, core_sentences, extract_text_from_file_fn):
    def score(file_text):
        text = file_text.lower()
        matched = sum(1 for s in core_sentences if s in text)
        has_year = year and year in text
        return (
            0 if matched == len(core_sentences) and has_year else
            1 if matched == len(core_sentences) else
            2 if matched > 1 and has_year else
            3 if has_year else
            4
        )

    scored = []
    for f in files:
        try:
            content = extract_text_from_file_fn(f)  # You’ll build this next
            scored.append((score(content), f))
        except:
            scored.append((5, f))  # fallback worst score

    return [f for _, f in sorted(scored, key=lambda x: x[0])]
