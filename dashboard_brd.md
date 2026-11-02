# Business Requirements Document: Digital-risk analysis, Q1–Q3

Status: requirements draft for team review. Date: 2 November 2026. Deliverable: this BRD only; no implementation or additional document.

Primary technical reference: **dashboard_handoff (3).md**, sections 2–7, read in full for this BRD. Its inventory, quality findings and example observations are attributed to that handoff unless explicitly marked as rechecked here. The team's latest instructions govern conflicts and additions. **Confirmed** means specified by the team; **Proposed** means awaiting confirmation; **Pending** identifies unresolved decisions. Acceptance scenarios are planned tests, not completed tests.

## 1. Project overview

**Problem and purpose.** The team needs a reproducible way to compare Thailand's content-freedom assessment with available ASEAN peers, examine recorded AI incidents and a defined deepfake subset, and inspect weekly Thai reported scam totals and named leading scam types. These are distinct analytical lenses with different coverage, units and time periods. Internet-freedom scores and all recorded AI incidents must not be described collectively as cybersecurity incidents.

**Proposed audience:** the student project team, instructor and readers reviewing these three questions. Intended benefits are clear comparisons, traceable calculations and visible limitations, without overstating prevalence or causation.

**Instructor/data constraints:** use provided groups 01, 02 and 04 and the uploaded guide only; exclude group 03 and external datasets. **Confirmed team scope/technology:** exactly three Q1–Q3 tabs using Python, Pandas, Streamlit and Plotly. Peer selection, detailed defaults, deepfake definition, ACSC eligibility policy, Q3 layout and UI language remain design decisions.

**Reference reconciliation:** the handoff's earlier prohibition on creating a BRD applied to its own step; this request authorizes the BRD. Its three-aligned-chart Q3 proposal is not an approved layout: the team's original dual-axis preference is an explicit alternative. This BRD adds the requested incomplete-2026 label and source-ratio reconciliation. It does not change the questions or revise the handoff.

## 2. Objectives and question-to-data mapping

| Question and user benefit | Source tables and fields | Measures and presentation | Limitations |
| --- | --- | --- | --- |
| **Q1:** How does Thailand compare with selected ASEAN countries available in the dataset on `limits_on_content` in the same `data_year`? Enables a like-year assessment comparison. | Freedom CSV: `iso3`, `country`, `data_year`, `report_edition`, `limits_on_content`; optional `total_score`. Separate Thai `weekly_panel`: dates, `acsc_highest_loss_type_th`, quality/source fields. Separate AIID `Incidents`: ID, occurrence year, `Risk Domain`. | Country comparison bars, Thailand highlighted; points /35, higher = greater content freedom. Proposed Thailand score, available-peer mean, difference and availability indicators. Separate Thai type-name/period table and global AI domain distribution including Unclassified. | Covered countries are not all ASEAN members. Context panels use independent periods and units; Thai type names are not measured type totals. `total_score` includes `limits_on_content` and is not independent corroboration. |
| **Q2:** How do recorded AI incidents vary by occurrence year and Risk Domain, and how many meet the agreed deepfake identification rule? Enables inspection of recorded patterns and classification completeness. | AIID `Incidents`: `Incident ID`, `date`, `year`, `Risk Domain`, `Implicated Systems`, `title`, `description`; `Estimated Date` for quality context. | Yearly distinct-ID lines by domain including Unclassified; separate aligned total/deepfake comparison chart; dynamic classification coverage and labelled filtered counts. | Curated recorded incidents are not all events. Deepfake overlaps domain categories; rule and final count pending. 2026 is incomplete. |
| **Q3:** How do weekly reported case totals, loss totals and loss per case change, and which scam types are named top-volume or highest-loss? Enables transparent weekly financial/case comparison. | Thai `weekly_panel`: dates, `acsc_reported`, `acsc_cases`, `acsc_loss_baht`, `acsc_loss_per_case_baht`, `acsc_top_type_th`, `acsc_highest_loss_type_th`, precision, flags, source URL. Supporting `acsc_weekly`: original dates, `days`, publisher, article date, notes. | Weekly all-type totals and calculated THB/case; top-type names as descriptive fields. Layout A or B remains pending. Optional range summary uses identical eligible periods for cases and losses. | Missing reporting, rounded figures, anomaly and overlapping period; leading-type names do not partition totals. Reported cases are not all real-world scams. |

