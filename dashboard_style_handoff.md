# Dashboard style handoff: Q1–Q3

Status: proposed visual specification, 2 November 2026. Output: this English Markdown document only. No code, dashboard, mockup or changes to source documents are included.

## Reference and authority

Read references: the latest analytical handoff, **dashboard_handoff (3).md** (the current detailed reference for the requested dashboard_handoff.md), **dashboard_brd.md**, and attached **messageImage_1793591241032(1).jpg**. The image informs hierarchy, compact cards, spacing and restrained red accents only. Its figures, dates, flags, country symbols, categories, conclusions, illustrations and policy recommendations are not analytical inputs.

The BRD's formulas, filter populations, source restrictions and interpretation safeguards govern this styling. Use exactly three Q1–Q3 tabs, Streamlit components and Plotly charts. Retain groups 01/02/04 only; Thai numerical input remains the workbook's `weekly_panel`, with `acsc_weekly` for reporting-period detail. No new dataset, cross-source join, risk score or fourth KPI is introduced.

**Design decisions remain proposals unless confirmed by the team.** UI language is pending; English document language does not settle UI language. Source findings below are attributed to the analytical documents, not new source-data checks. Q1 donut styling is a proposed presentation alternative to the documents' bars; Q3 A/B remains unresolved. Neither visual option changes calculations.

## 1. Design tokens

Use flat surfaces. Red is an emphasis colour, not a universal danger encoding. No photographic background, globe texture, mascot, glow, glass effect or large gradient is required.

| Token | Exact Hex | Use |
| --- | --- | --- |
| Canvas | `#0C1018` | App background |
| Sidebar | `#101621` | Scoped controls |
| Surface | `#151C28` | Cards and chart panels |
| Raised surface | `#1D2736` | Hover, expanded detail and table headers |
| Decorative border | `#334155` | Nonessential panel separation |
| Control border | `#62728A` | Input boundaries and interactive outlines |
| Primary text | `#F4F7FC` | Titles, values and table text |
| Secondary text | `#B0BCCE` | Units, notes and subtitle |
| Muted text | `#8C9BB0` | Timestamps and supplementary labels; never opacity-reduced |
| Accent | `#FF6B7A` | Active tab indicator, Thailand, candidate deepfake |
| Accent hover | `#FF8A96` | Hover/focus accent; not an extra data category |
| Selected surface | `#34212C` | Selected chips and controls |
| Focus ring | `#63D6E5` | 2 px keyboard outline, 2 px offset |
| Warning foreground / background | `#F2C66D` / `#2B2316` | Source anomalies, provisional rule and approximation |
| Error foreground / background | `#FF9BA4` / `#321E28` | Actual loading/validation errors |
| Informational foreground / background | `#8CB9FF` / `#172437` | Methods and scope notes |
| Neutral missing-state surface | `#19212E` | Unavailable/excluded placeholders |
| Grid | `#334155` | Thin chart grid on surface |
| Button foreground | `#0C1018` | Text on accent-filled buttons |

Primary, secondary and muted text on Surface calculate to approximately **15.9:1, 8.9:1 and 6.0:1** contrast respectively; these token calculations are not a rendered UI audit. Target at least 4.5:1 for normal text, 3:1 for large text and meaningful control/graphic boundaries. Check actual hover/selected/warning combinations during implementation. Decorative low-contrast borders must not be the sole cue identifying a control. Use dark foreground on accent fills; avoid white small text on red fills. Do not use opacity to fade essential text or data lines.

### Fixed categorical and metric palette

Use the source labels, not the image's simplified categories. The handoff reports these seven populated Risk Domain labels; confirm the category set at load time. Any unexpected new category requires a visible mapping review, not an arbitrary reassignment.

| Risk Domain | Colour | Q2 line marker |
| --- | --- | --- |
| Malicious Actors & Misuse | `#63D6E5` | Circle |
| AI system safety, failures, and limitations | `#B9A0FF` | Square |
| Discrimination and Toxicity | `#8CB9FF` | Diamond |
| Misinformation | `#F2CF73` | Triangle up |
| Privacy & Security | `#F3A6D7` | Triangle down |
| Human-Computer Interaction | `#81D6AF` | Cross |
| Socioeconomic & Environmental Harms | `#F5AC79` | X |
| Unclassified | `#9BA6B8` | Open circle; dotted line |

Use this mapping consistently in Q1/Q2, independent of sorting or filters. Candidate deepfake is **not** in this domain palette: reserve `#FF6B7A`, dashed line, diamond marker for the separate subset comparison. Q3 metric colours: cases `#63D6E5`, total loss `#FF6B7A`, calculated loss/case `#B9A0FF`. Metric colours do not denote alert severity.

