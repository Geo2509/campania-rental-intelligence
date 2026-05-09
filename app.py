import streamlit as st
import pandas as pd

from config import SCORED_DEALS_FILE


st.set_page_config(
    page_title="Campania Rental Intelligence",
    page_icon="🏡",
    layout="wide"
)


def detect_location(text):
    text = str(text).lower()

    if "capri" in text:
        return "Capri"
    if "ischia" in text:
        return "Ischia"
    if "monte di procida" in text:
        return "Monte di Procida"
    if "procida" in text:
        return "Procida"
    if "bacoli" in text:
        return "Bacoli"

    return "Other"


@st.cache_data
def load_data():
    df = pd.read_csv(SCORED_DEALS_FILE)

    df["location"] = df.apply(
        lambda row: detect_location(
            f"{row.get('title', '')} {row.get('snippet', '')} {row.get('link', '')}"
        ),
        axis=1
    )

    return df


df = load_data()

st.title("🏡 Campania Rental Intelligence Dashboard")
st.caption("AI-powered rental monitoring and property intelligence platform for Campania, Italy")

# Sidebar filters
st.sidebar.header("Filters")

locations = ["All"] + sorted(df["location"].unique().tolist())
selected_location = st.sidebar.selectbox("Location", locations)

categories = ["All"] + sorted(df["deal_category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

min_score = st.sidebar.slider(
    "Minimum intelligence score",
    min_value=0,
    max_value=100,
    value=0
)

filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["deal_category"] == selected_category]

filtered_df = filtered_df[filtered_df["intelligence_score"] >= min_score]

filtered_df = filtered_df.sort_values(
    by="intelligence_score",
    ascending=False
)

# KPI section
total_offers = len(filtered_df)
average_score = round(filtered_df["intelligence_score"].mean(), 1) if total_offers > 0 else 0
top_location = filtered_df["location"].value_counts().idxmax() if total_offers > 0 else "N/A"
top_category = filtered_df["deal_category"].value_counts().idxmax() if total_offers > 0 else "N/A"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Offers", total_offers)
col2.metric("Average Score", average_score)
col3.metric("Top Location", top_location)
col4.metric("Top Category", top_category)

st.divider()

# Main table
st.subheader("📌 Top Rental Offers")

st.dataframe(
    filtered_df[
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
    width="stretch",
    hide_index=True
)

st.divider()

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📍 Offers by Location")
    location_counts = filtered_df["location"].value_counts()
    st.bar_chart(location_counts)

with chart_col2:
    st.subheader("🏷 Offers by Category")
    category_counts = filtered_df["deal_category"].value_counts()
    st.bar_chart(category_counts)

st.divider()

st.subheader("🌍 Top Source Domains")
domain_counts = filtered_df["domain"].value_counts().head(10)
st.bar_chart(domain_counts)

st.divider()

# Cards
st.subheader("⭐ Top 5 High-Scoring Offers")

top_5 = filtered_df.head(5)

for _, row in top_5.iterrows():
    with st.container(border=True):
        st.markdown(f"### {row['title']}")
        c1, c2, c3 = st.columns(3)

        c1.metric("Score", f"{row['intelligence_score']}/100")
        c2.write(f"**Location:** {row['location']}")
        c3.write(f"**Category:** {row['deal_category']}")

        st.write(f"**Source:** {row['domain']}")
        st.write(f"**Why selected:** {row['score_reasons']}")
        st.link_button("Open Listing", row["link"])