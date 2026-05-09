def calculate_score(title, snippet, link):
    text = f"{title} {snippet} {link}".lower()

    score = 0
    reasons = []

    keywords = {
        "vista mare": 20,
        "mare": 12,
        "spiaggia": 12,
        "centro": 10,
        "terrazza": 10,
        "balcone": 8,
        "piscina": 15,
        "villa": 15,
        "luxury": 12,
        "panoramica": 15,
        "estate": 10,
        "casa vacanza": 12,
        "affitto breve": 10,
        "appartamento": 8,
    }

    for keyword, points in keywords.items():
        if keyword in text:
            score += points
            reasons.append(keyword)

    locations = {
        "capri": 15,
        "ischia": 14,
        "procida": 13,
        "bacoli": 10,
        "monte di procida": 10,
    }

    for location, points in locations.items():
        if location in text:
            score += points
            reasons.append(location)

    score = min(score, 100)

    return score, ", ".join(reasons) if reasons else "general rental match"


def add_scores_to_deals(df):
    scores = []
    reasons = []

    for _, row in df.iterrows():
        score, reason = calculate_score(
            row.get("title", ""),
            row.get("snippet", ""),
            row.get("link", "")
        )
        scores.append(score)
        reasons.append(reason)

    df["intelligence_score"] = scores
    df["score_reasons"] = reasons

    return df