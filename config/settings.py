import os

# Project Root Directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Logging Configuration
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
LOG_LEVEL = "INFO"  # Change to DEBUG for detailed logs

# Data Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
TICKERS_FILE = os.path.join(DATA_DIR, "nse_tickers.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "sqglp_results.csv")
HISTORICAL_DATA_FILE = os.path.join(DATA_DIR, "historical_data.csv")

# Default Stock Selection Criteria
MARKET_CAP_LIMIT = 5000  # In Crores
MAX_TICKERS = 50  # Maximum number of stocks to fetch dynamically

# Streamlit Dashboard Config
DEFAULT_SECTOR_FILTER = "All"
DEFAULT_SORT_COLUMN = "SQGLP_Score"
DEFAULT_SORT_ORDER = "descending"

# SQGLP Scoring Weights (Adjustable for Custom Weighting)
WEIGHTS = {
    "Revenue Growth": 0.25,
    "Earnings Growth": 0.25,
    "ROIC": 0.20,
    "Market Cap (Cr)": 0.10,
    "Debt-to-Equity": 0.05,
    "P/E Ratio": 0.05,
    "Dividend Yield": 0.05,
    "Price-to-Sales (P/S)": 0.05
}

# Predictive Growth Score (PGS) Configuration
PGS_LOOKBACK_YEARS = 5  # How many years to consider for historical trend analysis

# Visualization Settings
HEATMAP_COLOR_SCALE = "Viridis"  # Options: Plasma, Inferno, Magma, Viridis, etc.

# API Settings (if needed for external data fetching)
YAHOO_FINANCE_API_ENABLED = True

# Debug Mode
DEBUG = False  # Set to True to enable detailed error logging