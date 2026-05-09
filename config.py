import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY не найден в .env")

SEARCH_QUERIES = [
    "Procida appartamento affitto breve estate",
    "Procida casa vacanza estate",
    "Ischia appartamento affitto breve estate",
    "Ischia casa vacanza mare",
    "Capri appartamento affitto breve estate",
    "Capri villa casa vacanza",
    "Bacoli appartamento affitto breve",
    "Bacoli casa vacanza mare",
    "Monte di Procida casa vacanza",
    "Monte di Procida appartamento affitto breve",
]

ALLOWED_DOMAINS = [
    "booking.com",
    "airbnb.",
    "casevacanza.it",
    "subito.it",
    "idealista.it",
    "immobiliare.it",
    "casa.it",
    "vrbo.com",
    "tripadvisor.",
]

DATA_DIR = "data"
OUTPUT_DIR = "output"

RAW_DEALS_FILE = f"{DATA_DIR}/raw_deals.csv"
CLEAN_DEALS_FILE = f"{DATA_DIR}/clean_deals.csv"
SCORED_DEALS_FILE = f"{DATA_DIR}/scored_deals.csv"
PUBLISHED_POSTS_FILE = f"{DATA_DIR}/published_posts.csv"

FACEBOOK_POSTS_FILE = f"{OUTPUT_DIR}/facebook_posts.txt"
ANALYTICS_REPORT_FILE = f"{OUTPUT_DIR}/analytics_report.txt"
