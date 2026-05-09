def classify_deal(title, snippet, link):
    text = f"{title} {snippet} {link}".lower()

    categories = []

    if any(word in text for word in ["luxury", "lusso", "villa", "premium", "exclusive"]):
        categories.append("luxury")

    if any(word in text for word in ["famiglia", "family", "bambini", "kids"]):
        categories.append("family")

    if any(word in text for word in ["mare", "spiaggia", "beach", "vista mare"]):
        categories.append("beach")

    if any(word in text for word in ["estate", "stagione", "stagionale", "vacanza", "holiday"]):
        categories.append("seasonal")

    if any(word in text for word in ["economico", "low cost", "budget", "conveniente"]):
        categories.append("budget")

    if any(word in text for word in ["investimento", "rendita", "income", "property investment"]):
        categories.append("investment")

    if not categories:
        categories.append("general")

    return ", ".join(categories)


def add_categories_to_deals(df):
    df["deal_category"] = df.apply(
        lambda row: classify_deal(
            row.get("title", ""),
            row.get("snippet", ""),
            row.get("link", "")
        ),
        axis=1
    )

    return df