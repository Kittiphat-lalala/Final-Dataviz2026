"""Plotly figures. Gaps stay gaps: no interpolation, no zero filling."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .config import DOMAIN_STYLE, T, UNCLASSIFIED
from .theme import base_layout


def q1_bars(rows: pd.DataFrame, year: int) -> go.Figure:
    d = rows.sort_values("limits_on_content")
    cols = [T["accent"] if i == "THA" else T["peer"] for i in d["iso3"]]
    labels = [f"<b>Thailand (THA)</b>" if i == "THA" else f"{c} ({i})" for i, c in zip(d["iso3"], d["country"])]
    fig = go.Figure(go.Bar(
        x=d["limits_on_content"], y=labels, orientation="h", marker_color=cols,
        text=[f"{v:g}" for v in d["limits_on_content"]], textposition="outside",
        customdata=np.c_[d["iso3"], d["data_year"], d["report_edition"]],
        hovertemplate="%{y}<br>limits_on_content: %{x}/35<br>data_year %{customdata[1]} · edition %{customdata[2]}<extra></extra>"))
    base_layout(fig, height=max(300, 46 * len(d) + 80))
    fig.update_xaxes(range=[0, 36], title="Points /35 · higher = greater content freedom")
    fig.update_layout(showlegend=False)
    return fig


def domain_bars(counts: pd.DataFrame) -> go.Figure:
    d = counts.sort_values("incidents")
    fig = go.Figure(go.Bar(
        x=d["incidents"], y=d["domain"], orientation="h",
        marker_color=[DOMAIN_STYLE.get(x, ("#9BA6B8",))[0] for x in d["domain"]],
        text=[f"{n:,} ({p:.1f}%)" for n, p in zip(d["incidents"], d["pct_of_filtered"])], textposition="outside",
        hovertemplate="%{y}<br>%{x} distinct incidents<extra></extra>"))
    base_layout(fig, height=max(320, 44 * len(d) + 80))
    fig.update_xaxes(title="Distinct recorded incidents", range=[0, float(d["incidents"].max()) * 1.35])
    fig.update_traces(cliponaxis=False)
    fig.update_layout(showlegend=False)
    return fig


def _year_ticks(fig: go.Figure, years: list[int]):
    if not years:
        return
    tv = sorted(set(years))
    if len(tv) > 18:
        tv = [y for y in tv if (y % 5 == 0 and tv[-1] - y >= 3) or y == tv[-1]]
    fig.update_xaxes(tickangle=0, tickmode="array", tickvals=tv,
                     ticktext=[f"{y}*" if y == 2026 else str(y) for y in tv])


def q2_lines(ydc: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for dom in [d for d in DOMAIN_STYLE if d in set(ydc["domain"])]:
        s = ydc[ydc["domain"] == dom].sort_values("year")
        color, sym = DOMAIN_STYLE[dom]
        fig.add_scatter(x=s["year"], y=s["incidents"], name=dom, mode="lines+markers",
                        line=dict(color=color, width=2.5, dash="dot" if dom == UNCLASSIFIED else "solid"),
                        marker=dict(symbol=sym, size=7, color=color, line=dict(width=1.5, color=color)),
                        hovertemplate="%{x}: %{y} incidents<extra>" + dom + "</extra>")
    base_layout(fig, height=440)
    fig.update_yaxes(title="Distinct recorded incidents", rangemode="tozero")
    fig.update_xaxes(title="Occurrence year (2026* incomplete)")
    _year_ticks(fig, list(ydc["year"]))
    fig.update_layout(legend=dict(y=-0.32))
    return fig


def q2_subset(t: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(x=t["year"], y=t["total"], name="All incidents in selection", mode="lines+markers",
                    line=dict(color=T["text"], width=2.5), marker=dict(symbol="circle", size=7))
    fig.add_scatter(x=t["year"], y=t["candidate_deepfake"], name="Candidate deepfake · provisional rule",
                    mode="lines+markers", line=dict(color=T["accent"], width=3, dash="dash"),
                    marker=dict(symbol="diamond", size=8))
    base_layout(fig, height=360)
    fig.update_yaxes(title="Distinct recorded incidents", rangemode="tozero")
    fig.update_xaxes(title="Occurrence year (2026* incomplete)")
    _year_ticks(fig, list(t["year"]))
    fig.update_layout(legend=dict(y=-0.4))
    return fig


def _x_ticks(fig, w):
    ts = w["week_start"]
    keep = [d for i, d in enumerate(ts) if i % 4 == 0 or i == len(ts) - 1]
    fig.update_xaxes(tickmode="array", tickvals=keep,
                     ticktext=[d.strftime("%d %b\n%Y") if (d.month == 1 and d.day <= 7) or d == keep[0]
                               else d.strftime("%d %b") for d in keep])


def _hover(w):
    return [f"{a:%d %b %Y}–{b:%d %b %Y}" for a, b in zip(w["week_start"], w["week_end"])]


def _annotate(fig, w, rows):
    for _, r in w[w["excluded"]].iterrows():
        for rr in rows:
            kw = {"row": rr, "col": 1} if rr else {}
            fig.add_vrect(x0=r["week_start"] - pd.Timedelta(days=3.5), x1=r["week_start"] + pd.Timedelta(days=3.5),
                          fillcolor=T["missing"], opacity=1, line=dict(color=T["warn_fg"], width=1, dash="dot"),
                          layer="below", annotation_text="Excluded", annotation_font=dict(color=T["warn_fg"], size=12),
                          annotation_position="bottom", **kw)
    flagged = w[w["acsc_flag"].notna() & w["acsc_reported"] & ~w["excluded"]]
    return flagged


def q3_figures(w: pd.DataFrame, layout: str) -> list[go.Figure]:
    """Layout A: dual-axis cases/loss + separate ratio chart. Layout B: three aligned charts."""
    hov = _hover(w)
    cd = w["week_start"].dt.strftime("%Y-%m-%d")
    mark_round = ["≈ rounded loss" if r else "" for r in w["rounded"]]
    ratio_lbl = [f"{v:,.0f}" if pd.notna(v) else "—" for v in w["ratio_plot"]]

    def cases_tr(kind):
        common = dict(x=w["week_start"], y=w["cases_plot"], name="Total reported cases", customdata=cd,
                      hovertext=hov, hovertemplate="%{hovertext}<br>%{y:,.0f} reported cases (all types)<extra></extra>")
        if kind == "bar":
            return go.Bar(marker_color=T["cases"], **common)
        return go.Scatter(mode="lines+markers", line=dict(color=T["cases"], width=2.5), marker=dict(size=6),
                          connectgaps=False, **common)

    loss_tr = go.Scatter(x=w["week_start"], y=w["loss_million"], name="Total reported losses (THB million)",
                         mode="lines+markers", line=dict(color=T["loss"], width=2.5), connectgaps=False,
                         marker=dict(size=6, symbol=["circle-open" if r else "circle" for r in w["rounded"]],
                                     color=T["loss"], line=dict(width=2, color=T["loss"])),
                         customdata=np.c_[cd, mark_round], hovertext=hov,
                         hovertemplate="%{hovertext}<br>THB %{y:,.1f} million (all types) %{customdata[1]}<extra></extra>")
    ratio_tr = go.Scatter(x=w["week_start"], y=w["ratio_plot"], name="Calculated loss per case (THB/case)",
                          mode="lines+markers", line=dict(color=T["ratio"], width=2.5), connectgaps=False,
                          marker=dict(size=6, symbol=["circle-open" if r else "circle" for r in w["rounded"]]),
                          customdata=cd, hovertext=hov,
                          hovertemplate="%{hovertext}<br>%{y:,.0f} THB/case (calculated)<extra></extra>")
    figs = []
    if layout == "A":
        a = make_subplots(specs=[[{"secondary_y": True}]])
        a.add_trace(cases_tr("bar"), secondary_y=False)
        a.add_trace(loss_tr, secondary_y=True)
        base_layout(a, "Weekly total reported cases (left) and total reported losses (right), all types", 420)
        a.update_yaxes(title_text="Total reported cases", rangemode="tozero", secondary_y=False,
                       title_font=dict(color=T["cases"]))
        a.update_yaxes(title_text="Total reported losses (THB million)", rangemode="tozero", secondary_y=True,
                       showgrid=False, title_font=dict(color=T["loss"]))
        _annotate(a, w, [1]); _x_ticks(a, w)
        r = go.Figure(ratio_tr)
        base_layout(r, "Calculated loss per case (loss ÷ cases)", 340)
        r.update_yaxes(title="THB/case", rangemode="tozero"); _annotate(r, w, [None]); _x_ticks(r, w)
        figs = [a, r]
    else:
        for tr, title, ytitle in [(cases_tr("line"), "Total reported cases", "Reported cases"),
                                  (loss_tr, "Total reported losses", "THB million"),
                                  (ratio_tr, "Calculated loss per case", "THB/case")]:
            f = go.Figure(tr)
            base_layout(f, title, 300)
            f.update_yaxes(title=ytitle, rangemode="tozero"); f.update_layout(showlegend=False)
            _annotate(f, w, [None]); _x_ticks(f, w)
            figs.append(f)
    return figs
