# Digital Risk: Q1–Q3 dashboard

Streamlit + Plotly + Pandas dashboard with exactly three question tabs, built from
`dashboard_brd.md`, `dashboard_handoff.md` and `dashboard_style_handoff.md`
(reference image: `messageImage_1793591241032.jpg`, used for hierarchy/spacing only).

## Required local data (not committed)
Place these instructor files in the **project root** (or `data/`, or any folder named by the
`DATAVIZ_DATA_DIR` environment variable). A duplicate suffix such as ` (1)` is accepted; two
different files matching one name raise an "Ambiguous input" error instead of guessing.

| File | Sheet / header |
| --- | --- |
| `AIID_Excel_Export-20261026.xlsx` | `Incidents`, Excel row 3 (pandas header offset 2) |
| `freedom_on_the_net_scores.csv` | CSV row 1 |
| `thai-disinfo-scam-dataset.xlsx` | `weekly_panel` and `acsc_weekly`, row 1 |
| `00_Data_Guide_TH.pdf` | documentation only |

They are listed in `.gitignore`, so they stay on your machine but remain readable by the app.
Group 03 and external data are not used.

## Run
```
python -m venv .venv
.venv\Scripts\activate          # Windows (source .venv/bin/activate elsewhere)
pip install -r requirements.txt  # developed on Python 3.13
streamlit run app.py
python -m pytest -q              # 14 checks against the supplied files
```

## Defaults (all proposals in the BRD, pending team confirmation)
- UI language: English. Q1: data year 2024, seven peers (KHM, IDN, MYS, MMR, PHL, SGP, VNM), all AI years/domains, all briefing periods.
- Q2: all occurrence years, all domains incl. Unclassified.
- Q3: week starts 2025-11-09 – 2026-10-25, "Comparable — proposed policy", layout A (layout B selectable; decision pending).
- Reset is per tab and clears that tab's chart selections only.
- Versions: `deepfake-keyword-v1` (provisional rule), `acsc-comparable-v1` (proposed: excludes 16–22 Aug 2026 and the eight-day 30 May–6 Jun 2026 overlap; keeps 12–18 Apr and 23–29 Aug with warnings).

## Layout
`app.py` UI · `dashboard/data.py` loading + validation · `dashboard/calc.py` BRD formulas ·
`dashboard/deepfake.py` keyword rule · `dashboard/charts.py`, `theme.py`, `config.py` styling · `tests/`.

## Known limitations
- The tab strip is a styled radio group so the sidebar can show only the active tab's controls.
- Candidate-deepfake counts are exploratory until the team approves the rule; Q3 range summary is an optional extra; no type-specific loss or estimated type cases.
- Visual checks were done in desktop Chromium at 1440 px and 420 px widths; contrast and Thai rendering are not formally audited.
