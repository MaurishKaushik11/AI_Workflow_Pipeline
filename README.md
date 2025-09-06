# Coursera B2B Lead Discovery – Delhi NCR (Google Places + Google Sheets)

This project implements a minimal, working AI agent workflow to discover, enrich, score, and export leads for Coursera’s workforce upskilling outreach.

- **Cities**: Delhi NCR (easily extensible)
- **Discovery Source**: Google Places API (Text Search + Place Details)
- **Output**: Google Sheets (and local CSV)
- **LLM usage**: Optional lightweight normalization and notes generation

## Quick Start (10–15 minutes)

1. Create API credentials:
   - **Google Places API key**: From Google Cloud Console → Enable Places API → Create API Key.
   - **Google Service Account JSON** for Sheets: Create a service account, enable Google Sheets API & Drive API, create a key, download JSON.
2. Save credentials:
   - Put your Places key into `.env`:
     ```env
     GOOGLE_PLACES_API_KEY=YOUR_PLACES_KEY
     GOOGLE_SHEETS_SPREADSHEET_ID=REPLACE_WITH_SHEET_ID
     GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON=credentials/service_account.json
     TARGET_CITIES=Delhi NCR
     # Optional LLM (e.g., OpenAI)
     OPENAI_API_KEY=
     ```
   - Place the service account JSON at `credentials/service_account.json`.
   - Share your target Google Sheet with the service account email.
3. Install dependencies:
   ```bash
   # PowerShell compatible commands
   python -m venv .venv
   .\.venv\Scripts\pip install -r requirements.txt
   ```
4. Run the pipeline:
   ```bash
   .\.venv\Scripts\python pipeline\run_pipeline.py --query "learning and development" --industry "IT" --min_employees 200
   ```

The pipeline will:
- Discover companies via Google Places (Delhi NCR) using keyword queries
- Enrich with Place Details (website, phone, address)
- Heuristically infer industry and size when available
- Score leads using transparent rules
- Save results to `output/leads.csv` and update your Google Sheet

## Structure

```
pipeline/
  config.py
  discovery.py
  enrich.py
  scoring.py
  exporters.py
  run_pipeline.py
requirements.txt
.env (create locally)
credentials/service_account.json (add)
output/ (generated)
```

## Design Notes

- **Deterministic code**: data fetching, transformations, rule-based scoring, validation, and deduplication are deterministic.
- **LLM usage (optional)**: normalize industry labels, summarize public info into a one-liner note. If no `OPENAI_API_KEY`, these steps are skipped.
- **APIs**:
  - Google Places Text Search and Place Details.
  - Google Sheets via service account.
- **Guardrails**:
  - Rate limiting and retries for Google APIs.
  - Input validation, required fields, and schema enforcement.
  - Domain-based dedupe and name+address fuzzy matching.
  - Configurable city and query whitelists.
- **Data model**: columns include `name, city, industry, employees_est, has_ld_signals, website, phone, address, google_place_id, score, score_breakdown, notes`.

## Extend

- Add Apollo/G2/Crunchbase modules for deeper enrichment when credentials are available.
- Add CRM export (Salesforce/HubSpot) in `exporters.py`.
- Add priority queues or webhooks for sales alerts.

## Troubleshooting

- 403/REQUEST_DENIED: Ensure Places API is enabled and key is unrestricted or properly restricted.
- Sheets write fails: Share the sheet with the service account email, ensure correct spreadsheet ID.
- Low results: Tweak `--query`, add synonyms, or broaden city radius in `discovery.py`.