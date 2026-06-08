import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Path to dengue case CSV (should be set in .env as DENGUE_CASES_PATH)
CASE_CSV_PATH = os.getenv("DENGUE_CASES_PATH")

def load_cases() -> pd.DataFrame:
    """Load dengue case data.
    Expected columns: ['date', 'district', 'cases']
    """
    if not CASE_CSV_PATH or not os.path.exists(CASE_CSV_PATH):
        raise FileNotFoundError("DENGUE_CASES_PATH not set or file does not exist.")
    df = pd.read_csv(CASE_CSV_PATH, parse_dates=["date"])
    return df
