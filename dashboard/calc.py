"""Pure calculations following dashboard_brd.md section 4. No Streamlit imports."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import COMPARABLE_EXCLUSIONS, UNCLASSIFIED


# ---------- Q1 ----------
def q1_scores(freedom: pd.DataFrame, year: int, peers: list[str]) -> dict:
    """Thailand + requested peers for one data_year. Missing country-years stay unavailable."""
    yr = freedom[freedom["data_year"] == year]
    rows = yr[yr["iso3"].isin(["THA", *peers])]
    got = rows.dropna(subset=["limits_on_content"])
    peer_rows = got[got["iso3"] != "THA"]
    tha = got.loc[got["iso3"] == "THA", "limits_on_content"]
    tha_v = float(tha.iloc[0]) if len(tha) else np.nan
    mean = float(peer_rows["limits_on_content"].mean()) if len(peer_rows) else np.nan
    return {
        "rows": got.sort_values("limits_on_content", ascending=False),
        "thailand": tha_v, "peer_mean": mean,
        "difference": tha_v - mean if not (np.isnan(tha_v) or np.isnan(mean)) else np.nan,
        "n_available": len(peer_rows), "n_requested": len(peers),
        "unavailable": sorted(set(peers) - set(peer_rows["iso3"])),
        "edition": int(rows["report_edition"].iloc[0]) if len(rows) else None,
    }


# ---------- Q1 / Q2 ----------
def incidents_in_years(df: pd.DataFrame, y0: int, y1: int) -> pd.DataFrame:
    """A(Y): distinct incident records in the occurrence-year range, before domain filtering."""
    return df[(df["year"] >= y0) & (df["year"] <= y1)].drop_duplicates("Incident ID")


def coverage(a_y: pd.DataFrame) -> dict:
    n = len(a_y)
    classified = int((a_y["domain"] != UNCLASSIFIED).sum())
    return {"all": n, "classified": classified, "unclassified": n - classified,
            "pct": (classified / n * 100) if n else np.nan}


def coverage_by_year(a_y: pd.DataFrame) -> pd.DataFrame:
    g = a_y.groupby("year")["domain"].agg(all="size", classified=lambda s: int((s != UNCLASSIFIED).sum()))
    g["unclassified"] = g["all"] - g["classified"]
    g["coverage_pct"] = g["classified"] / g["all"] * 100
    return g.reset_index()


def domain_counts(a_yd: pd.DataFrame) -> pd.DataFrame:
    c = a_yd.groupby("domain")["Incident ID"].nunique().rename("incidents").reset_index()
    c["pct_of_filtered"] = c["incidents"] / c["incidents"].sum() * 100 if len(c) else np.nan
    return c.sort_values("incidents", ascending=False)


def yearly_domain_counts(a_yd: pd.DataFrame) -> pd.DataFrame:
    """Distinct IDs per (year, domain); zero only for domains within years that have records."""
    g = a_yd.groupby(["year", "domain"])["Incident ID"].nunique().unstack(fill_value=0)
    return g.stack().rename("incidents").reset_index()


def yearly_totals(a_yd: pd.DataFrame, deepfake_ids: set) -> pd.DataFrame:
    t = a_yd.groupby("year")["Incident ID"].nunique().rename("total")
    d = a_yd[a_yd["Incident ID"].isin(deepfake_ids)].groupby("year")["Incident ID"].nunique().rename("candidate_deepfake")
    return pd.concat([t, d], axis=1).fillna(0).astype(int).rename_axis("year").reset_index()


# ---------- Q3 ----------
def loss_per_case(loss, cases):
    loss = pd.to_numeric(pd.Series(loss), errors="coerce")
    cases = pd.to_numeric(pd.Series(cases), errors="coerce")
    ok = loss.notna() & cases.notna() & (cases > 0)
    return (loss / cases).where(ok)


def prepare_weeks(thai: pd.DataFrame, start, end, view: str) -> pd.DataFrame:
    """Selected panel weeks with eligibility. Selected weeks always remain in the timeline."""
    w = thai[(thai["week_start"] >= start) & (thai["week_start"] <= end)].copy()
    w["excluded"] = (view == "comparable") & w["week_start"].isin(COMPARABLE_EXCLUSIONS)
    w["eligible"] = w["acsc_reported"] & ~w["excluded"] & w["acsc_cases"].notna() & w["acsc_loss_baht"].notna()
    w["loss_per_case_calc"] = loss_per_case(w["acsc_loss_baht"], w["acsc_cases"])
    w["diff_vs_source"] = w["loss_per_case_calc"] - w["acsc_loss_per_case_baht"]
    shown = w["acsc_reported"] & ~w["excluded"]
    for c, out in [("acsc_cases", "cases_plot"), ("acsc_loss_baht", "loss_plot"), ("loss_per_case_calc", "ratio_plot")]:
        w[out] = w[c].where(shown)
    w["loss_million"] = w["loss_plot"] / 1_000_000
    w["rounded"] = w["acsc_loss_precision"].eq("rounded")
    return w


def coverage_counts(w: pd.DataFrame) -> dict:
    return {"selected": len(w), "reported": int(w["acsc_reported"].sum()),
            "included": int(w["eligible"].sum()),
            "paired": int((w["eligible"] & w["loss_per_case_calc"].notna()).sum())}


def range_summary(w: pd.DataFrame) -> dict:
    p = w[w["eligible"] & w["loss_per_case_calc"].notna()]  # E-paired
    cases, loss = p["acsc_cases"].sum(), p["acsc_loss_baht"].sum()
    return {"periods": len(p), "cases": cases, "loss": loss,
            "ratio": loss / cases if len(p) and cases > 0 else np.nan}


def latest_kpi(w: pd.DataFrame) -> dict:
    """Latest eligible week in the selection, adjacent-week deltas, newer-week disclosure."""
    el = w[w["eligible"] & w["loss_per_case_calc"].notna()]
    if el.empty:
        return {"available": False}
    cur = el.iloc[-1]
    newer = w[w["week_start"] > cur["week_start"]]
    prev = w[(w["week_start"] == cur["week_start"] - pd.Timedelta(days=7)) & w["eligible"]
             & w["loss_per_case_calc"].notna()]
    regular = int(cur.get("days", 7) or 7) == 7
    d = {"available": True, "week": cur, "newer": newer.iloc[-1] if len(newer) else None,
         "delta": None}
    if len(prev) and regular and int(prev.iloc[0].get("days", 7) or 7) == 7:
        p = prev.iloc[0]
        d["delta"] = {
            "prev_start": p["week_start"],
            "cases_pct": (cur["acsc_cases"] / p["acsc_cases"] - 1) * 100 if p["acsc_cases"] > 0 else np.nan,
            "loss_pct": (cur["acsc_loss_baht"] / p["acsc_loss_baht"] - 1) * 100 if p["acsc_loss_baht"] > 0 else np.nan,
            "ratio_abs": cur["loss_per_case_calc"] - p["loss_per_case_calc"],
        }
    return d


def peak_loss(w: pd.DataFrame):
    """Highest displayed total loss among valid included points; ties returned together."""
    el = w[w["eligible"]]
    if el.empty:
        return None
    return el[el["acsc_loss_baht"] == el["acsc_loss_baht"].max()]