## 2. Typography and spacing

**System-font fallback stack:** `Tahoma, "Leelawadee UI", "Noto Sans Thai", "Thonburi", "Arial Unicode MS", system-ui, sans-serif`. Use only fonts already installed; do not fetch font files, icon packs or images. Plotly and Streamlit must use matching available fallback families. Verify Thai vowels/tone marks and mixed Thai/Latin/numeral text on the actual device; OS fallbacks may differ.

| Element | Desktop size / weight | Line height |
| --- | --- | --- |
| App title | 28 px / 700 | 1.3 |
| Tab question title | 22 px / 650–700 | 1.4 |
| Panel heading | 18 px / 600 | 1.4 |
| KPI value | 30 px / 700; reduce to 26 px on small screens | 1.25 |
| Body, inputs and table | 14–16 px / 400–500 | 1.6 |
| Chart ticks and legend | 13–14 px / 400 | 1.45 |
| Source/caption | 13 px / 400 | 1.6 |

Use tabular numerals where supported, without relying on that feature for alignment. Do not insert fixed card heights that clip Thai marks or long names. Avoid forced uppercase except ISO codes. Chart labels must not fall below 12 px to make a dense plot fit.

Spacing scale: **4, 8, 12, 16, 24, 32 px**. Desktop page padding 24–32 px, sidebar padding 20 px, panel padding 20–24 px, panel gap 24 px, card gap 16 px, label-to-control gap 8 px. Card radius 12 px; input/button radius 8 px; badges 6 px. Borders 1 px; active-tab underline 3 px. No shadow needed; optional subtle elevation must not replace borders. Small-screen padding 16 px, panel padding 16 px, gaps 16 px. Prefer native Streamlit spacing when exact dimensions are unsupported, preserving the hierarchy rather than fragile internal-selector overrides.

## 3. Layout and responsive behavior

**Reading order:** header → Thai weekly KPI strip → Q1/Q2/Q3 navigation → question title and active scope → charts/context → short insights → detail/methodology expanders. Sidebar stays visually separate. Do not reproduce the image's all-questions-on-one-canvas composition.

- **Header:** proposed title “Digital Risk: Q1–Q3”; short subtitle explaining separate assessments, recorded incidents and reported scams. Keep title left, source/edition information below. No single global year badge suggesting shared periods.
- **Sidebar:** 288–320 px proposed width on desktop. Show the active tab name and only its relevant control groups, each explicitly labelled by panel/source. No global date filter.
- **KPI strip:** exactly three equal cards on desktop in the requested order: total reported losses, total reported cases, calculated loss/case. Shared eyebrow “Thai reported scams · Q3 selection” and one explicit reporting-period label. This is contextual even when Q1/Q2 is open, not a measure filtered by their controls.
- **Tabs:** precisely Q1, Q2, Q3, each with a short descriptive label and full question inside. Selected tab uses accent underline plus text weight, not colour alone. Long translated labels may wrap; retain usable touch targets.
- **Panels:** heading, source-period/unit subline, plot, legend, insight, then source caption. Never put required period/units only in hover. Q1 main bars take a full-width row; its AI context and Thai context may form a 50/50 second row. Q2 and both Q3 layout options remain vertically aligned.
- **Tables:** full-width, raised headers, horizontal separators, 44 px minimum interactive row target; row height expands for wrapped Thai. No fixed-width clipped type names without accessible full detail. Use ISO codes alongside country names, not flag images.
- **Methods:** native expanders headed “Methods & source”, “Quality & excluded observations”, and Q2 “Candidate rule & examples”. These are within tabs; never a fourth tab.

**Proposed breakpoints:** at ≥1200 px allow Q1 context columns; at 768–1199 px stack context panels and keep three KPI cards only if their content fits. At <768 px collapse sidebar using Streamlit's normal toggle, stack KPI cards and all panels, use 22 px app title and 20 px question title. Keep charts full-width with readable minimum height (roughly 300 px) rather than scaling down text. Allow table-only horizontal scrolling, not page-wide scrolling. Native component capabilities may constrain exact breakpoints; validate content fit and reading order, not only viewport numbers. No sticky strip on small screens that obscures charts or controls.

## 4. Sidebar controls and scope indicators