### Reference inventory and file resolution

Use the handoff section 2 for detailed counts, grains, date ranges, missingness and quality findings rather than duplicating that inventory. In this BRD task, local file presence and the following headers were rechecked; other source findings are carried forward from the handoff, not represented as newly repeated checks.

| Input available in this workspace | Required table/header, rechecked here |
| --- | --- |
| `upload/AIID_Excel_Export-20261026(1).xlsx` | `Incidents`, Excel row 3; Pandas header offset 2 |
| `upload/freedom_on_the_net_scores(1).csv` | CSV row 1 |
| `upload/thai-disinfo-scam-dataset(1).xlsx` | `weekly_panel` and `acsc_weekly`, row 1; Pandas offset 0 |
| `upload/00_Data_Guide_TH(2).pdf` | Supporting instructor documentation; not an observation table |

These relative paths describe this workspace, not a deployment contract. Resolve configured filenames against actual supplied files at startup, allowing duplicate suffixes; report ambiguity rather than arbitrarily choosing among different versions. Do not copy another session's absolute paths. No separate `weekly_panel.csv` is available here or assumed.

## 3. Scope

**MVP:** exactly three tabs named for Q1, Q2 and Q3, containing their required charts, descriptive details, controls, local Reset, attribution and expandable methodology/quality information. Global AI context in Q1 is a separate panel, not a country-level join. The deepfake comparison remains visibly provisional until rule approval; no final result is asserted by this BRD.

**Optional, separately confirmed extensions within these questions:** `total_score` context in Q1; Q3 range summaries; incomplete type-specific loss detail or estimated top-type cases after the handoff's field/assumption reviews. They are not default MVP commitments.

**Out of scope:** group 03, external datasets, historical AIID snapshot growth, standalone AFNC analysis, cross-source country joins, combined risk scores, causal modelling, entity/report exploration, live refresh and unrequested publication/deployment. `afnc_false_finance` exists in the Thai panel but has no confirmed analytical role: **not used in the MVP** unless the team defines a specific question. Do not add a fourth tab for quality or methodology.

## 4. KPI and calculation definitions

### Filter populations

- **F:** Freedom rows for one selected `data_year`, Thailand and the requested peer set. A peer mean excludes Thailand and uses only valid available selected peers; show excluded/unavailable peers and its actual denominator.
- **A(Y):** distinct AI incident records after the selected occurrence-year range Y, **before Risk Domain filtering**. **A(Y,D):** those records after the selected domain set D, including selectable Unclassified. Q1 and Q2 have independent controls.
- **E:** Thai reporting periods in the selected panel-week range passing the explicitly displayed eligibility policy. For optional range financial summaries, use a common subset **E-paired** with both cases and loss present and valid for summation. Do not silently aggregate different period sets.

