from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")

TABS = ["Q1 · ไทยเทียบอาเซียน", "Q2 · เหตุการณ์ AI", "Q3 · คดีหลอกลวงที่รายงาน"]


def run(tab, **state):
    at = AppTest.from_file(APP, default_timeout=120)
    at.session_state["active_tab"] = tab
    for k, v in state.items():
        at.session_state[k] = v
    return at.run()


def test_all_tabs_render_without_exception():
    for t in TABS:
        at = run(t)
        assert not at.exception, (t, at.exception)
        assert not at.error


def test_reset_is_tab_local():
    at = run(TABS[2], q3_view="as_published", q1_year=2020)
    at.button(key="reset_q3").click().run()
    assert at.session_state["q3_view"] == "comparable" and at.session_state["q1_year"] == 2020


def test_layout_b_and_empty_filters():
    assert not run(TABS[2], q3_layout="B").exception
    assert not run(TABS[1], q2_domains=[]).exception
    assert not run(TABS[0], q1_peers=[]).exception
    assert not run(TABS[2], q3_range=(pd.Timestamp("2026-06-07"), pd.Timestamp("2026-06-14"))).exception


def test_thai_ui_and_missing_file_error_visible(tmp_path, monkeypatch):
    at = run(TABS[0])
    texts = " ".join(m.value for m in at.markdown) + " ".join(h.value for h in at.header)
    assert "ภาษาของหน้าจอ: ภาษาไทย" in texts and "team decision pending" not in texts
    assert "English" not in texts  # the English-language pending notice was replaced
    # a missing source must surface a visible Thai error, not a zero result
    monkeypatch.setenv("DATAVIZ_DATA_DIR", str(tmp_path))
    monkeypatch.setattr("dashboard.data.ROOT", tmp_path)
    from dashboard import data
    import pytest
    with pytest.raises(data.DataError, match="ไม่พบไฟล์ที่จำเป็น"):
        data.load_freedom()
