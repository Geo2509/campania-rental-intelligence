import pandas as pd

from config import SCORED_DEALS_FILE, ANALYTICS_REPORT_FILE


def main():
    df = pd.read_csv(SCORED_DEALS_FILE)

    total_deals = len(df)
    average_score = round(df["intelligence_score"].mean(), 1)

    top_domains = df["domain"].value_counts().head(5)
    top_categories = df["deal_category"].value_counts().head(5)

    report = []
    report.append("Campania Rental Intelligence Report")
    report.append("=" * 40)
    report.append("")
    report.append(f"Total offers found: {total_deals}")
    report.append(f"Average intelligence score: {average_score}/100")
    report.append("")
    report.append("Top source domains:")
    for domain, count in top_domains.items():
        report.append(f"- {domain}: {count}")

    report.append("")
    report.append("Top categories:")
    for category, count in top_categories.items():
        report.append(f"- {category}: {count}")

    report.append("")
    report.append("Top 10 offers:")
    top_10 = df.head(10)

    for _, row in top_10.iterrows():
        report.append("")
        report.append(f"Title: {row.get('title', '')}")
        report.append(f"Domain: {row.get('domain', '')}")
        report.append(f"Score: {row.get('intelligence_score', '')}/100")
        report.append(f"Category: {row.get('deal_category', '')}")
        report.append(f"Reasons: {row.get('score_reasons', '')}")
        report.append(f"Link: {row.get('link', '')}")

    with open(ANALYTICS_REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print(f"Report saved to: {ANALYTICS_REPORT_FILE}")


if __name__ == "__main__":
    main()