from __future__ import annotations
from typing import Dict, Any, List
import re

# Simple heuristics to infer industry and L&D presence signals

IT_KEYWORDS = ["software", "it", "technology", "info tech", "saas", "cloud", "analytics", "ai", "data"]
LND_KEYWORDS = ["learning", "training", "l&d", "human resources", "hr", "people development", "upskilling"]


def _normalize_industry_from_types(types: List[str] | None) -> str | None:
    if not types:
        return None
    t = " ".join(types).lower()
    if any(k in t for k in ["university", "school", "college"]):
        return "Education"
    if any(k in t for k in ["hospital", "health"]):
        return "Healthcare"
    if any(k in t for k in ["bank", "finance"]):
        return "Financial Services"
    if any(k in t for k in ["software", "it", "technology"]):
        return "Information Technology"
    return None


def infer_industry(name: str | None, types: List[str] | None) -> str | None:
    # Types first
    industry = _normalize_industry_from_types(types)
    if industry:
        return industry
    # Name-based heuristic
    if name:
        n = name.lower()
        if any(k in n for k in IT_KEYWORDS):
            return "Information Technology"
    return None


def has_ld_signals(name: str | None, website: str | None) -> bool:
    text = f"{name or ''} {website or ''}".lower()
    return any(k in text for k in LND_KEYWORDS)


def estimate_employees_from_name(name: str | None) -> int | None:
    # Placeholder heuristic: look for patterns like "Pvt Ltd", "Solutions", etc. Not reliable; kept minimal.
    if not name:
        return None
    if re.search(r"(labs|solutions|systems|technologies|global)", name.lower()):
        return 200  # assume mid-size for prioritization demo
    return None


def enrich_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    seen_domains: set[str] = set()
    for r in records:
        industry = infer_industry(r.get("name"), r.get("types"))
        employees_est = estimate_employees_from_name(r.get("name"))
        ld = has_ld_signals(r.get("name"), r.get("website"))
        # dedupe by website domain if present
        website = r.get("website")
        if website:
            domain = re.sub(r"^https?://", "", website).split("/")[0].lower()
            if domain in seen_domains:
                continue
            seen_domains.add(domain)
        out.append({
            **r,
            "industry": industry,
            "employees_est": employees_est,
            "has_ld_signals": ld,
        })
    return out