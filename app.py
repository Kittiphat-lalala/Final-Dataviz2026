"""Digital Risk: Q1-Q3 dashboard. Run: streamlit run app.py  (see README.md)."""
from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd
import streamlit as st

from dashboard import calc, charts, config as C, data, deepfake
from dashboard.theme import CSS, badge, note

st.set_page_config(page_title="Digital Risk: Q1–Q3", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)
S = st.session_state
TABS = ["Q1 · Thailand vs ASEAN", "Q2 · AI incidents", "Q3 · Reported scams"]
TAB_ID = dict(zip(TABS, ["q1", "q2", "q3"]))


# ---------------------------------------------------------------- loading
@st.cache_data(show_spinner="Loading source…")
def _load(kind: str):
    fn = {"freedom": data.load_freedom, "aiid": data.load_aiid, "thai": data.load_thai}[kind]
    try:
        return fn(), None
    except data.DataError as e:
        return None, str(e)
    except Exception as e:  # noqa: BLE001
        return None, f"Unexpected error loading {kind}: {e}"


@st.cache_data
def _evidence():
    aiid, _ = _load("aiid")
    return deepfake.find_matches(aiid)


freedom, err_f = _load("freedom")
aiid, err_a = _load("aiid")
thai, err_t = _load("thai")

# ---------------------------------------------------------------- state / defaults
yrs = (int(aiid["year"].min()), int(aiid["year"].max())) if aiid is not None else (1983, 2026)
domains_all = ([d for d in C.DOMAIN_STYLE if d in set(aiid["domain"])]
               + sorted(set(aiid["domain"]) - set(C.DOMAIN_STYLE))) if aiid is not None else []
if thai is not None:
    _rep = thai[thai["acsc_reported"]]["week_start"]
    BRIEF = (_rep.min().to_pydatetime(), _rep.max().to_pydatetime())
    Q3_WEEKS = [d for d in thai["week_start"] if d >= C.Q3_DEFAULT_START] or list(thai["week_start"])
    Q3_BOUNDS = (Q3_WEEKS[0].to_pydatetime(), Q3_WEEKS[-1].to_pydatetime())
    Q3_DEF = (Q3_WEEKS[0].to_pydatetime(), min(Q3_WEEKS[-1], C.Q3_DEFAULT_END).to_pydatetime())
else:
    BRIEF = (C.Q3_DEFAULT_START.to_pydatetime(), C.Q3_DEFAULT_END.to_pydatetime())
    Q3_BOUNDS, Q3_DEF = BRIEF, BRIEF
free_years = sorted(freedom.loc[freedom.iso3 == "THA", "data_year"].unique(), reverse=True) if freedom is not None else []
peer_opts = [p for p in C.ASEAN_PEERS if freedom is not None and p in set(freedom["iso3"])]
DEF = {
    "q1_year": C.FREEDOM_DEFAULT_YEAR, "q1_peers": peer_opts, "q1_ai_years": yrs, "q1_ai_domains": domains_all,
    "q1_thai_range": BRIEF,
    "q2_years": yrs, "q2_domains": domains_all,
    "q3_range": Q3_DEF, "q3_view": "comparable", "q3_layout": "A",
}
TAB_KEYS = {"q1": ["q1_year", "q1_peers", "q1_ai_years", "q1_ai_domains", "q1_thai_range"],
            "q2": ["q2_years", "q2_domains"], "q3": ["q3_range", "q3_view", "q3_layout"]}
for k, v in DEF.items():
    S.setdefault(k, v)
for t in TAB_KEYS:
    S.setdefault(f"nonce_{t}", 0)
S.setdefault("active_tab", TABS[0])
for k in [*DEF, "active_tab"]:  # keep widget state alive while its tab's controls are not rendered
    S[k] = S[k]


def reset(tab: str):
    for k in TAB_KEYS[tab]:
        S[k] = DEF[k]
    S[f"nonce_{tab}"] += 1


