import streamlit as st
import pandas as pd

from config import SCORED_DEALS_FILE


st.set_page_config(
    page_title="Campania Rental Intelligence",
    layout="wide"
)


def detect_location(text):
    text = str(text).lower()

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

    return "Other"


def create_rule_based_summary(row):
    location = row.get("location", "Campania")
    category = row.get("deal_category", "general")
    score = row.get("intelligence_score", 0)
    reasons = row.get("score_reasons", "")

    if score >= 70:
        strength = "high-priority"
    elif score >= 40:
        strength = "medium-priority"
    else:
        strength = "low-priority"

    return (
        f"{strength.capitalize()} rental signal in {location}. "
        f"Category: {category}. "
        f"Main indicators: {reasons}."
    )


@st.cache_data
def load_data():
    df = pd.read_csv(SCORED_DEALS_FILE)

    df["location"] = df.apply(
        lambda row: detect_location(
            f"{row.get('title', '')} {row.get('snippet', '')} {row.get('link', '')}"
        ),
        axis=1
    )

    df["summary"] = df.apply(create_rule_based_summary, axis=1)

    return df


df = load_data()

st.markdown("""
# 🏡 Campania Rental Intelligence
### AI-powered rental monitoring dashboard for Campania, Italy
""")


st.sidebar.header("Filters")

locations = sorted(df["location"].dropna().unique())
selected_locations = st.sidebar.multiselect(
    "Location",
    locations,
    default=locations
)

categories = sorted(df["deal_category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

min_score = st.sidebar.slider(
    "Minimum intelligence score",
    min_value=0,
    max_value=100,
    value=0
)

domains = sorted(df["domain"].dropna().unique())
selected_domains = st.sidebar.multiselect(
    "Source domain",
    domains,
    default=domains
)

filtered_df = df[
    (df["location"].isin(selected_locations)) &
    (df["deal_category"].isin(selected_categories)) &
    (df["intelligence_score"] >= min_score) &
    (df["domain"].isin(selected_domains))
]

top_df = filtered_df.sort_values(
    by="intelligence_score",
    ascending=False
)

total_offers = len(filtered_df)

if total_offers > 0:
    average_score = round(filtered_df["intelligence_score"].mean(), 1)
    max_score = int(filtered_df["intelligence_score"].max())
    top_location = filtered_df["location"].value_counts().idxmax()
else:
    average_score = 0
    max_score = 0
    top_location = "N/A"


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Offers", total_offers)

with col2:
    st.metric("Average Score", average_score)

with col3:
    st.metric("Max Score", max_score)

with col4:
    st.metric("Top Location", top_location)


tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overview", "🏡 Offers", "⭐ Top Signals", "🧠 Summaries"]
)


with tab1:
    st.subheader("Category Distribution")

    if not filtered_df.empty:
        st.bar_chart(filtered_df["deal_category"].value_counts())
    else:
        st.warning("No offers match the selected filters.")

    st.subheader("Location Distribution")

    if not filtered_df.empty:
        st.bar_chart(filtered_df["location"].value_counts())

    st.subheader("Top Source Domains")

    if not filtered_df.empty:
        st.bar_chart(filtered_df["domain"].value_counts())


with tab2:
    st.subheader("Filtered Rental Offers")

    if not top_df.empty:
        st.dataframe(
            top_df[
                [
                    "title",
                    "location",
                    "domain",
                    "intelligence_score",
                    "deal_category",
                    "score_reasons",
                    "link",
                ]
            ],
            width="stretch"
        )
    else:
        st.warning("No offers available.")


with tab3:
    st.subheader("Top 5 High-Scoring Rental Signals")

    top_5 = top_df.head(5)

    if not top_5.empty:
        for _, row in top_5.iterrows():
            st.markdown(f"""
### {row['title']}

**Location:** {row['location']}  
**Score:** {row['intelligence_score']}/100  
**Category:** {row['deal_category']}  
**Source:** {row['domain']}  
**Signals:** {row['score_reasons']}  

[Open Listing]({row['link']})
""")
            st.divider()
    else:
        st.warning("No top signals available.")


with tab4:
    st.subheader("Rule-Based Intelligence Summaries")

    if not top_df.empty:
        for _, row in top_df.head(10).iterrows():
            st.markdown(f"""
### {row['location']} — Score {row['intelligence_score']}/100

{row['summary']}

[Open Listing]({row['link']})
""")
            st.divider()
    else:
        st.warning("No summaries available.")