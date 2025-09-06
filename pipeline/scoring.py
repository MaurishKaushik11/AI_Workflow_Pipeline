from __future__ import annotations
from typing import Dict, Any
from .config import SETTINGS


def score_record(r: Dict[str, Any]) -> tuple[float, str]:
    score = 0.0
    parts: list[str] = []

    # L&D presence
    if r.get("has_ld_signals"):
        score += SETTINGS.weight_has_ld
        parts.append(f"L&D signals (+{SETTINGS.weight_has_ld})")

    # Size estimate
    emp = r.get("employees_est") or 0
    if emp >= 1000:
        s = SETTINGS.weight_size
    elif emp >= 200:
        s = SETTINGS.weight_size * 0.7
    elif emp >= 50:
        s = SETTINGS.weight_size * 0.4
    else:
        s = 0.0
    score += s
    if s:
        parts.append(f"Size tier (+{s:.1f})")

    # Industry fit (IT, FS, etc.)
    industry = (r.get("industry") or "").lower()
    if any(k in industry for k in ["information technology", "financial", "professional services", "education"]):
        score += SETTINGS.weight_industry_fit
        parts.append(f"Industry fit (+{SETTINGS.weight_industry_fit})")

    # Contactability: has website or phone
    if r.get("website") or r.get("phone"):
        score += SETTINGS.weight_contactability
        parts.append(f"Contactable (+{SETTINGS.weight_contactability})")

    return score, "; ".join(parts) if parts else ""