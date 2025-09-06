from __future__ import annotations
import argparse
from typing import List, Dict, Any
from .config import SETTINGS, require_config
from .discovery import discover_and_enrich
from .enrich import enrich_records
from .scoring import score_record
from .exporters import to_csv, to_google_sheets

try:
    from openai import OpenAI
except Exception:  # optional
    OpenAI = None  # type: ignore


def maybe_generate_notes(rows: List[Dict[str, Any]]) -> None:
    if not SETTINGS.openai_api_key or OpenAI is None:
        for r in rows:
            r["notes"] = ""
        return
    client = OpenAI(api_key=SETTINGS.openai_api_key)
    for r in rows:
        prompt = (
            f"Company: {r.get('name')}\n"
            f"Industry: {r.get('industry')}\n"
            f"Website: {r.get('website')}\n"
            f"Signals: L&D={r.get('has_ld_signals')}\n"
            f"Write a 1-line seller note for Coursera B2B outreach."
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=50,
            )
            r["notes"] = resp.choices[0].message.content.strip()
        except Exception:
            r["notes"] = ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Coursera B2B Lead Pipeline")
    parser.add_argument("--query", required=True, help="Discovery query, e.g., 'learning and development'")
    parser.add_argument("--industry", default=None, help="Optional industry hint to include in search")
    parser.add_argument("--min_employees", type=int, default=0, help="Minimum employee estimate to include")
    args = parser.parse_args()

    require_config()

    query = args.query if not args.industry else f"{args.query} {args.industry}"

    # 1) Discover + details
    discovered = discover_and_enrich(query, SETTINGS.target_cities)

    # 2) Heuristic enrichment
    enriched = enrich_records(discovered)

    # Filter by min employees estimate if provided
    filtered = [r for r in enriched if (r.get("employees_est") or 0) >= args.min_employees]

    # 3) Scoring
    for r in filtered:
        s, breakdown = score_record(r)
        r["score"] = round(s, 2)
        r["score_breakdown"] = breakdown

    # 4) Optional LLM notes
    maybe_generate_notes(filtered)

    # 5) Export
    to_csv(filtered, "output/leads.csv")
    to_google_sheets(filtered)

    print(f"Done. {len(filtered)} leads exported to output/leads.csv and Google Sheets.")


if __name__ == "__main__":
    main()