| Measure | Formula and denominator | Grain / unit | Filter and missing behavior |
| --- | --- | --- | --- |
| Q1 Thailand content freedom | THA `limits_on_content` | country-year; points /35 | F year; absent/null score = unavailable, not zero |
| Q1 peer mean, proposed | sum(valid selected-peer scores) / count(valid selected-peer scores) | selected peers in one year; points /35 | F, excluding THA; no valid peers = unavailable |
| Q1 difference, proposed | Thailand score − peer mean | selected year; points | Unavailable if either operand unavailable |
| Q1 peer availability | valid selected-peer country-years / requested peer countries, displayed as n/N | selected year; countries | Preserve unavailable selections visibly; N=0 means no peers selected, not 0% |
| AI domain counts, Q1/Q2 | count distinct `Incident ID` per domain; additionally per occurrence year for Q2 | incidents | Respective panel's year/domain filters; map null/blank domain to display category Unclassified, retaining raw value |
| Q2 classification coverage | distinct IDs with populated domain in A(Y) / distinct IDs in A(Y) ×100 | selected years and each individual year; % | Before D; denominator shown. Empty A(Y) = unavailable |
| Q2 displayed incidents | count distinct IDs in A(Y,D) | incidents | Label as selected-domain count beside full A(Y) count and coverage denominator |
| Q2 deepfake subset | count distinct matching IDs in A(Y,D); optional share = matching IDs / IDs in A(Y,D) ×100 | incidents; optional % | Same year/domain filters as comparison total; empty denominator = unavailable; provisional until approved |
| Q3 weekly cases/loss | `acsc_cases`; `acsc_loss_baht` | reporting period; reported cases; THB | Week range and policy; absent/excluded values remain gaps, not zero |
| Q3 weekly calculated loss/case | `acsc_loss_baht / acsc_cases` | reporting period; THB/case | Both valid inputs required and cases >0; otherwise unavailable. An observed zero loss with positive cases gives zero |
| Q3 source ratio reconciliation | calculated ratio versus `acsc_loss_per_case_baht`; difference = calculated − supplied | reporting period; THB/case | Retain both values and raw precision. Source missing = comparison unavailable; source ratio never fills a missing input |
| Optional range totals/ratio | sum(cases), sum(loss), sum(loss)/sum(cases), all over E-paired | range; cases, THB, THB/case | Empty E-paired or zero summed cases gives unavailable ratio. No unweighted average of weekly ratios |
| Q3 coverage counters | selected = panel weeks in range; reported = selected weeks with `acsc_reported=true`; included = selected eligible reported periods; show paired count if different | counts of weeks/periods, explicitly labelled | Inclusion/exclusion does not remove selected weeks from the displayed timeline |

Display loss in THB million only by dividing THB by 1,000,000 and labelling the axis/card. Use raw totals for calculations; round only for presentation. Compare the calculated weekly ratio with the source value at its reported precision, explaining expected integer rounding. Do not assert a rounding convention or tolerance has been verified: review examples before agreeing that reconciliation rule, and retain unexplained differences for inspection. A rounded total remains approximate even if the arithmetic ratio has many decimal places.

## 5. Functional requirements

| ID | Requirement |
| --- | --- |
| FR-01 | Provide exactly three question-based tabs, using the confirmed stack. Keep per-tab methods, active filters, limitations and quality details accessible inside each tab. |
| FR-02 | Resolve actual inputs and validate required sheets, header offsets, columns and key uniqueness. Surface missing/unreadable/ambiguous input errors for the affected panel; never fabricate replacement data. |
| FR-03 | Q1 fixes Thailand as the highlighted comparator; provides one Freedom year and selectable available ASEAN peers. Show missing requested country-years. Proposed defaults: 2024 and all seven handoff-listed peers (KHM, IDN, MYS, MMR, PHL, SGP, VNM), pending team selection. |
| FR-04 | Q1 provides independent Thai briefing-range and global AI occurrence-year controls; defaults proposed as all available briefing periods and all AI occurrence years/domains. Show categorical highest-loss type names and periods separately from global distinct-ID domain bars, including Unclassified. Freedom controls must not filter context panels. |
| FR-05 | Q2 provides occurrence-year range and domain selection including Unclassified; proposed defaults are full available range/all domains. Display yearly domain lines and a separate aligned total/deepfake chart. Both charts use A(Y,D); the classification strip uses A(Y), with total/classified/unclassified counts and yearly coverage. Label 2026 incomplete and its actual cutoff. |
| FR-06 | Carry forward the provisional normalized keyword rule in section 6. Provide rule/evidence details and reviewable matching/nonmatching examples. Label exploratory counts provisional and withhold any claim of an approved final count until approval and rerun. |
| FR-07 | Q3 provides whole-panel-week range and explicit quality-view controls. Proposed range: week starts 2025-11-09 through 2026-10-25 inclusive, retaining the final unavailable week. Layout decision pending: **A:** dual-axis cases/loss chart plus separate loss/case chart; **B:** three aligned charts. A must label both axes/units; B must share a time axis with three labelled scales. Neither is approved. |
| FR-08 | Q3 detail table/tooltips retain all-type cases/loss, calculated/source ratios, both leading-type names, panel and original reporting dates, precision, flags, source and notes. Do not use type names to relabel totals. Proposed MVP has no type filter on total charts. |
| FR-09 | Apply only the confirmed quality policy when released. Carry forward the specific pending policy in section 6, preserve missing/excluded states and source inspection access, and show included/reported/selected counts. Optional range summaries follow section 4. |
| FR-10 | Reset clears controls and Plotly selections for the current tab only, restoring the agreed tab defaults, including quality view; it does not reset other tabs. Until defaults are approved, describe them as proposed in planning. |
| FR-11 | Attribute each panel to its source and show its active observation period, edition/snapshot, unit and coverage. Retain source URLs as references without fetching external datasets. Q1 Thai context may show flagged source observations descriptively even when Q3 excludes them from comparable totals; disclose this difference. |
| FR-12 | Provide readable labels, distinguishable series, visible filter state, loading, empty and error states, and reproducible startup instructions as specified in section 7. |

