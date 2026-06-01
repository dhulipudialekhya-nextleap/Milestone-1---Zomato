"""
Basic web UI (Streamlit) — primary input surface for user preferences.

Run from project root:
    streamlit run src/presentation/web_ui.py
"""

from __future__ import annotations

import streamlit as st

from src.app import execute_pipeline
from src.config import setup_logging
from src.input.phase2 import DEFAULT_FORM_VALUES, InputValidationError, build_user_preferences
from src.presentation.phase5 import build_phase5_view_model
from src.models.preferences import VALID_BUDGETS

setup_logging()

st.set_page_config(
    page_title="Zomato AI Recommendations",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️ Restaurant Recommendations")
st.caption("AI-powered suggestions inspired by Zomato — Phase 1 ingestion enabled")

with st.sidebar:
    st.header("Options")
    use_mock_data = st.checkbox(
        "Use mock dataset",
        value=False,
        help="Use in-memory sample data instead of processed/ingested data.",
    )
    st.divider()
    st.markdown("**Dev / testing**")
    st.code("python -m src --mock-data", language="bash")

with st.form("preferences_form", clear_on_submit=False):
    st.subheader("Your preferences")

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input(
            "Location *",
            value=DEFAULT_FORM_VALUES.location,
            placeholder="e.g. Delhi, Bangalore",
        )
        cuisine = st.text_input(
            "Preferred cuisine *",
            value=DEFAULT_FORM_VALUES.cuisine,
            placeholder="e.g. Italian, Chinese",
        )
    with col2:
        budget = st.selectbox(
            "Budget *",
            options=list(VALID_BUDGETS),
            index=list(VALID_BUDGETS).index(DEFAULT_FORM_VALUES.budget),
        )
        min_rating = st.slider(
            "Minimum rating",
            min_value=0.0,
            max_value=5.0,
            value=DEFAULT_FORM_VALUES.min_rating,
            step=0.5,
        )

    extras = st.text_area(
        "Additional preferences (optional)",
        placeholder="e.g. family-friendly, quick service",
        value=DEFAULT_FORM_VALUES.extras,
        height=80,
    )

    submitted = st.form_submit_button("Get recommendations", type="primary")

if submitted:
    try:
        preferences = build_user_preferences(
            location=location,
            budget=budget,
            cuisine=cuisine,
            min_rating=min_rating,
            extras=extras or None,
        )
    except InputValidationError as exc:
        st.error(f"Invalid input: {exc}")
        st.stop()

    with st.spinner("Finding restaurants for you…"):
        try:
            result = execute_pipeline(preferences, use_mock_data=use_mock_data)
        except Exception as exc:  # noqa: BLE001 — show user-friendly message in UI
            st.error(f"Something went wrong: {exc}")
            st.stop()

    if result.used_llm_fallback:
        st.warning("AI unavailable — showing filter-based results.")

    vm = build_phase5_view_model(result, top_k=5)
    if vm.summary:
        st.info(vm.summary)

    if vm.empty_message:
        st.warning(
            "No restaurants matched your filters. "
            "Try a different location, cuisine, or lower the minimum rating."
        )
    else:
        st.success(
            f"Found {len(result.recommendations)} recommendation(s) "
            f"(showing top {len(vm.items)})"
        )
        for item in vm.items:
            with st.container(border=True):
                st.markdown(f"### #{item.rank} {item.name}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Rating", item.rating_text)
                c2.write(f"**Cuisine:** {item.cuisines_text}")
                c3.write(f"**Est. cost:** {item.estimated_cost_text}")
                st.markdown(f"**Why this pick:** {item.explanation}")

else:
    st.markdown(
        "Fill in your preferences and click **Get recommendations** to run the pipeline."
    )
