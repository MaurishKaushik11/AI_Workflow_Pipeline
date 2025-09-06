from __future__ import annotations
import time
import requests
from typing import Iterable, List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .config import SETTINGS

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def _get(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("status") not in {"OK", "ZERO_RESULTS", "OVER_QUERY_LIMIT", "INVALID_REQUEST", "UNKNOWN_ERROR"}:
        # Surface other statuses early
        raise RuntimeError(f"Places API returned status={data.get('status')} error={data.get('error_message')}")
    return data


def discover_places_for_city(query: str, city: str) -> List[Dict[str, Any]]:
    """Use Places Text Search to find organizations for a query in a given city."""
    results: List[Dict[str, Any]] = []
    params = {
        "query": f"{query} in {city}",
        "key": SETTINGS.google_places_api_key,
        "type": "establishment",
    }

    while True:
        data = _get(PLACES_TEXT_SEARCH_URL, params)
        results.extend(data.get("results", []))
        next_page = data.get("next_page_token")
        if not next_page or len(results) >= SETTINGS.max_results_per_city:
            break
        time.sleep(2)  # Wait before using next_page_token
        params = {"pagetoken": next_page, "key": SETTINGS.google_places_api_key}

    return results[: SETTINGS.max_results_per_city]


def fetch_place_details(place_id: str) -> Dict[str, Any]:
    params = {
        "place_id": place_id,
        "key": SETTINGS.google_places_api_key,
        "fields": "name,formatted_address,international_phone_number,website,types"
    }
    data = _get(PLACE_DETAILS_URL, params)
    return data.get("result", {})


def discover_and_enrich(query: str, cities: Iterable[str]) -> List[Dict[str, Any]]:
    """Discover organizations then enrich with Place Details."""
    all_items: List[Dict[str, Any]] = []
    for city in cities:
        base = discover_places_for_city(query, city)
        for item in base:
            pid = item.get("place_id")
            details = fetch_place_details(pid) if pid else {}
            all_items.append({
                "name": details.get("name") or item.get("name"),
                "address": details.get("formatted_address") or item.get("formatted_address"),
                "phone": details.get("international_phone_number"),
                "website": details.get("website"),
                "types": details.get("types") or item.get("types"),
                "google_place_id": item.get("place_id"),
                "city": city,
            })
    return all_items