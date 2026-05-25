# Campania Rental Intelligence Platform

Real estate monitoring and rental intelligence platform focused on tourism and rental market signals in Campania, Italy.

The project uses Python automation, SerpAPI, Pandas, rule-based scoring, classification logic, Plotly dashboards, and dashboard-ready datasets to monitor rental opportunities and tourism-related property signals.

Main goals:
- monitor rental and tourism-related market activity
- aggregate structured datasets from online sources
- filter and classify property-related signals
- generate analytical summaries and dashboards
- prepare content-ready datasets for reporting and social workflows

---

## What This Project Demonstrates

This project demonstrates practical data automation and intelligence workflow skills.

Key skills shown:
- collecting data from online sources using APIs and search automation
- cleaning and structuring search results with Pandas
- filtering duplicate and low-quality links
- applying rule-based scoring and classification logic
- generating CSV datasets and analytical reports
- preparing ready-to-use content for social media workflows
- building dashboard-ready datasets for monitoring and reporting

---

## Technologies Used

- Python
- Pandas
- Requests
- SerpAPI
- Plotly
- Streamlit
- CSV Data Pipelines
- Rule-Based Scoring
- Dashboard Analytics

---

## Workflow

Search queries
↓
Google / SerpAPI collection
↓
Data cleaning and filtering
↓
Duplicate removal
↓
Scoring and classification
↓
CSV exports
↓
Dashboard-ready datasets
↓
Interactive dashboards and reporting

---

## Project Structure

```bash
campania-rental-intelligence/
│
├── agent.py
├── scoring.py
├── classifier.py
├── post_generator.py
├── dashboard_data.py
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw_results.csv
│   ├── filtered_results.csv
│   ├── scored_results.csv
│   └── dashboard_dataset.csv
│
├── screenshots/
│   ├── csv_preview.png
│   ├── streamlit_dashboard.png
│   └── terminal_run.png
│
├── output/
│   ├── generated_posts.csv
│   └── reports.csv
│
└── .env
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Environment Variables

```env
SERPAPI_API_KEY=your_api_key_here
```

---

## Run Pipeline

Run data collection:

```bash
python3 agent.py
```

Run scoring and classification:

```bash
python3 scoring.py
```

Generate posts and reports:

```bash
python3 post_generator.py
```

Prepare dashboard datasets:

```bash
python3 dashboard_data.py
```

Launch interactive dashboard:

```bash
streamlit run app.py
```

---

## Key Features

- Rental market monitoring
- Tourism-related signal tracking
- Structured search result aggregation
- Duplicate filtering workflows
- Rule-based scoring system
- Dashboard-ready CSV exports
- Interactive Plotly dashboards
- Automated content preparation

---

## Example Screenshots

### CSV Data Preview

![CSV Preview](screenshots/csv_preview.png)

### Streamlit Dashboard

![Dashboard](screenshots/streamlit_dashboard.png)

---

## Business Use Cases

- short-term rental market monitoring
- tourism-oriented property research
- real estate lead generation
- competitor and source monitoring
- social media content preparation
- local market intelligence dashboards

---

## Responsible Use

This project is intended for educational, analytical, and portfolio purposes only.

It does not scrape private data, does not bypass authentication, and does not collect personal information. The system works with publicly accessible search results and structured datasets.

---

## Future Improvements

- Automated scheduled monitoring
- Geographic rental mapping
- Trend anomaly detection
- Telegram notification workflows
- Real-time dashboard updates
- AI-assisted market summaries

---

## Author

Yurii Vasylenko