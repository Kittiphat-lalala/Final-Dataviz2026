"""Input resolution, loading and validation. Never fabricates replacement data."""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

import pandas as pd

from . import config as C

ROOT = Path(__file__).resolve().parent.parent


class DataError(Exception):
    """A source is missing, unreadable, ambiguous or fails validation."""


def search_dirs() -> list[Path]:
    dirs = []
    if os.environ.get("DATAVIZ_DATA_DIR"):
        dirs.append(Path(os.environ["DATAVIZ_DATA_DIR"]))
    return dirs + [ROOT, ROOT / "data"]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def find_input(key: str, dirs: list[Path] | None = None) -> Path:
    stem, ext = C.INPUTS[key]
    rx = re.compile(rf"{re.escape(stem)}(?: \(\d+\))?{re.escape(ext)}", re.IGNORECASE)
    found = [p for d in (dirs or search_dirs()) if d.is_dir() for p in sorted(d.iterdir())
             if p.is_file() and rx.fullmatch(p.name)]
    if not found:
        raise DataError(f"Required file '{stem}{ext}' not found in: "
                        + ", ".join(str(d) for d in (dirs or search_dirs())))
    if len({_sha(p) for p in found}) > 1:
        raise DataError("Ambiguous input: different versions of "
                        f"'{stem}{ext}' found: " + ", ".join(str(p) for p in found))
    return found[0]


def _require(df: pd.DataFrame, cols: list[str], name: str):
    miss = [c for c in cols if c not in df.columns]
    if miss:
        raise DataError(f"{name}: missing required columns {miss}")


def _unique(df: pd.DataFrame, cols: list[str], name: str):
    dup = df[df.duplicated(cols, keep=False)]
    if len(dup):
        raise DataError(f"{name}: {len(dup)} rows conflict on key {cols}")


def load_freedom(path: Path | None = None) -> pd.DataFrame:
    path = path or find_input("freedom")
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        raise DataError(f"Freedom CSV unreadable ({path.name}): {e}") from e
    _require(df, ["iso3", "country", "data_year", "report_edition", "limits_on_content"], "Freedom CSV")
    _unique(df, ["iso3", "data_year"], "Freedom CSV")
    df["limits_on_content"] = pd.to_numeric(df["limits_on_content"], errors="coerce")
    return df


def load_aiid(path: Path | None = None) -> pd.DataFrame:
    path = path or find_input("aiid")
    try:
        df = pd.read_excel(path, sheet_name=C.AIID_SHEET, header=C.AIID_HEADER_OFFSET)
    except Exception as e:  # noqa: BLE001
        raise DataError(f"AIID workbook unreadable ({path.name}, sheet {C.AIID_SHEET}, "
                        f"header offset {C.AIID_HEADER_OFFSET}): {e}") from e
    _require(df, ["Incident ID", "date", "year", "Risk Domain", "Implicated Systems", "title",
                  "description", "Estimated Date"], "AIID Incidents")
    _unique(df, ["Incident ID"], "AIID Incidents")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    bad = int((df["date"].dt.year.astype("Int64") != df["year"]).sum())
    if bad:
        raise DataError(f"AIID Incidents: {bad} rows where year != year(date)")
    raw = df["Risk Domain"]
    blank = raw.isna() | raw.astype(str).str.strip().eq("")
    df["domain"] = raw.where(~blank, C.UNCLASSIFIED).astype(str).str.strip()  # raw value retained
    return df


def load_thai(path: Path | None = None) -> pd.DataFrame:
    """weekly_panel plus acsc_weekly metadata attached one-to-one via a documented exception map."""
    path = path or find_input("thai")
    try:
        panel = pd.read_excel(path, sheet_name=C.THAI_PANEL_SHEET)
        acsc = pd.read_excel(path, sheet_name=C.THAI_ACSC_SHEET)
    except Exception as e:  # noqa: BLE001
        raise DataError(f"Thai workbook unreadable ({path.name}): {e}") from e
    _require(panel, ["week_start", "week_end", "acsc_reported", "acsc_cases", "acsc_loss_baht",
                     "acsc_loss_precision", "acsc_loss_per_case_baht", "acsc_top_type_th",
                     "acsc_highest_loss_type_th", "acsc_flag", "acsc_source_url"], "weekly_panel")
    _require(acsc, ["week_start", "week_end", "days", "publisher", "article_date", "notes"], "acsc_weekly")
    _unique(panel, ["week_start"], "weekly_panel")
    panel["acsc_reported"] = panel["acsc_reported"].astype(bool)

    acsc = acsc.copy()
    pws = set(panel["week_start"])
    acsc["panel_week_start"] = [s if s in pws else C.ACSC_DATE_EXCEPTIONS.get(s) for s in acsc["week_start"]]
    if acsc["panel_week_start"].isna().any():
        raise DataError("acsc_weekly: rows with no panel week and no documented exception: "
                        f"{acsc.loc[acsc['panel_week_start'].isna(), 'week_start'].tolist()}")
    _unique(acsc, ["panel_week_start"], "acsc_weekly (after exception mapping)")
    meta = acsc.rename(columns={"week_start": "orig_start", "week_end": "orig_end"})[
        ["panel_week_start", "orig_start", "orig_end", "days", "publisher", "article_date", "notes"]]
    out = panel.merge(meta, left_on="week_start", right_on="panel_week_start", how="left",
                      validate="one_to_one").drop(columns="panel_week_start")
    if len(out) != len(panel) or out["orig_start"].notna().sum() != len(acsc):
        raise DataError("acsc_weekly attach lost or multiplied rows")
    out["excluded_reason"] = out["week_start"].map(C.COMPARABLE_EXCLUSIONS)
    return out.sort_values("week_start").reset_index(drop=True)