def fmt_d(d): return pd.Timestamp(d).strftime("%d %b %Y")
def fmt_w(a, b): return f"{fmt_d(a)} – {fmt_d(b)}"
def num(v, f="{:,.0f}"): return "Unavailable" if v is None or (isinstance(v, float) and np.isnan(v)) else f.format(v)


def show(fig, tab, name, select=False):
    key = f"{tab}_{name}_{S[f'nonce_{tab}']}"
    if select:
        return st.plotly_chart(fig, key=key, width="stretch", on_select="rerun", selection_mode=("points",))
    st.plotly_chart(fig, key=key, width="stretch")


def source_error(name, msg):
    st.markdown(note(f"<b>{name} could not be loaded.</b> {msg}<br>Other panels remain available. "
                     "Check the file names/paths in README.md.", "err"), unsafe_allow_html=True)


def chips(*items):
    st.markdown("".join(badge(i) for i in items), unsafe_allow_html=True)


# ---------------------------------------------------------------- header + weekly KPI strip
st.title("Digital Risk: Q1–Q3")
st.markdown('<div class="sub">Three separate lenses: expert content-freedom assessments, recorded AI incidents and '
            'reported scam totals. Periods, units and coverage differ; nothing here implies causation.</div>',
            unsafe_allow_html=True)
st.markdown('<div class="cap">Sources: Freedom House via QoG (Jan 2026), instructor-transformed · Responsible AI '
            'Collaborative (AIID export 2026-10-26) · compiled ACSC briefing figures (Thai workbook, compiled '
            '2026-11-01). UI language: English (team decision pending).</div>', unsafe_allow_html=True)

st.markdown('<div class="eyebrow">Thai reported scams · Q3 selection</div>', unsafe_allow_html=True)
if thai is None:
    source_error("Thai workbook", err_t)
