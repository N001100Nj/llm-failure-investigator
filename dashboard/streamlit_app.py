"""Streamlit dashboard for LLM failure investigation reports."""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from app.storage.sqlite_store import SQLiteStore
from app.utils.settings import Settings


st.set_page_config(page_title="LLM Failure Investigator", layout="wide")
st.title("Graph Based LLM Failure Investigation System")

store = SQLiteStore(Settings().sqlite_path)
reports = store.list_reports()
metrics = store.metrics()

left, middle, right = st.columns(3)
left.metric("Total incidents", metrics.total_incidents)
middle.metric("Critical rate", f"{metrics.critical_rate:.1%}")
right.metric("High or critical", f"{metrics.high_or_critical_rate:.1%}")

if not reports:
    st.info("No incident reports found. Run `python app/main.py app/sample_traces/hallucination.json` first.")
else:
    frame = pd.DataFrame(reports)
    chart_left, chart_right = st.columns(2)
    chart_left.subheader("Severity distribution")
    chart_left.bar_chart(frame["severity"].value_counts())
    chart_right.subheader("Failure type counts")
    chart_right.bar_chart(frame["failure_type"].value_counts())

    st.subheader("Incident reports")
    selected = st.selectbox("Select report", frame["report_id"].tolist())
    report = next(item for item in reports if item["report_id"] == selected)
    st.dataframe(frame[["created_at", "trace_id", "failure_type", "severity", "root_cause"]], use_container_width=True)
    st.json({**report, "findings_json": json.loads(report["findings_json"])})

