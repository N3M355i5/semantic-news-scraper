from pathlib import Path

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

COMPANY_DATA_FOLDER = BASE_DIR / "data" / "companies"

# ==========================================
# DATABASE
# ==========================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "lead_intelligence",
    "user": "postgres",
    "password": "admin"
}

# ==========================================
# RSS SETTINGS
# ==========================================

RSS_RESULTS_PER_QUERY = 50

MAX_ARTICLES_PER_COMPANY = 10

RSS_TIMEOUT = 20

# ==========================================
# SEARCH SETTINGS
# ==========================================

MAX_SEARCH_QUERIES = 3

# ==========================================
# EXTRACTION SETTINGS
# ==========================================

USER_AGENT = (
    "Mozilla/5.0 SemanticNewsScraper"
)

REQUEST_TIMEOUT = 30