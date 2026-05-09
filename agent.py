import requests
import pandas as pd
from urllib.parse import urlparse
from classifier import add_categories_to_deals

from config import (
    SERPAPI_API_KEY,
    SEARCH_QUERIES,
    ALLOWED_DOMAINS,
    RAW_DEALS_FILE,
    SCORED_DEALS_FILE,
)

from scoring import add_scores_to_deals


def is_allowed_domain(link):
    domain = urlparse(link).netloc.lower()

    for allowed in ALLOWED_DOMAINS:
        if allowed in domain:
            return True

    return False


def search_google(query):
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 10,
        "hl": "it",
        "gl": "it",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    results = []

    for item in data.get("organic_results", []):
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")

        if not link:
            continue

        if not is_allowed_domain(link):
            continue

        results.append({
            "query": query,
            "title": title,
            "snippet": snippet,
            "link": link,
            "domain": urlparse(link).netloc.lower(),
        })

    return results


def remove_duplicates(df):
    if "link" in df.columns:
        df = df.drop_duplicates(subset=["link"])

    return df


def main():
    all_results = []

    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")

        try:
            results = search_google(query)
            all_results.extend(results)
        except Exception as e:
            print(f"Error with query: {query}")
            print(e)

    if not all_results:
        print("No results found.")
        return

    df = pd.DataFrame(all_results)

    df = remove_duplicates(df)

    df.to_csv(RAW_DEALS_FILE, index=False)
    print(f"Raw deals saved to: {RAW_DEALS_FILE}")

    df = add_scores_to_deals(df)
    df = add_categories_to_deals(df)

    df = df.sort_values(by="intelligence_score", ascending=False)

    df.to_csv(SCORED_DEALS_FILE, index=False)
    print(f"Scored deals saved to: {SCORED_DEALS_FILE}")

    print("Done.")
    print(df[["title", "domain", "intelligence_score", "score_reasons"]].head(10))


if __name__ == "__main__":
    main()