## 6. Data and interpretation requirements

**Identity and safe aggregation.** Validate unique country-year, incident ID and panel-week keys; report conflicts rather than silently dropping conflicting records. Count distinct incident IDs after any evidence expansion. Preserve raw missing values and normalize blank domains only for grouping/display. Scores, incidents, posts and police cases are distinct units. No combined risk score, unsupported relationship or causal interpretation is allowed. Recorded counts reflect source coverage, not all real-world events.

**Time.** Use AI `date`/`year` as occurrence time, not `Date Modified`, report publication or snapshot date. Handoff reports AI occurrence coverage through 22 October 2026 in the 26 October export: 2026 is incomplete, and no full-year projection is authorized. Freedom `data_year` and `report_edition` differ; show both. Do not carry 2024 scores forward as 2025/2026 observations. Handoff reports Thai compilation on 1 November 2026; a week with no briefing is not zero cases. Preserve consecutive panel-week slots and gaps; do not interpolate or connect missing/excluded observations as if observed. Partial/irregular reporting periods need explicit labels.

**Proposed deepfake rule, pending approval.** On each of `Implicated Systems`, `title`, `description`, apply Unicode NFKC normalization, map Unicode dashes to a plain hyphen, and search case-insensitively for whole-token pattern `\bdeep[\s-]?fakes?\b`. Any matching field makes an incident a candidate; repeated field/term matches count once per ID. Preserve raw text and matched field, term, excerpt and rule version. Skip missing text; a nonmatch means no keyword match, not proof the incident is not a deepfake. Misinformation is not an equivalent identifier. Do not add deepfake to domain totals or present **526** as an approved/verified final count.

The handoff reports candidate matches for IDs 39 (title/description), 1112 (systems) and 1785 (systems/title), and nonmatching boundary example 728 involving voice cloning/synthetic audio. These are attributed examples, not a new semantic review here. Before approval, review raw descriptions/excerpts for matching and nonmatching examples, including incidental mentions, negation, missing text and voice-cloning boundaries; agree whether broader terms or contextual exclusions are needed. Rerun the approved normalized rule and document resulting membership without claiming unmeasured accuracy.

**ACSC anomaly/overlap proposal, pending confirmation.** The handoff proposes excluding the suspect **16–22 August 2026** and overlapping eight-day **30 May–6 June 2026** from comparable trend/KPI calculations. Keep **12–18 April** and **23–29 August** totals with warnings. Do not automatically exclude every flagged week. Preserve all original observations in a source-detail view; an as-published view may reveal flagged points but must not present overlapping-period sums as deduplicated totals. Do not invent corrected figures, prorate eight days into seven, or silently smooth the suspect value.

The handoff reports that 47/48 raw ACSC starts align exactly with the panel; the exception is raw 30 May versus panel 31 May 2026, both ending 6 June. Validate a documented exception mapping when attaching `acsc_weekly` metadata, preserving both dates and `days`. A silent start-date equality join would lose that record. Do not append `acsc_weekly` totals to `weekly_panel` or multiply them through post-level joins. Interior missing weeks and the final not-yet-reported week stay unavailable as detailed in the handoff. Preserve loss precision; approximate values remain labelled approximate. Published prior-week change fields may use revised comparators and are not required measures for this MVP.

