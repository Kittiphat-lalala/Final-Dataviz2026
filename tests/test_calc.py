import numpy as np
import pandas as pd
import pytest

from dashboard import calc, config as C, data, deepfake


@pytest.fixture(scope="module")
def thai(): return data.load_thai()
@pytest.fixture(scope="module")
def aiid(): return data.load_aiid()
@pytest.fixture(scope="module")
def freedom(): return data.load_freedom()


def test_loss_per_case_rules():
    r = calc.loss_per_case([100, 0, 50, None, 10], [4, 5, 0, 5, None])
    assert r[0] == 25 and r[1] == 0 and np.isnan(r[2]) and np.isnan(r[3]) and np.isnan(r[4])


def test_thai_attach_is_one_to_one(thai):
    assert len(thai) == 409 and thai["orig_start"].notna().sum() == 48
    row = thai[thai.week_start == "2026-05-31"].iloc[0]
    assert row["orig_start"] == pd.Timestamp("2026-05-30") and row["days"] == 8


def test_comparable_policy_counts(thai):
    w = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "comparable")
    cc = calc.coverage_counts(w)
    assert cc == {"selected": 51, "reported": 48, "included": 46, "paired": 46}
    wp = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "as_published")
    assert calc.coverage_counts(wp)["included"] == 48
    assert w[w.week_start == "2026-10-25"]["eligible"].item() is False  # final week stays unavailable


def test_range_summary_weighted_ratio(thai):
    w = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "comparable")
    s = calc.range_summary(w)
    p = w[w.eligible]
    assert s["ratio"] == pytest.approx(p.acsc_loss_baht.sum() / p.acsc_cases.sum())
    assert s["ratio"] != pytest.approx((p.acsc_loss_baht / p.acsc_cases).mean())


def test_kpi_latest_and_delta(thai):
    w = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "comparable")
    k = calc.latest_kpi(w)
    assert k["week"]["week_start"] == pd.Timestamp("2026-10-18")
    assert k["newer"]["week_start"] == pd.Timestamp("2026-10-25")
    assert k["delta"]["prev_start"] == pd.Timestamp("2026-10-11")
    w2 = calc.prepare_weeks(thai, pd.Timestamp("2026-06-07"), pd.Timestamp("2026-06-21"), "comparable")
    assert calc.latest_kpi(w2)["week"]["week_start"] == pd.Timestamp("2026-06-21")
    assert calc.latest_kpi(w2)["delta"] is None  # 14 Jun predecessor is a missing week -> no skip-back


def test_peak_excludes_suspect_in_comparable(thai):
    w = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "comparable")
    assert calc.peak_loss(w)["week_start"].iloc[0] != pd.Timestamp("2026-08-16")
    wp = calc.prepare_weeks(thai, C.Q3_DEFAULT_START, C.Q3_DEFAULT_END, "as_published")
    assert calc.peak_loss(wp)["week_start"].iloc[0] == pd.Timestamp("2026-08-16")


def test_q1_peer_mean_and_missing(freedom):
    r = calc.q1_scores(freedom, 2024, C.ASEAN_PEERS)
    peers = r["rows"][r["rows"].iso3 != "THA"]["limits_on_content"]
    assert r["n_available"] == 7 and r["peer_mean"] == pytest.approx(peers.mean())
    assert r["difference"] == pytest.approx(r["thailand"] - r["peer_mean"])
    r2 = calc.q1_scores(freedom, 2010, C.ASEAN_PEERS)  # KHM, PHL, SGP absent in 2010
    assert {"KHM", "PHL", "SGP"} <= set(r2["unavailable"]) and r2["n_available"] == 4
    r3 = calc.q1_scores(freedom, 2024, [])
    assert np.isnan(r3["peer_mean"]) and np.isnan(r3["difference"])


def test_aiid_counts(aiid):
    assert len(aiid) == 1775 and aiid["Incident ID"].is_unique
    a = calc.incidents_in_years(aiid, 1983, 2026)
    c = calc.coverage(a)
    assert (c["all"], c["classified"], c["unclassified"]) == (1775, 1496, 279)
    assert calc.domain_counts(a)["incidents"].sum() == 1775
    # domain filter does not change coverage base
    sel = a[a.domain == "Misinformation"]
    assert calc.coverage(a)["all"] == 1775 and len(sel) == 196


def test_deepfake_rule_examples_and_containment(aiid):
    ev = deepfake.find_matches(aiid)
    ids = deepfake.candidate_ids(ev)
    assert {39, 1112, 1785} <= ids and 728 not in ids
    assert set(ev[ev["Incident ID"] == 1112]["field"]) == {"Implicated Systems"}
    t = calc.yearly_totals(aiid, ids)
    assert (t.candidate_deepfake <= t.total).all()
    assert deepfake.normalize("Deep‑fake") == "Deep-fake"
    assert deepfake.PATTERN.search("a deep fake b") and not deepfake.PATTERN.search("deepfaker")


def test_missing_input_error(tmp_path):
    with pytest.raises(data.DataError):
        data.find_input("freedom", [tmp_path])


def test_ambiguous_input_error(tmp_path):
    (tmp_path / "freedom_on_the_net_scores.csv").write_text("a")
    (tmp_path / "freedom_on_the_net_scores (1).csv").write_text("b")
    with pytest.raises(data.DataError, match="Ambiguous"):
        data.find_input("freedom", [tmp_path])
