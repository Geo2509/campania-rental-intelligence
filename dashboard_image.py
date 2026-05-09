import pandas as pd
import matplotlib.pyplot as plt

from config import SCORED_DEALS_FILE


OUTPUT_IMAGE = "output/dashboard.png"


def main():
    df = pd.read_csv(SCORED_DEALS_FILE)

    total_deals = len(df)
    average_score = round(df["intelligence_score"].mean(), 1)

    top_domain = df["domain"].value_counts().idxmax()
    top_category = df["deal_category"].value_counts().idxmax()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.axis("off")

    dashboard_text = f"""
Campania Rental Intelligence Dashboard

Total offers found: {total_deals}

Average intelligence score: {average_score}/100

Top source domain:
{top_domain}

Top property category:
{top_category}

Monitored locations:
• Procida
• Ischia
• Capri
• Bacoli
• Monte di Procida

Workflow:
Search → Filter → Score → Classify → Analyze → Generate Posts

Built with:
Python · pandas · SerpAPI · Automation
"""

    ax.text(
        0.05,
        0.95,
        dashboard_text,
        fontsize=16,
        verticalalignment="top",
        family="DejaVu Sans"
    )

    plt.tight_layout()

    plt.savefig(OUTPUT_IMAGE, dpi=200)

    print(f"Dashboard saved to: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()