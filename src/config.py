import os
from pathlib import Path

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/flyrank/the-polite-scraper)"
REQUEST_TIMEOUT = 8
POLITENESS_DELAY = 0.5

# Directories
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
