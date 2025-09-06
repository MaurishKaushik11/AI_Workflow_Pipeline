import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load .env
load_dotenv()

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON")

# Authenticate
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
)
client = gspread.authorize(creds)

# Open the spreadsheet and select worksheet
sh = client.open_by_key(SPREADSHEET_ID)
try:
    worksheet = sh.worksheet("Leads")
except gspread.WorksheetNotFound:
    worksheet = sh.add_worksheet(title="Leads", rows="1000", cols="10")

# Append rows
worksheet.append_rows([
    ["Name", "Company", "Industry", "Employees"],
    ["Test Lead", "Test Company", "IT", 200]
], value_input_option='RAW')

print("✅ Successfully appended rows to the sheet!")
