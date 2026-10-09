from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REJECTED_DATA_DIR = DATA_DIR / "rejected"

# Input and output files
RAW_SALES_FILE = RAW_DATA_DIR / "sales.csv"
CLEAN_SALES_FILE = PROCESSED_DATA_DIR / "sales_clean.csv"
REJECTED_SALES_FILE = REJECTED_DATA_DIR / "sales_rejected.csv"

# Database
DATABASE_FILE = DATA_DIR / "sales.db"

# Logs
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

# Ensure required output directories exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)