| Active tab / group | Controls and visible scope | Proposed defaults from analytical documents |
| --- | --- | --- |
| Q1 · Freedom comparison | Single `data_year`; ASEAN peer multiselect; Thailand fixed/highlighted. Caption: “Only country comparison”. Retain unavailable requested peers visibly. | 2024; seven handoff-listed available peer candidates, pending selection |
| Q1 · Global AI context | Occurrence-year range and Risk Domain including Unclassified; caption “Only AI context”. | All available occurrence years/domains |
| Q1 · Thai context | Reporting-period range; source-warning explanation. Caption “Type names only; source records may include flagged periods”. | Available briefing range |
| Q2 · AI occurrence | Occurrence years and domain multiselect including Unclassified. Caption explains coverage uses years before domain filtering. | Full available year range; all domains |
| Q3 · Thai reporting | Whole panel-week range; quality view (“Comparable — proposed policy” / “As published” if implemented). Do not introduce type filters on totals. | Week starts 2025-11-09–2026-10-25; pending comparable policy |

Controls for Q1 and Q2 must retain independent state. Q1 Thai context and Q3 may also use different ranges; do not sync them implicitly. Above charts, show text chips for active year/range, peer count, domain selection and quality view with a visible group label. Chips summarize state, not new cross-source controls.

**Reset:** full-width outlined button “Reset Q1/Q2/Q3”, neutral surface, Control border, primary text; accent border on hover and cyan keyboard ring. It resets only the active tab's controls and chart selections to agreed defaults. Under the top strip outside Q3, provide a quiet “Edit Q3 selection” navigation action; Q1/Q2 Reset must not change strip values. No “Reset all” or global danger-coloured Reset.

## 5. Weekly KPI strip

Use native metric components within bordered containers where supported. Top accent strokes may use loss/cases/ratio metric colours; all values use Primary text. Iconography is optional and secondary to text. No fourth card, fake-news count, risk score or decorative alert number. `afnc_false_finance` stays outside MVP; a count above zero does not trigger danger styling.

The strip uses the **latest eligible Q3 reporting week within the Q3 selected range**, as proposed in the analytical handoff. Its shared subtitle must state that week, Q3 range and quality policy; if a newer selected week is missing/excluded, show “Newer selected period unavailable/excluded” with its date. Never silently label an older eligible record “this week”. If no eligible week exists, all three cards show unavailable.

| Card | Value presentation | Supporting text |
| --- | --- | --- |
| Total reported losses | THB million for readability, clearly labelled; calculate from raw `acsc_loss_baht` | “All reported types”; approximation badge when source loss is rounded |
| Total reported cases | Grouped integer from `acsc_cases`; unit “reported cases” | “All reported types” |
| Calculated loss per case | `acsc_loss_baht / acsc_cases`; THB/case, only valid inputs and cases >0 | “Calculated”; source-provided ratio and reconciliation in detail table |

**Delta proposal requiring confirmation:** cases/loss show signed percentage against the immediately preceding adjacent seven-day eligible reporting period; require both same-policy valid values and a positive prior denominator. Ratio shows signed absolute THB/case change over the same two periods, each with valid ratio inputs. Never skip a missing/excluded predecessor to find an older comparator. Irregular/overlapping periods cannot supply a comparable delta. Display “Δ unavailable — no comparable prior period” instead of inventing a number; use recomputed totals, not published change fields. Deltas are descriptive, not proof of worsening/improving risk: neutral Secondary text with explicit +/− and “vs [period]”, not automatic red/green judgments. This proposal adds no fourth KPI and changes none of the defined current-week values.

Unavailable value: em dash and “Unavailable”, not zero or an empty red card. Approximate ratio inherits the rounded-loss caveat. Excluded status is different from unavailable input and retains its reason in detail. Display rounding never changes calculations; source-ratio rounding convention remains pending.

## 6. Q1 styling

**Country comparison:** proposed horizontal bars with a zero-based 0–35 axis, `limits_on_content` only. Thailand uses Accent plus bold label and explicit “Thailand” text; peers use `#8CB9FF`. Add numeric endpoint labels if space permits. Header states selected `data_year`, report edition and “Points /35 · higher = greater content freedom”. No flag assets, crown, threat rating or claim that all ASEAN members are covered. Missing requested country-years appear in a separate unavailable list, not zero-length scored bars. Optional `total_score` context must say “/100; includes limits_on_content” and cannot share the /35 scale.