**Type-specific safeguards.** Default Q1/Q3 use names only. The handoff reports highest-type loss/name pairs in 27/48 periods and top-type share/name pairs in 37/48 before exclusions, not complete type series. Any optional highest-type loss must use `acsc_highest_loss_type_loss_baht`, not all-type loss, and needs row-level precision/source review. Any estimated top-type cases would require total cases × stated share/100, verified common denominator/period, share bounds and explicit approximation assumptions. Neither is authorized as an observed type count or default MVP output.

**Attribution.** Use the handoff's provenance: Responsible AI Collaborative for AIID; Freedom House via QoG January 2026 with instructor transformations for scores; compiled ACSC briefing articles/police releases with publisher, article date and source URL for reported cases. State these are reported briefing figures, not a complete police open-data census. Do not infer a licence, scrape reference links or fetch external data.

## 7. Usability and delivery requirements

- Use descriptive titles, readable axes, explicit denominators/units, stable domain colours and distinct Thailand highlighting; do not rely on colour alone. Display Thai type names faithfully even if the eventual UI uses English.
- Make active filters, source periods, approximation, excluded/missing states and Reset effects visible. Empty/no-match is distinct from a load error or zero. A failed source must not silently produce a successful-looking zero result; unaffected panels should remain available where feasible.
- **English is confirmed for the BRD and handoff; dashboard UI language is pending.** Do not treat the document language as an approved UI language.
- Future delivery must include reproducible startup instructions covering environment/dependency versions, required supplied files, configured relative paths/header offsets, startup command, default controls, rule/policy versions and known limitations. This is a future delivery requirement, not an additional document created now.
- No hosting, publication, deployment date, refresh service or numeric performance target is committed. Validate responsiveness with the actual supplied data when implementation is authorized; agree any measurable target separately.

## 8. Acceptance criteria

**All scenarios below are planned acceptance tests. No application tests have been performed or passed by creating this BRD.** Independent expected values must come from separately calculated source aggregations, not copied chart outputs. Deliberate missing/zero cases may use labelled test fixtures, never fabricated production observations.

