from pathlib import Path

# Base project directory (two levels up from this file: /app/data -> project root)
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "DATA"

# CSV dataset files (kept for reference)
CYBER_INCIDENTS_CSV = DATA_DIR / "cyber_incidents.csv"
DATASETS_METADATA_CSV = DATA_DIR / "datasets_metadata.csv"
IT_TICKETS_CSV = DATA_DIR / "it_tickets.csv"

# Database file used by this project
cyber_incidents = DATA_DIR / "intelligence_platform.db"

# Backwards-compatible alias: some modules import `datasets_metadata.cyber_incidents`
# which is expected to be a Path-like pointing to the DB used for incidents.
