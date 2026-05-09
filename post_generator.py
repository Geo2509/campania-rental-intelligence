import pandas as pd

from config import SCORED_DEALS_FILE, FACEBOOK_POSTS_FILE


def detect_location(text):
    text = text.lower()

    locations = {
        "capri": "Capri",
        "ischia": "Ischia",
        "procida": "Procida",
        "bacoli": "Bacoli",
        "monte di procida": "Monte di Procida",
    }

    for key, value in locations.items():
        if key in text:
            return value

    return "Campania"


def create_post(row):
    title = row.get("title", "")
    snippet = row.get("snippet", "")
    domain = row.get("domain", "")
    score = row.get("intelligence_score", "")
    category = row.get("deal_category", "")
    reasons = row.get("score_reasons", "")
    link = row.get("link", "")

    full_text = f"{title} {snippet} {link}"
    location = detect_location(full_text)

    post = f"""
🏡 Rental opportunity detected in {location}

Our Campania Rental Intelligence Agent found a potentially interesting rental offer for the local short-term rental market.

📌 Property signal:
{title}

📍 Area:
{location}

⭐ Intelligence score:
{score}/100

🏷 Category:
{category}

🔎 Why this offer was selected:
{reasons}

🌍 Source:
{domain}

🔗 More details:
{link}

This is part of an automated real estate monitoring workflow built with Python, data filtering, scoring logic, and content generation.

#Campania #RealEstate #RentalIntelligence #Python #Automation #OSINT #PropertyTech
"""
    return post.strip()


def main():
    df = pd.read_csv(SCORED_DEALS_FILE)

    df = df.sort_values(by="intelligence_score", ascending=False)

    top_deals = df.head(10)

    posts = []

    for index, row in top_deals.iterrows():
        posts.append(f"POST #{len(posts) + 1}")
        posts.append(create_post(row))
        posts.append("\n" + "-" * 60 + "\n")

    with open(FACEBOOK_POSTS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(posts))

    print(f"Facebook posts saved to: {FACEBOOK_POSTS_FILE}")


if __name__ == "__main__":
    main()