| AC / linked FR | Given / When / Then |
| --- | --- |
| AC-01 / FR-01, FR-12 | **Given** the MVP, **when** navigation is inspected, **then** exactly Q1–Q3 tabs exist and methods/quality remain accessible inside each; no extra analytical question appears. |
| AC-02 / FR-02 | **Given** supplied files or a missing/wrong-header/ambiguous variant, **when** loading occurs, **then** actual paths/sheets/header offsets are validated and affected errors identify the problem without substitution or assumed CSV paths. |
| AC-03 / FR-03 | **Given** selected same-year country rows, **when** Q1 renders, **then** bars and proposed KPIs match independent score/peer-mean calculations; Thailand is highlighted and points /35, direction, denominator and edition are visible. |
| AC-04 / FR-03 | **Given** a selected unavailable country-year or no valid peers, **when** Q1 calculates, **then** missingness remains visible, no zero score is invented and the peer mean/difference is unavailable where required. |
| AC-05 / FR-04, FR-11 | **Given** three Q1 panels, **when** the Freedom year changes, **then** Thai and AI controls/results remain unchanged; each panel displays its own period/unit, and type names do not label all-type totals. |
| AC-06 / FR-05 | **Given** selected occurrence years, **when** the domain filter changes, **then** displayed distinct counts/chart populations update consistently but classification coverage remains based on A(Y), with independently verified labelled classified/all counts; changing Y recalculates coverage. |
| AC-07 / FR-05, FR-06 | **Given** one incident matching several fields and a domain, **when** subset/domain charts calculate, **then** the ID counts once in the subset and its domain, is never added as an extra domain, and subset counts cannot exceed same-population total counts. |
| AC-08 / FR-06 | **Given** matching/nonmatching examples and unapproved rule status, **when** deepfake detail is inspected, **then** evidence/rule version and provisional status are visible, a nonmatch is not called a confirmed negative, and no approved final count is claimed before review/rerun. |
| AC-09 / FR-05, FR-11 | **Given** occurrence data through October 2026, **when** Q2 shows 2026, **then** it is labelled incomplete with source cutoff/snapshot and no implied full-year projection. |
| AC-10 / FR-07, FR-08 | **Given** eligible Thai periods, **when** weekly measures calculate, **then** cases/loss agree with independent source totals, ratio equals loss/cases using raw inputs, and supplied ratio plus rounding/unexplained difference is retained for reconciliation. |
| AC-11 / FR-07, FR-09 | **Given** missing weeks, absent operands or zero cases, **when** Q3 renders, **then** gaps remain, ratio is unavailable as specified, and no interpolation/zero filling hides missingness. Positive cases with observed zero loss yield zero ratio. |
| AC-12 / FR-08 | **Given** different top-volume and highest-loss names, **when** inspecting a week, **then** both appear under correct descriptive labels and all-type totals remain explicitly all-type, not assigned to either named type. |
| AC-13 / FR-09 | **Given** the eventual confirmed quality policy, **when** comparable/as-published views are inspected, **then** only policy-specified exclusions apply, retained flagged periods keep warnings, excluded source records remain inspectable and included/reported/selected counts reconcile. Under the current proposal, April and 23–29 August are not blanket-excluded. |
| AC-14 / FR-02, FR-08, FR-09 | **Given** the eight-day raw/panel date exception, **when** metadata is attached, **then** no row is lost or multiplied, original and panel dates remain visible, and overlapping periods never become a purported deduplicated range total. |
| AC-15 / FR-09 | **Given** optional range summaries, **when** calculated, **then** independently computed totals share E-paired, ratio is sum(loss)/sum(cases), and coverage/approximation are disclosed; no unweighted average of weekly ratios is used. |
| AC-16 / FR-10 | **Given** changed filters and chart selections in several tabs, **when** one tab's Reset is used, **then** that tab returns to agreed defaults and clears its selections while other tab state remains intact. |
| AC-17 / FR-07, FR-12 | **Given** the team's recorded A/B layout decision, **when** Q3 is accepted, **then** it matches that choice with explicit units/scales; before decision, neither alternative is reported approved. Loading/empty/error states and startup instructions are reviewable. |

## 9. Open decisions and risks

| Decision / risk | Current status and consequence |
| --- | --- |
| Peer set and initial year | Proposed seven available peers and 2024; team confirmation required. Availability must always be checked for the selected year, avoiding an implied complete ASEAN ranking. |
| Deepfake identification | Normalized keyword rule and semantic boundaries pending review; final membership/count and reconciliation examples cannot be accepted as approved yet. This does not block planning domain charts or source loading. |
| ACSC anomaly/overlap policy | Specific two-period exclusion proposal pending confirmation, not blanket flag removal. Policy choice affects comparable totals/coverage and must be visible/versioned. |
| Q3 chart layout | **A:** dual-axis cases/loss plus separate ratio chart; **B:** three aligned charts. Team must choose; dual axes need especially clear unit/scale labels. Both share the same calculation contract. |
| Ratio reconciliation convention | Source rounding method/tolerance is not confirmed. Review source/calculated examples and record the accepted display/reconciliation rule without hiding unexplained differences. |
| UI language and detailed defaults | Pending; documents remain English. Agree defaults and local Reset behavior before interaction acceptance. |
| Optional extensions | `total_score`, range summaries and type-specific numbers are not default commitments. `afnc_false_finance` has no MVP role without a confirmed question. |
| Coverage/interpretation | Different years, curated AI coverage, limited peer coverage, reported-only scams and rounded losses constrain conclusions. Preserve distinct panels and source notes; never imply causation or complete event prevalence. |

Resolve each decision before accepting its affected feature. Unresolved items do not prevent unrelated requirements planning. Implementation, additional documents and deployment are outside this authorized deliverable.