**Global Risk Domain donut proposal:** 2D flat donut, 60% hole, fixed domain palette, Surface-coloured 2 px slice separators. Count distinct incidents using the panel's existing filter population; show Unclassified when present. Centre label is “Recorded incidents” and that population's total, not a risk index. Adjacent external legend/table lists full domain, count and percentage using the same total including Unclassified. Tiny slices retain legend rows; do not collapse into invented “Other”, hide Unclassified or create a deepfake wedge. Never use 3D/exploded sectors. Do not silently rebase percentages by hiding legend items; treat legend as informational. For small screens, place the legend below and keep an accessible count table. If category partition/exclusivity cannot be validated, show the BRD's count bars instead; a donut would imply an unsupported partition. Team confirmation is needed for replacing the specified bars with this donut.

**Thai highest-loss-type context table:** distinct container labelled “Thailand · reported highest-loss type names”. Show panel week and original reporting dates where different, type name, quality/precision and source. No loss/case totals next to a type name in a way that implies type attribution. Show missing type names as unavailable and long Thai names wrapped. Each of the three Q1 panels has its own source and period; a small neutral note states that they are separate context, not causal or same-period comparisons.

## 7. Q2 styling

**Domain chart:** flat Plotly lines, 2.5 px stroke, 5–6 px markers, year ticks, y-axis “Distinct recorded incidents”, zero-based count scale. Apply fixed domain colours/markers; Unclassified uses grey dotted line/open circle. Legend wraps below, never overlays the plot. Full labels remain accessible even where compact legends use reviewed display aliases. Do not copy the image's labels or categories. Use sidebar controls for analytical filtering; a legend interaction must not silently change KPI/coverage populations.

**Subset comparison:** a separate aligned chart with same occurrence-year span. Total for A(Y,D): `#F4F7FC` solid line/circle; candidate deepfake: Accent dashed 3 px line/diamond. Label “Candidate deepfake · provisional rule” until approval. Never stack the subset, add it as a domain or sum it with total. Keep rule version, matched-field examples and review status accessible; do not embed an assumed final count.

**Coverage strip:** compact text directly above domain chart, e.g. placeholders “Classified [n] / all in selected years [N] · [p]%” and “Displayed after domain selection: [m]”. These are live bindings, not sample results. Coverage uses A(Y) before domain selection; changing domain selection must not visually relabel its denominator. Provide per-year coverage in table/hover as well.

**Incomplete year:** label the 2026 tick “2026*”, with an amber outline badge “Incomplete observation year” and source cutoff/snapshot note from loaded metadata. Use a light bounded background band if helpful, without obscuring lines; do not shade all 2026 incidents as excluded. No annualized extrapolation, implied full-year growth or trend conclusion.

## 8. Q3 styling and pending layout

**Decision remains pending. Recommend A** to reflect the team's original preference; retain B as the analytical handoff alternative. Both preserve identical values, filters, eligibility and gaps.

| Option | Visual specification |
| --- | --- |
| **A — recommended, not approved** | Plotly dual-axis combination: cases as flat cyan bars, left axis “Total reported cases”; loss as coral solid line/circles, right axis “Total reported losses (THB million)”. Both magnitude axes start at zero and show distinct metric labels/legend keys. A separate aligned violet loss/case chart below uses “Calculated loss per case (THB/case)”. Do not align arbitrary axis ranges to suggest correlation. |
| **B — pending alternative** | Three vertical plots: cases cyan, losses coral, loss/case violet, each with its own labelled zero-based scale and the same weekly x range. Prefer consistent line/marker treatment for trend comparisons, or cases bars if the team prefers; no shared magnitude scale between units. |

Use reporting-week tick labels that include year at boundaries; hover shows full date range. Approximate loss points get a visible “≈ / rounded” tooltip/text cue. Missing/excluded observations remain breaks; do not draw interpolating lines or zero-height bars. Show excluded weeks as faint full-height bands/flags below the data region with a reason, never as zero values. As-published anomalous points remain individually identified and may change axis extent; do not clip them to make the plot look smooth. Offer source detail rather than silently changing the scale or data.

**Peak annotation proposal:** identify a maximum only among valid included points in the displayed selection and state “Highest displayed total reported loss · [period] · [value/unit]”. A separate descriptive row may say “Type named highest-loss in this briefing: [name]”. Never write “[type] caused [total loss]”, position the all-type amount as the named type's measured loss, or call the largest included point the true real-world maximum. Disclose excluded periods; ties share the label or are listed in detail, not arbitrarily ranked. Limit annotations to avoid collisions.

## 9. Insights, quality and interaction states

Insights sit **below** their chart in a Surface container with a 2 px informational left border, 14–16 px text, at most two short sentences. Use one or two descriptive comparisons supported by the current filter population, followed by a caveat when needed. They are not a fixed conclusion copied from the image.

