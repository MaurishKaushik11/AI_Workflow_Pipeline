import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    google_places_api_key: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
    google_sheets_spreadsheet_id: str = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    google_sheets_service_account_json: str = os.getenv(
        "GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON", "credentials/service_account.json"
    )
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    target_cities: list[str] = tuple(
        c.strip() for c in os.getenv("TARGET_CITIES", "Delhi NCR").split(",") if c.strip()
    )

    # Discovery defaults
    discovery_radius_m: int = int(os.getenv("DISCOVERY_RADIUS_M", "30000"))  # 30km
    max_results_per_city: int = int(os.getenv("MAX_RESULTS_PER_CITY", "120"))

    # Scoring weights
    weight_has_ld: float = float(os.getenv("WEIGHT_HAS_LD", "4.0"))
    weight_size: float = float(os.getenv("WEIGHT_SIZE", "3.0"))
    weight_industry_fit: float = float(os.getenv("WEIGHT_INDUSTRY_FIT", "2.0"))
    weight_contactability: float = float(os.getenv("WEIGHT_CONTACTABILITY", "1.0"))


SETTINGS = Settings()


def require_config() -> None:
    missing = []
    if not SETTINGS.google_places_api_key:
        missing.append("GOOGLE_PLACES_API_KEY")
    if not SETTINGS.google_sheets_spreadsheet_id:
        missing.append("GOOGLE_SHEETS_SPREADSHEET_ID")
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. Configure your .env."
        )