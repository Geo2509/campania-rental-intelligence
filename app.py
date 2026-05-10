import streamlit as st
import pandas as pd
import plotly.express as px

from config import SCORED_DEALS_FILE


st.set_page_config(
    page_title="Campania Rental Intelligence",
    page_icon="🏡",
    layout="wide"
)


def detect_location(text):
    text = str(text).lower()

    if "monte di procida" in text:
        return "Monte di Procida"
    if "capri" in text:
        return "Capri"
    if "ischia" in text:
        return "Ischia"
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

st.markdown("""
# 🏡 Campania Rental Intelligence
### AI-powered rental monitoring dashboard for Campania, Italy
""")

st.sidebar.header("Filters")

locations = ["All"] + sorted(df["location"].unique().tolist())
selected_location = st.sidebar.selectbox("Location", locations)

categories = ["All"] + sorted(df["deal_category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

domains = ["All"] + sorted(df["domain"].unique().tolist())
selected_domain = st.sidebar.selectbox("Source domain", domains)

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

if selected_domain != "All":
    filtered_df = filtered_df[filtered_df["domain"] == selected_domain]

filtered_df = filtered_df[filtered_df["intelligence_score"] >= min_score]

filtered_df = filtered_df.sort_values(
    by="intelligence_score",
    ascending=False
)

total_offers = len(filtered_df)
average_score = round(filtered_df["intelligence_score"].mean(), 1) if total_offers > 0 else 0
max_score = int(filtered_df["intelligence_score"].max()) if total_offers > 0 else 0
top_location = filtered_df["location"].value_counts().idxmax() if total_offers > 0 else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Offers", total_offers)
kpi2.metric("Average Score", average_score)
kpi3.metric("Max Score", max_score)
kpi4.metric("Top Location", top_location)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overview", "🏡 Offers", "⭐ Top Signals", "🧠 Summaries"]
)

with tab1:
    st.subheader("Category Distribution")

    category_counts = (
        filtered_df["deal_category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = ["Category", "Count"]

    fig_category = px.bar(
        category_counts,
        x="Category",
        y="Count",
        text="Count",
        title="Offers by Category",
    )

    fig_category.update_traces(
        textposition="outside"
    )

    fig_category.update_layout(
        height=430,
        xaxis_title="Category",
        yaxis_title="Offers",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=60, b=40),
    )

    st.plotly_chart(fig_category, width="stretch")

    st.subheader("Location Distribution")

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .reset_index()
    )

    location_counts.columns = ["Location", "Count"]

    fig_location = px.bar(
        location_counts,
        x="Location",
        y="Count",
        text="Count",
        title="Offers by Location",
    )

    fig_location.update_traces(
        textposition="outside"
    )

    fig_location.update_layout(
        height=430,
        xaxis_title="Location",
        yaxis_title="Offers",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=60, b=40),
    )

    st.plotly_chart(fig_location, width="stretch")

    st.subheader("Top Source Domains")

    domain_counts = (
        filtered_df["domain"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    domain_counts.columns = ["Domain", "Count"]

    fig_domains = px.bar(
        domain_counts,
        x="Count",
        y="Domain",
        orientation="h",
        text="Count",
        title="Top Source Domains",
    )

    fig_domains.update_traces(
        textposition="outside"
    )

    fig_domains.update_layout(
        height=500,
        xaxis_title="Offers",
        yaxis_title="Domain",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=60, b=40),
    )

    st.plotly_chart(fig_domains, width="stretch")


with tab2:
    st.subheader("Filtered Rental Offers")

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


with tab3:
    st.subheader("Top 5 High-Scoring Rental Signals")

    top_5 = filtered_df.head(5)

    for _, row in top_5.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['title']}")

            c1, c2, c3 = st.columns(3)

            c1.metric("Score", f"{row['intelligence_score']}/100")
            c2.write(f"**Location:** {row['location']}")
            c3.write(f"**Category:** {row['deal_category']}")

            st.write(f"**Source:** {row['domain']}")
            st.write(f"**Signals:** {row['score_reasons']}")
            st.link_button("Open Listing", row["link"])


with tab4:
    st.subheader("Rule-Based Intelligence Summaries")

    summary_df = filtered_df.head(10)

    for _, row in summary_df.iterrows():
        score = row["intelligence_score"]

        if score >= 70:
            priority = "High-priority"
        elif score >= 40:
            priority = "Medium-priority"
        else:
            priority = "Low-priority"

        st.markdown(f"""
### {row['location']} — Score {score}/100

{priority} rental signal in **{row['location']}**.  
Category: **{row['deal_category']}**.  
Main indicators: **{row['score_reasons']}**.

[Open Listing]({row['link']})
---
""")