import os
from dotenv import load_dotenv
import gspread
from gspread.exceptions import APIError

# Load environment variables from .env
load_dotenv()

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON")

if not SPREADSHEET_ID or not SERVICE_ACCOUNT_JSON:
    raise RuntimeError("❌ Missing spreadsheet ID or service account JSON path in .env")

try:
    # Authenticate using service account
    client = gspread.service_account(filename=SERVICE_ACCOUNT_JSON)

    # Open the spreadsheet
    sh = client.open_by_key(SPREADSHEET_ID)

    # Get the first worksheet
    worksheet = sh.get_worksheet(0)

    # Write a test message in cell A1
    worksheet.update_cell(1, 1, "Hello from AI-WORKFLOW!")

    print("✅ Successfully wrote to the sheet!")

except APIError as e:
    print("❌ APIError:", e)

except Exception as e:
    print("❌ Something went wrong:", e)
