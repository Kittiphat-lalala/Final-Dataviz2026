"""Configuration, versions and design tokens (dashboard_style_handoff.md section 1)."""
from __future__ import annotations

import pandas as pd

DEEPFAKE_RULE_VERSION = "deepfake-keyword-v1 (provisional, review pending)"
QUALITY_POLICY_VERSION = "acsc-comparable-v1 (proposed, confirmation pending)"

# Input files: stem + extension. Duplicate suffixes such as " (1)" are tolerated.
INPUTS = {
    "aiid": ("AIID_Excel_Export-20261026", ".xlsx"),
    "freedom": ("freedom_on_the_net_scores", ".csv"),
    "thai": ("thai-disinfo-scam-dataset", ".xlsx"),
    "guide": ("00_Data_Guide_TH", ".pdf"),
}
AIID_SHEET, AIID_HEADER_OFFSET = "Incidents", 2          # Excel row 3
THAI_PANEL_SHEET, THAI_ACSC_SHEET = "weekly_panel", "acsc_weekly"  # header row 1

# Proposed Q1 defaults (team confirmation pending)
ASEAN_PEERS = ["KHM", "IDN", "MYS", "MMR", "PHL", "SGP", "VNM"]
FREEDOM_DEFAULT_YEAR = 2024

# Documented ACSC raw-start -> panel-week-start exception (8-day period)
ACSC_DATE_EXCEPTIONS = {pd.Timestamp("2026-05-30"): pd.Timestamp("2026-05-31")}

# Proposed comparable-view exclusions (panel week_start -> reason)
COMPARABLE_EXCLUSIONS = {
    pd.Timestamp("2026-05-31"): "Overlapping eight-day period (30 May-6 Jun 2026)",
    pd.Timestamp("2026-08-16"): "Suspect published figures (16-22 Aug 2026)",
}
Q3_DEFAULT_START = pd.Timestamp("2025-11-09")
Q3_DEFAULT_END = pd.Timestamp("2026-10-25")

UNCLASSIFIED = "Unclassified"

T = dict(
    canvas="#0C1018", sidebar="#101621", surface="#151C28", raised="#1D2736",
    border="#334155", control="#62728A", text="#F4F7FC", text2="#B0BCCE", muted="#8C9BB0",
    accent="#FF6B7A", accent_hover="#FF8A96", selected="#34212C", focus="#63D6E5",
    warn_fg="#F2C66D", warn_bg="#2B2316", err_fg="#FF9BA4", err_bg="#321E28",
    info_fg="#8CB9FF", info_bg="#172437", missing="#19212E", grid="#334155",
    btn_fg="#0C1018", peer="#8CB9FF",
    cases="#63D6E5", loss="#FF6B7A", ratio="#B9A0FF",
)
FONT = 'Tahoma, "Leelawadee UI", "Noto Sans Thai", "Thonburi", "Arial Unicode MS", system-ui, sans-serif'

DOMAIN_STYLE = {  # colour, plotly marker symbol
    "Malicious Actors & Misuse": ("#63D6E5", "circle"),
    "AI system safety, failures, and limitations": ("#B9A0FF", "square"),
    "Discrimination and Toxicity": ("#8CB9FF", "diamond"),
    "Misinformation": ("#F2CF73", "triangle-up"),
    "Privacy & Security": ("#F3A6D7", "triangle-down"),
    "Human-Computer Interaction": ("#81D6AF", "cross"),
    "Socioeconomic & Environmental Harms": ("#F5AC79", "x"),
    UNCLASSIFIED: ("#9BA6B8", "circle-open"),
}
