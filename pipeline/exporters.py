from __future__ import annotations
import os
import pandas as pd
from typing import List, Dict, Any
import gspread
from google.oauth2.service_account import Credentials

from .config import SETTINGS

# Define the columns for CSV/Sheets
COLUMNS = [
    "name",
    "city",
    "industry",
    "employees_est",
    "has_ld_signals",
    "website",
    "phone",
    "address",
    "google_place_id",
    "score",
    "score_breakdown",
    "notes",
]

def to_csv(rows: List[Dict[str, Any]], path: str) -> str:
    """
    Export leads to a CSV file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(rows, columns=COLUMNS)
    df.to_csv(path, index=False)
    return path

def to_google_sheets(rows: List[Dict[str, Any]]) -> None:
    """
    Export leads to Google Sheets.
    """
    # Authenticate using service account
    creds = Credentials.from_service_account_file(
        SETTINGS.google_sheets_service_account_json,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    client = gspread.authorize(creds)
    sh = client.open_by_key(SETTINGS.google_sheets_spreadsheet_id)

    # Get or create the "Leads" worksheet
    try:
        ws = sh.worksheet("Leads")
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="Leads", rows="1000", cols=str(len(COLUMNS)))

    # Prepare data: header + rows
    data = [COLUMNS] + [[row.get(c, "") for c in COLUMNS] for row in rows]

    # Append rows (works even if sheet is empty)
    ws.append_rows(data, value_input_option="RAW")
