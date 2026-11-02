"""Provisional keyword rule for the candidate deepfake subset (not an approved definition)."""
from __future__ import annotations

import re
import unicodedata

import pandas as pd

from .config import DEEPFAKE_RULE_VERSION

FIELDS = ["Implicated Systems", "title", "description"]
PATTERN = re.compile(r"\bdeep[\s-]?fakes?\b", re.IGNORECASE)
_DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).translate(_DASHES)


def find_matches(incidents: pd.DataFrame) -> pd.DataFrame:
    """One row per (Incident ID, field, term) with an excerpt. Raw text is untouched."""
    rows = []
    for field in FIELDS:
        if field not in incidents:
            continue
        for iid, raw in zip(incidents["Incident ID"], incidents[field]):
            if not isinstance(raw, str):  # missing text is skipped, never evidence of absence
                continue
            norm = normalize(raw)
            for m in PATTERN.finditer(norm):
                lo, hi = max(0, m.start() - 60), min(len(norm), m.end() + 60)
                rows.append({"Incident ID": iid, "field": field, "term": m.group(0),
                             "excerpt": norm[lo:hi].replace("\n", " "),
                             "rule_version": DEEPFAKE_RULE_VERSION})
    return pd.DataFrame(rows, columns=["Incident ID", "field", "term", "excerpt", "rule_version"])


def candidate_ids(evidence: pd.DataFrame) -> set:
    return set(evidence["Incident ID"].unique())