Permitted placeholder structures: “In [data_year], Thailand's component is [value]/35; [available]/[selected] selected peers have data.” “For [years], [classified]/[all] recorded incidents have a domain; [displayed] remain after domain selection.” “The latest eligible week is [period]; loss is [value/unit, approximation if applicable].” Populate only when the stated inputs/definitions support the sentence. Empty inputs produce a useful unavailable explanation. No claims about causality, policy success, danger levels or all real-world incidents; avoid an overall summary that adds domains, deepfake counts or source units together.

| State | Visual and content treatment |
| --- | --- |
| Source/method note | Secondary text, source/edition, observation period, unit and denominator; reference link with meaningful text |
| Provisional rule | Amber-outline badge “Provisional — review pending”; rule/evidence expander, no approved final count |
| Missing observation | Neutral surface, em dash plus “Unavailable”; plot gap and reason/date in table |
| Excluded period | Neutral marker and amber-outline “Excluded by [policy]”; reason and original values retained in detail |
| Source anomaly/overlap | Amber note icon plus explicit flag text; do not auto-remove every flagged record or equate warning colour with case severity |
| Approximate value | “≈” and “Rounded source loss”; maintain precision note in hover/table, no false decimal certainty |
| Loading | Native progress/spinner with affected source/panel label; no invented KPI placeholders or random chart data; avoid flashing animation |
| Empty filter result | Neutral explanatory text and scoped Reset; distinguish no matching records from source failure |
| Load/validation error | Error foreground/background, clear affected source and recoverable action; never render zero values to conceal failure |

Carry forward the **pending**, specific ACSC policy: proposed comparable view excludes suspect 16–22 August 2026 and overlapping eight-day 30 May–6 June 2026; retains 12–18 April and 23–29 August totals with warnings. Show original 30 May start versus panel 31 May start, both ending 6 June, in detail. Policy badges must say proposed until confirmed. Keep included/reported/selected period counts in the quality area as inline metadata, not additional top KPI cards. Do not alter ranges or policies merely for a visually smoother chart.

Native tables must expose full detail beyond tooltip-only information, support readable source links and preserve Thai text. Use descriptive expander labels and keyboard-visible focus. Essential actions need approximately 44 px touch height. Do not rely on emoji or fetched icon assets for status meaning.

## 10. Visual acceptance checklist and remaining decisions

These are **planned review checks**, not passed UI tests; no dashboard has been implemented in this task.

- [ ] Exactly three tabs and three weekly KPI cards; no AFNC KPI, fourth tab, unsupported labels, copied numbers, flags or conclusions from the reference image.
- [ ] Body/caption/control contrast checked in all states; meaningful chart lines/control boundaries distinguishable on dark surfaces. Category identification does not rely only on colour.
- [ ] Thai marks, long Thai type names, mixed-language text and full source labels render without clipping in Streamlit and Plotly using local fonts.
- [ ] Desktop, intermediate and narrow layouts preserve reading order, accessible sidebar toggle, usable tabs and non-overlapping legends/labels; no page-wide horizontal scroll.
- [ ] Units, selected periods, source editions/snapshots, active scopes, unavailable states and provisional labels visible without hover. Q1 shows /35 and higher-is-freer direction.
- [ ] Domain colours stay fixed across Q1/Q2; donut only used after partition validation and team presentation approval. Unclassified remains represented; deepfake is separate and overlapping.
- [ ] Coverage denominator remains A(Y), independent of domain filter; displayed A(Y,D) counts are separately labelled. 2026 is visibly incomplete.
- [ ] Q3 A/B choice recorded; all axes and legends identify metrics/units; peak annotation refers to total loss separately from the descriptive type name.
- [ ] KPI period and delta comparator explicit; no skipped missing comparator, invented fourth KPI or automatic increase/decrease danger judgement.
- [ ] Q3 missing/excluded weeks stay visible as gaps; source values, original periods, precision and policy-specific warnings remain inspectable.
- [ ] Tab-local controls/Reset keep other tabs and the Q3-bound strip state intact; Q1 Freedom year does not affect either contextual source.
- [ ] Insights are derived from active data and retain caveats; loading/empty/error states are distinct; no unsupported causal/policy conclusions.

**Remaining decisions:** UI language; selected peers and defaults; deepfake rule approval; ACSC eligibility policy; Q3 A versus B; whether Q1 count bars may become a validated donut; proposed delta display/comparison convention; source-ratio rounding/display convention. This style handoff recommends A and the specified dark visual system without claiming these unresolved analytical or layout choices are approved. Stop before implementation.