else:
    wk = calc.prepare_weeks(thai, *map(pd.Timestamp, S["q3_range"]), S["q3_view"])
    k = calc.latest_kpi(wk)
    view_lbl = "Comparable — proposed policy" if S["q3_view"] == "comparable" else "As published"
    if k["available"]:
        cur = k["week"]
        st.markdown(f'<div class="cap">Latest eligible week: <b>{fmt_w(cur.week_start, cur.week_end)}</b> · '
                    f'Q3 range {fmt_d(S["q3_range"][0])} – {fmt_d(S["q3_range"][1])} · {view_lbl}</div>',
                    unsafe_allow_html=True)
        if k["newer"] is not None:
            nw = k["newer"]
            why = "excluded by policy" if nw["excluded"] else "unavailable"
            st.markdown(note(f"Newer selected period {fmt_w(nw.week_start, nw.week_end)} is {why}.", "warn"),
                        unsafe_allow_html=True)
        dl = k["delta"]
        dtxt = (lambda s: f"{s} vs {fmt_d(dl['prev_start'])}") if dl else (lambda s: None)
        c1, c2, c3 = st.columns(3)
        approx = "≈ " if cur["rounded"] else ""
        with c1, st.container(key="kpi_loss"):
            st.metric("Total reported losses", f"{approx}THB {cur.acsc_loss_baht / 1e6:,.1f} M",
                      dtxt(f"{dl['loss_pct']:+.1f}%") if dl and not np.isnan(dl["loss_pct"]) else None, delta_color="off")
            st.caption("All reported types" + (" · rounded source loss" if cur["rounded"] else ""))
        with c2, st.container(key="kpi_cases"):
            st.metric("Total reported cases", f"{cur.acsc_cases:,.0f}",
                      dtxt(f"{dl['cases_pct']:+.1f}%") if dl and not np.isnan(dl["cases_pct"]) else None, delta_color="off")
            st.caption("All reported types")
        with c3, st.container(key="kpi_ratio"):
            st.metric("Calculated loss per case", f"{approx}THB {cur.loss_per_case_calc:,.0f}",
                      dtxt(f"{dl['ratio_abs']:+,.0f} THB/case") if dl else None, delta_color="off")
            st.caption("Calculated from raw loss ÷ cases")
        if not dl:
            st.markdown('<div class="cap">Δ unavailable — no comparable prior period.</div>', unsafe_allow_html=True)
    else:
        st.markdown(note("No eligible reporting week in the Q3 selection — all three values unavailable.", "miss"),
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        for c, lab in zip((c1, c2, c3), ["Total reported losses", "Total reported cases", "Calculated loss per case"]):
            c.metric(lab, "— Unavailable")
if S["active_tab"] != TABS[2] and st.button("Edit Q3 selection", key="goto_q3"):
    S["active_tab"] = TABS[2]; st.rerun()

with st.container(key="nav"):
    tab = st.radio("Question tabs", TABS, horizontal=True, key="active_tab", label_visibility="collapsed")
tid = TAB_ID[tab]

# ---------------------------------------------------------------- sidebar (active tab only)
with st.sidebar:
    st.markdown(f"### {tab}")
    if tid == "q1":
        st.markdown("**Freedom comparison**"); st.caption("Only country comparison")
        if freedom is not None:
            st.selectbox("Data year (data_year)", free_years, key="q1_year")
            st.multiselect("ASEAN peers available in dataset (Thailand fixed)", peer_opts, key="q1_peers",
                           format_func=lambda i: f"{freedom.loc[freedom.iso3 == i, 'country'].iloc[0]} ({i})")
        st.divider(); st.markdown("**Global AI context**"); st.caption("Only AI context")
        if aiid is not None:
            st.slider("Occurrence years", yrs[0], yrs[1], key="q1_ai_years")
            st.multiselect("Risk Domain (incl. Unclassified)", domains_all, key="q1_ai_domains")
        st.divider(); st.markdown("**Thai context**")
        st.caption("Type names only; source records may include flagged periods")
        if thai is not None:
            st.slider("Reporting-period range (week starts)", BRIEF[0], BRIEF[1], step=timedelta(days=7),
                      key="q1_thai_range", format="DD MMM YYYY")
    elif tid == "q2":
        st.markdown("**AI occurrence**")
        st.caption("Coverage uses the selected years before the domain filter is applied.")
        if aiid is not None:
            st.slider("Occurrence years", yrs[0], yrs[1], key="q2_years")
            st.multiselect("Risk Domain (incl. Unclassified)", domains_all, key="q2_domains")
    else:
        st.markdown("**Thai reporting**")
        if thai is not None:
            st.slider("Panel-week range (week starts)", Q3_BOUNDS[0], Q3_BOUNDS[1], step=timedelta(days=7),
                      key="q3_range", format="DD MMM YYYY")
            st.radio("Quality view", ["comparable", "as_published"], key="q3_view",
                     format_func=lambda v: "Comparable — proposed policy" if v == "comparable" else "As published")
            st.radio("Chart layout (team decision pending)", ["A", "B"], key="q3_layout",
                     format_func=lambda v: "A · dual-axis + ratio (recommended)" if v == "A" else "B · three aligned charts")
            st.caption("No type filters on totals: all-type totals only.")
    st.button(f"Reset {tid.upper()}", key=f"reset_{tid}", on_click=reset, args=(tid,))


def scoped_reset_hint():
    st.caption(f"Reset {tid.upper()} restores this tab's defaults and clears its chart selections only.")


# ================================================================ Q1
if tid == "q1":
    st.header("Q1 · How does Thailand compare with ASEAN countries in the dataset on content freedom?")
    chips(f"Data year {S['q1_year']}", f"{len(S['q1_peers'])} peers selected",
          f"AI years {S['q1_ai_years'][0]}–{S['q1_ai_years'][1]}", f"AI domains {len(S['q1_ai_domains'])}/{len(domains_all)}")
    with st.container(border=True):
        st.subheader("Thailand vs selected peers · limits_on_content")
        if freedom is None:
            source_error("Freedom on the Net CSV", err_f)
        else:
            r = calc.q1_scores(freedom, S["q1_year"], S["q1_peers"])
            st.markdown(f'<div class="sub">data_year {S["q1_year"]} · report edition {r["edition"] or "—"} · '
                        'Points /35 · higher = greater content freedom</div>', unsafe_allow_html=True)
            a, b, c, d = st.columns(4)
            a.metric("Thailand (points /35)", num(r["thailand"], "{:g}"))
            b.metric("Selected-peer mean (points /35)", num(r["peer_mean"], "{:.1f}"))
            c.metric("Thailand − peer mean (points)", num(r["difference"], "{:+.1f}"))
            d.metric("Peer availability", f"{r['n_available']}/{r['n_requested']} countries")
            if len(r["rows"]) == 0:
                st.markdown(note("No Freedom rows for this selection.", "miss"), unsafe_allow_html=True)
            else:
                ev = show(charts.q1_bars(r["rows"], S["q1_year"]), "q1", "bars", select=True)
                if ev and ev.selection.points:
                    sel = {p.get("customdata", [None])[0] for p in ev.selection.points}
                    st.dataframe(r["rows"][r["rows"].iso3.isin(sel)][
                        ["country", "iso3", "data_year", "report_edition", "limits_on_content", "total_score"]],
                        hide_index=True, width="stretch")
            if r["unavailable"]:
                st.markdown(note("Requested but unavailable in this year (no score, not zero): "
                                 + ", ".join(r["unavailable"]), "warn"), unsafe_allow_html=True)
            if np.isnan(r["thailand"]):
                st.markdown(note("Thailand has no score in this year.", "miss"), unsafe_allow_html=True)
            if r["n_available"]:
                st.markdown(note(f"In {S['q1_year']}, Thailand's component is {r['thailand']:g}/35; "
                                 f"{r['n_available']}/{r['n_requested']} selected peers have data. Assessment scores "
                                 "are expert judgements, not incident counts.", "info"), unsafe_allow_html=True)
            st.caption("Source: Freedom House via QoG Standard Dataset (Jan 2026), instructor transformations. "
                       "Covered countries are not all ASEAN members.")
    c_ai, c_th = st.columns(2)
    with c_ai, st.container(border=True):
        st.subheader("Global recorded AI incidents by Risk Domain")
        if aiid is None:
            source_error("AIID workbook", err_a)
        else:
            y0, y1 = S["q1_ai_years"]
            a_y = calc.incidents_in_years(aiid, y0, y1)
            a_yd = a_y[a_y["domain"].isin(S["q1_ai_domains"])]
            cov = calc.coverage(a_y)
            st.markdown(f'<div class="sub">Occurrence years {y0}–{y1} · distinct incidents · global, not Thailand-specific</div>',
                        unsafe_allow_html=True)
            if len(a_yd) == 0:
                st.markdown(note("No incidents match these filters (not a load error).", "miss"), unsafe_allow_html=True)
            else:
                show(charts.domain_bars(calc.domain_counts(a_yd)), "q1", "ai")
            st.markdown(f'<div class="cap">Classified {cov["classified"]:,} / all in selected years {cov["all"]:,} · '
                        f'{num(cov["pct"], "{:.1f}")}%. Displayed after domain selection: {len(a_yd):,}. '
                        'Percentages use the displayed total as denominator.</div>', unsafe_allow_html=True)
            st.caption("Source: Responsible AI Collaborative (AIID), export 2026-10-26.")
    with c_th, st.container(border=True):
        st.subheader("Thailand · reported highest-loss type names")
        if thai is None:
            source_error("Thai workbook", err_t)
        else:
            s0, s1 = map(pd.Timestamp, S["q1_thai_range"])
            t = thai[thai["acsc_reported"] & (thai.week_start >= s0) & (thai.week_start <= s1)].copy()
            st.markdown(f'<div class="sub">Reporting periods {fmt_d(s0)} – {fmt_d(s1)} · {len(t)} reported periods</div>',
                        unsafe_allow_html=True)
            st.caption("Type reported as having the highest loss in this reporting period. Categorical briefing "
                       "information, not a measured total loss by that type.")
            t["Original period (if not 7 days)"] = [f"{fmt_w(a, b)} ({int(d)} days)" if d != 7 else ""
                                                    for a, b, d in zip(t.orig_start, t.orig_end, t.days)]
            t["Highest-loss type"] = t["acsc_highest_loss_type_th"].fillna("Unavailable")
            t["Week"] = t.week_start.dt.strftime("%Y-%m-%d") + " – " + t.week_end.dt.strftime("%Y-%m-%d")
            st.dataframe(t[["Week", "Highest-loss type", "acsc_flag", "acsc_loss_precision",
                            "acsc_source_url", "Original period (if not 7 days)"]].rename(columns={
                "acsc_flag": "Source flag", "acsc_loss_precision": "Loss precision", "acsc_source_url": "Source"}),
                hide_index=True, width="stretch", column_config={"Source": st.column_config.LinkColumn("Source", display_text="link")})
            st.caption("Source: compiled ACSC briefings (publisher, article date and URL per row). Flagged periods "
                       "are shown descriptively here even where Q3's comparable view excludes them.")
    st.markdown(note("The three panels use independent periods and units. They are separate context, not a "
                     "same-period or causal comparison.", "info"), unsafe_allow_html=True)
    with st.expander("Methods & source"):
        st.markdown("""- **Comparison:** `limits_on_content` for Thailand and selected peers in one `data_year` (points /35, higher = freer). Peer mean is unweighted over available selected peers, excluding Thailand; unavailable peers are listed, never zero-filled.
- **AI context:** distinct `Incident ID` per `Risk Domain` (blank → *Unclassified*). The Freedom year does not filter either context panel.
- **Thai context:** `acsc_highest_loss_type_th` names only. No cross-source country join, no risk index, no causal claim.
- `total_score` includes `limits_on_content` and is not used as corroboration.""")
    with st.expander("Quality & excluded observations"):
        st.markdown("- Freedom coverage varies by year (37 countries in 2010 → 71 in 2024); no 2026 edition.\n"
                    "- ACSC flags (12–18 Apr, 30 May–6 Jun, 16–22 Aug, 23–29 Aug 2026) are shown as published here.\n"
                    "- AIID `Risk Domain` is blank for some incidents; they appear as Unclassified.")
        if thai is not None:
            st.dataframe(thai[thai.acsc_flag.notna()][["week_start", "week_end", "acsc_flag"]], hide_index=True, width="stretch")
    scoped_reset_hint()

# ================================================================ Q2
elif tid == "q2":
    st.header("Q2 · How do recorded AI incidents vary by occurrence year and Risk Domain?")
    if aiid is None:
        source_error("AIID workbook", err_a)
    else:
        y0, y1 = S["q2_years"]
        a_y = calc.incidents_in_years(aiid, y0, y1)
        a_yd = a_y[a_y["domain"].isin(S["q2_domains"])]
        cov = calc.coverage(a_y)
        cutoff = aiid["date"].max()
        chips(f"Years {y0}–{y1}", f"Domains {len(S['q2_domains'])}/{len(domains_all)}")
        if y1 >= 2026:
            st.markdown(badge(f"2026* · Incomplete observation year — occurrences recorded through {fmt_d(cutoff)} "
                              "(export 2026-10-26); no full-year projection", "warn"), unsafe_allow_html=True)
        st.markdown(f'<div class="cap">Classified {cov["classified"]:,} / all in selected years {cov["all"]:,} · '
                    f'{num(cov["pct"], "{:.1f}")}% &nbsp;|&nbsp; Displayed after domain selection: {len(a_yd):,}</div>',
                    unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Distinct recorded incidents by occurrence year and Risk Domain")
            st.markdown('<div class="sub">Source: AIID · unit: distinct incidents · occurrence date (not report or modified date)</div>',
                        unsafe_allow_html=True)
            if len(a_yd) == 0:
                st.markdown(note("No incidents match these filters (not a load error).", "miss"), unsafe_allow_html=True)
            else:
                show(charts.q2_lines(calc.yearly_domain_counts(a_yd)), "q2", "lines")
                top = calc.domain_counts(a_yd).iloc[0]
                st.markdown(note(f"For {y0}–{y1}, {cov['classified']:,}/{cov['all']:,} recorded incidents have a domain; "
                                 f"{len(a_yd):,} remain after domain selection. Largest displayed domain: "
                                 f"{top['domain']} ({int(top['incidents']):,}).", "info"), unsafe_allow_html=True)
        ev = _evidence()
        ids = deepfake.candidate_ids(ev)
        tt = calc.yearly_totals(a_yd, ids)
        with st.container(border=True):
            st.subheader("All incidents vs candidate deepfake subset")
            st.markdown(badge("Provisional — review pending", "warn"), unsafe_allow_html=True)
            if len(a_yd):
                n_df = int(tt["candidate_deepfake"].sum())
                show(charts.q2_subset(tt), "q2", "subset")
                st.markdown(note(f"Candidate deepfake (keyword rule, provisional): {n_df:,} of {len(a_yd):,} incidents "
                                 f"({n_df / len(a_yd) * 100:.1f}%) in the selection. The subset overlaps domains; "
                                 "it is not a domain and is never added to totals. A nonmatch means “no keyword match”, "
                                 "not “not a deepfake”.", "warn"), unsafe_allow_html=True)
        with st.expander("Candidate rule & examples"):
            st.markdown(f"**Rule:** `{C.DEEPFAKE_RULE_VERSION}`. Unicode NFKC normalisation, Unicode dashes → `-`, "
                        r"case-insensitive whole-token pattern `\bdeep[\s-]?fakes?\b` searched in `Implicated Systems`, "
                        "`title` and `description`. Any field match makes a candidate; each ID counts once. "
                        "Missing text is skipped. Misinformation is not treated as equivalent. "
                        f"Whole-dataset candidate IDs under this rule: **{len(ids):,}** (provisional, not approved).")
            ex = aiid[aiid["Incident ID"].isin([39, 1112, 1785, 728])][["Incident ID", "title", "Implicated Systems"]].copy()
            ex["Keyword match"] = ex["Incident ID"].map(lambda i: "match" if i in ids else "no keyword match (boundary example)")
            ex["Matched fields"] = ex["Incident ID"].map(lambda i: ", ".join(sorted(set(ev[ev["Incident ID"] == i]["field"]))))
            st.dataframe(ex, hide_index=True, width="stretch")
            st.markdown("**Evidence (all matches):**")
            st.dataframe(ev, hide_index=True, width="stretch")
        with st.expander("Methods & source"):
            st.markdown("""- Count = distinct `Incident ID`; x = occurrence `year` (from `date`), not `Date Modified`.
- A(Y) = incidents in the selected years **before** domain filtering; coverage = classified / A(Y). The domain filter changes the charts, not the coverage denominator.
- Blank `Risk Domain` is shown as *Unclassified* (raw value retained). Domain lines show zero only for domains within years that have records; years with no records are not drawn.
- Recorded incidents are curated reports, not all real-world events.""")
        with st.expander("Quality & excluded observations"):
            cy = calc.coverage_by_year(a_y)
            st.markdown("Per-year classification coverage:")
            st.dataframe(cy, hide_index=True, width="stretch")
            est = a_y["Estimated Date"]
            st.markdown(f"`Estimated Date`: true {int((est == 1).sum())}, false {int((est == 0).sum())}, "
                        f"unknown {int(est.isna().sum())} (unknown ≠ false).")
        scoped_reset_hint()

# ================================================================ Q3
else:
    st.header("Q3 · How do weekly reported scam cases, losses and loss per case change?")
    if thai is None:
        source_error("Thai workbook", err_t)
    else:
        w = calc.prepare_weeks(thai, *map(pd.Timestamp, S["q3_range"]), S["q3_view"])
        cc = calc.coverage_counts(w)
        view_lbl = "Comparable — proposed policy" if S["q3_view"] == "comparable" else "As published"
        chips(f"Weeks {fmt_d(S['q3_range'][0])} – {fmt_d(S['q3_range'][1])}", view_lbl, f"Layout {S['q3_layout']}")
        st.markdown(badge("Quality policy proposed — confirmation pending", "warn")
                    + badge("Layout A/B decision pending", "warn"), unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Weekly totals · all reported scam types")
            st.markdown('<div class="sub">Source: compiled ACSC briefing figures · reported cases and THB · '
                        'gaps = not reported or excluded (never zero)</div>', unsafe_allow_html=True)
            sel_weeks = set()
            for i, f in enumerate(charts.q3_figures(w, S["q3_layout"])):
                ev = show(f, "q3", f"fig{i}", select=True)
                if ev and ev.selection.points:
                    for p in ev.selection.points:
                        cd = p.get("customdata")
                        sel_weeks.add(cd[0] if isinstance(cd, (list, tuple)) else cd)
            pk = calc.peak_loss(w)
            if pk is not None:
                r0 = pk.iloc[0]
                tied = "; ".join(fmt_w(a, b) for a, b in zip(pk.week_start, pk.week_end))
                st.markdown(note(f"Highest displayed total reported loss · {tied} · THB {r0.acsc_loss_baht / 1e6:,.1f} million "
                                 "(all types). Among valid included points in this selection only. Type named highest-loss "
                                 f"in that briefing: {r0.acsc_highest_loss_type_th if pd.notna(r0.acsc_highest_loss_type_th) else 'Unavailable'}.",
                                 "info"), unsafe_allow_html=True)
            excl = w[w["excluded"]]
            if len(excl):
                st.markdown(note("Excluded from this comparable view: " + "; ".join(
                    f"{fmt_w(a, b)} ({rs})" for a, b, rs in zip(excl.week_start, excl.week_end, excl.excluded_reason)), "warn"),
                    unsafe_allow_html=True)
            if S["q3_view"] == "as_published" and w["acsc_flag"].notna().any():
                st.markdown(note("As published: flagged points are shown unchanged; the suspect and overlapping periods "
                                 "may stretch the axes. Overlapping periods must not be read as a deduplicated total.", "warn"),
                            unsafe_allow_html=True)
            if cc["included"] == 0:
                st.markdown(note("No eligible reporting weeks in this selection.", "miss"), unsafe_allow_html=True)
            else:
                rs = calc.range_summary(w)
                st.markdown(note(f"{cc['included']} eligible periods: {rs['cases']:,.0f} reported cases and "
                                 f"THB {rs['loss'] / 1e6:,.0f} million in total; weighted loss per case "
                                 f"THB {rs['ratio']:,.0f} (sum of loss ÷ sum of cases over the same periods).", "info"),
                            unsafe_allow_html=True)
            if sel_weeks:
                st.markdown("**Selected points**")
                st.dataframe(w[w.week_start.dt.strftime("%Y-%m-%d").isin(sel_weeks)][
                    ["week_start", "week_end", "acsc_cases", "acsc_loss_baht", "loss_per_case_calc", "acsc_flag"]],
                    hide_index=True, width="stretch")
        with st.expander("Weekly detail (all selected weeks)", expanded=False):
            t = w.copy()
            t["Status"] = np.where(t["excluded"], "Excluded by proposed policy",
                          np.where(~t["acsc_reported"], "Not reported / unavailable",
                          np.where(t["eligible"], "Included", "Reported, incomplete values")))
            t["Original period"] = [f"{fmt_w(a, b)} ({int(d)} days)" if pd.notna(d) and d != 7 else ""
                                    for a, b, d in zip(t.orig_start, t.orig_end, t.days)]
            show_cols = {"week_start": "Week start", "week_end": "Week end", "Original period": "Original period",
                         "Status": "Status", "acsc_cases": "Cases (all types)", "acsc_loss_baht": "Loss THB (all types)",
                         "acsc_loss_precision": "Loss precision", "loss_per_case_calc": "Calculated THB/case",
                         "acsc_loss_per_case_baht": "Source THB/case", "diff_vs_source": "Calc − source",
                         "acsc_top_type_th": "Top-volume type (name)", "acsc_highest_loss_type_th": "Highest-loss type (name)",
                         "acsc_flag": "Source flag", "notes": "Notes", "publisher": "Publisher",
                         "article_date": "Article date", "acsc_source_url": "Source"}
            st.dataframe(t[list(show_cols)].rename(columns=show_cols), hide_index=True, width="stretch",
                         column_config={"Source": st.column_config.LinkColumn("Source", display_text="link")})
            st.caption("Top-volume and highest-loss names are descriptive; they do not partition the all-type totals.")
        with st.expander("Methods & source"):
            st.markdown("""- **Cases** = `acsc_cases`; **losses** = `acsc_loss_baht` (÷ 1,000,000 for display only); **loss per case** = loss ÷ cases, only when both exist and cases > 0 (an observed zero loss with positive cases gives 0).
- All series are **all reported types**; type names are annotations, not filters.
- Missing weeks, unreported weeks and excluded weeks are gaps — no interpolation, zero filling or smoothing. Rounded losses are drawn with open markers (≈).
- Range summary sums cases and losses over the same eligible periods and divides sums (no averaging of weekly ratios).
- Figures are reported briefing figures, not a complete police open-data census.""")
        with st.expander("Quality & excluded observations"):
            q1, q2, q3, q4 = st.columns(4)
            q1.metric("Selected weeks", cc["selected"]); q2.metric("Reported", cc["reported"])
            q3.metric("Included", cc["included"]); q4.metric("Paired (cases & loss)", cc["paired"])
            st.markdown(f"Policy: `{C.QUALITY_POLICY_VERSION}` — excludes 16–22 Aug 2026 (suspect) and the eight-day "
                        "30 May–6 Jun 2026 overlap from the comparable view; 12–18 Apr and 23–29 Aug are kept with warnings.")
            st.markdown("**Date exception:** raw ACSC start 30 May 2026 is attached to panel week 31 May 2026 (both end 6 Jun; "
                        "8 days). Both dates are retained above.")
            st.markdown("**Source-ratio reconciliation** (calculated − supplied; the rounding convention is not yet confirmed):")
            rec = w[w["acsc_reported"]][["week_start", "loss_per_case_calc", "acsc_loss_per_case_baht", "diff_vs_source"]].copy()
            rec["Reading"] = np.where(rec["diff_vs_source"].isna(), "Comparison unavailable",
                              np.where(rec["diff_vs_source"].abs() <= 0.5, "within ±0.5 THB/case",
                                       "outside ±0.5 — inspect"))
            st.dataframe(rec.rename(columns={"week_start": "Week start", "loss_per_case_calc": "Calculated",
                                             "acsc_loss_per_case_baht": "Supplied", "diff_vs_source": "Difference"}),
                         hide_index=True, width="stretch")
            fl = w[w["acsc_flag"].notna()][["week_start", "week_end", "excluded_reason", "acsc_flag"]]
            if len(fl):
                st.markdown("**Flagged source records:**"); st.dataframe(fl, hide_index=True, width="stretch")
            miss = w[~w["acsc_reported"]]["week_start"]
            st.caption(f"{len(miss)} selected weeks have no briefing (not zero cases): " + ", ".join(d.strftime("%d %b %Y") for d in miss))
        scoped_reset_hint()
