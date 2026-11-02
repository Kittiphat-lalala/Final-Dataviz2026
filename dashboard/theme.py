"""Streamlit CSS (flat dark surfaces) and the shared Plotly layout."""
from __future__ import annotations

import plotly.graph_objects as go

from .config import FONT, T

CSS = f"""
<style>
html, body, [class*="css"], .stApp {{ font-family: {FONT}; }}
.stApp {{ background: {T['canvas']}; color: {T['text']}; }}
[data-testid="stSidebar"] {{ background: {T['sidebar']}; border-right: 1px solid {T['border']}; }}
[data-testid="stSidebar"] > div {{ padding: 8px 4px; }}
.block-container {{ padding: 24px 32px 48px; max-width: 1500px; }}
h1 {{ font-size: 28px !important; font-weight: 700; line-height: 1.3; }}
h2 {{ font-size: 22px !important; font-weight: 700; line-height: 1.4; }}
h3 {{ font-size: 18px !important; font-weight: 600; line-height: 1.4; }}
p, li, label, .stMarkdown {{ line-height: 1.6; }}
.sub {{ color: {T['text2']}; font-size: 14px; }}
.cap {{ color: {T['muted']}; font-size: 13px; line-height: 1.6; }}
.eyebrow {{ color: {T['text2']}; font-size: 13px; margin: 8px 0 4px; }}
[data-testid="stMetric"] {{ background: {T['surface']}; border: 1px solid {T['border']};
  border-radius: 12px; padding: 16px; }}
[data-testid="stMetricValue"] {{ font-size: 30px; font-weight: 700; font-variant-numeric: tabular-nums; }}
[data-testid="stMetricLabel"] p {{ color: {T['text2']}; font-size: 14px; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 12px; border-color: {T['border']}; }}
.st-key-kpi_loss [data-testid="stMetric"] {{ border-top: 3px solid {T['loss']}; }}
.st-key-kpi_cases [data-testid="stMetric"] {{ border-top: 3px solid {T['cases']}; }}
.st-key-kpi_ratio [data-testid="stMetric"] {{ border-top: 3px solid {T['ratio']}; }}
.badge {{ display:inline-block; border-radius:6px; padding:2px 8px; font-size:13px; margin:0 8px 8px 0; }}
.b-warn {{ color:{T['warn_fg']}; border:1px solid {T['warn_fg']}; background:{T['warn_bg']}; }}
.b-info {{ color:{T['info_fg']}; border:1px solid {T['info_fg']}; background:{T['info_bg']}; }}
.b-chip {{ color:{T['text']}; border:1px solid {T['control']}; background:{T['selected']}; }}
.b-miss {{ color:{T['text2']}; border:1px solid {T['border']}; background:{T['missing']}; }}
.note {{ border-radius:8px; padding:12px 16px; margin:8px 0; font-size:14px; }}
.n-info {{ background:{T['info_bg']}; color:{T['text']}; border-left:2px solid {T['info_fg']}; }}
.n-warn {{ background:{T['warn_bg']}; color:{T['text']}; border-left:2px solid {T['warn_fg']}; }}
.n-err  {{ background:{T['err_bg']}; color:{T['err_fg']}; border-left:2px solid {T['err_fg']}; }}
.n-miss {{ background:{T['missing']}; color:{T['text2']}; border-left:2px solid {T['border']}; }}
/* question navigation styled as a tab strip */
div[data-testid="stRadio"][aria-label="Question tabs"] > div[role="radiogroup"],
.st-key-nav div[role="radiogroup"] {{ gap: 8px; border-bottom: 1px solid {T['border']}; flex-wrap: wrap; }}
.st-key-nav label {{ padding: 8px 16px; min-height: 44px; border-bottom: 3px solid transparent; cursor: pointer; }}
.st-key-nav label:has(input:checked) {{ border-bottom-color: {T['accent']}; font-weight: 700; }}
.st-key-nav label > div:first-child {{ display: none; }}
.stButton > button {{ background:{T['surface']}; color:{T['text']}; border:1px solid {T['control']};
  border-radius:8px; min-height:44px; width:100%; }}
.stButton > button:hover {{ border-color:{T['accent_hover']}; color:{T['text']}; }}
:focus-visible {{ outline: 2px solid {T['focus']} !important; outline-offset: 2px; }}
details {{ background:{T['surface']}; border:1px solid {T['border']} !important; border-radius:12px; }}
@media (max-width: 767px) {{
  .block-container {{ padding: 16px; }}
  h1 {{ font-size: 22px !important; }} h2 {{ font-size: 20px !important; }}
  [data-testid="stMetricValue"] {{ font-size: 26px; }}
}}
</style>
"""


def badge(text: str, kind: str = "chip") -> str:
    return f'<span class="badge b-{kind}">{text}</span>'


def note(text: str, kind: str = "info") -> str:
    return f'<div class="note n-{kind}">{text}</div>'


def base_layout(fig: go.Figure, title: str | None = None, height: int = 380) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=T["text"])) if title else None,
        paper_bgcolor=T["surface"], plot_bgcolor=T["surface"], height=height,
        font=dict(family=FONT, size=13, color=T["text2"]),
        margin=dict(l=16, r=16, t=48 if title else 16, b=16),
        legend=dict(orientation="h", y=-0.22, x=0, font=dict(size=13, color=T["text2"])),
        hoverlabel=dict(bgcolor=T["raised"], font=dict(color=T["text"], family=FONT)),
    )
    fig.update_xaxes(gridcolor=T["grid"], linecolor=T["control"], zerolinecolor=T["grid"],
                     tickfont=dict(size=13, color=T["text2"]))
    fig.update_yaxes(gridcolor=T["grid"], linecolor=T["control"], zerolinecolor=T["grid"],
                     tickfont=dict(size=13, color=T["text2"]))
    return fig
