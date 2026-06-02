"""
Basic web UI (Streamlit) — primary input surface for user preferences.

Run from project root:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from src.app import execute_pipeline
from src.config import setup_logging
from src.input.phase2 import DEFAULT_FORM_VALUES, InputValidationError, build_user_preferences
from src.models.preferences import VALID_BUDGETS
from src.presentation.form_options import (
    BANGALORE_LOCATIONS,
    CRAVING_OPTIONS,
    CUISINE_OPTIONS,
    STREAMLIT_DEFAULT_CUISINE,
    STREAMLIT_DEFAULT_LOCATION,
    normalize_cuisine,
    normalize_extras,
)
from src.presentation.phase5 import build_phase5_view_model

setup_logging()


def _option_index(options: tuple[str, ...], value: str, *, fallback: int = 0) -> int:
    try:
        return options.index(value)
    except ValueError:
        return fallback


def _inject_ui_styles() -> None:
    """Apply lightweight visual polish for Streamlit Cloud."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        .app-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: #fff1f2;
            color: #be123c;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.65rem;
        }

        .app-subtitle {
            color: #475569;
            margin-bottom: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Zomato AI Recommendations",
    page_icon="🍽️",
    layout="centered",
)

_inject_ui_styles()
st.markdown('<span class="app-badge">DineAI • Streamlit</span>', unsafe_allow_html=True)
st.title("Restaurant Recommendations")
st.markdown(
    '<p class="app-subtitle">Bangalore-first search with cleaner preferences and card-style results.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Options")
    use_mock_data = st.checkbox(
        "Use mock dataset",
        value=True,
        help="Recommended on Streamlit Cloud (no large CSV). Uses in-memory sample data.",
    )
    st.caption("No advanced tuning controls in Streamlit UI.")

with st.form("preferences_form", clear_on_submit=False):
    st.subheader("Your preferences")

    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox(
            "Location *",
            options=list(BANGALORE_LOCATIONS),
            index=_option_index(BANGALORE_LOCATIONS, STREAMLIT_DEFAULT_LOCATION),
        )
        cuisine = st.selectbox(
            "Preferred cuisine *",
            options=list(CUISINE_OPTIONS),
            index=_option_index(CUISINE_OPTIONS, STREAMLIT_DEFAULT_CUISINE),
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

    extras = st.selectbox(
        "Specific cravings (optional)",
        options=list(CRAVING_OPTIONS),
        index=0,
    )

    submitted = st.form_submit_button("Get recommendations", type="primary")

if submitted:
    try:
        preferences = build_user_preferences(
            location=location,
            budget=budget,
            cuisine=normalize_cuisine(cuisine),
            min_rating=min_rating,
            extras=normalize_extras(extras),
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

    # No frontend result cap: render all recommendations returned by backend.
    vm = build_phase5_view_model(result, top_k=max(len(result.recommendations), 1))
    if vm.summary:
        st.info(vm.summary)

    if vm.empty_message:
        st.warning(
            "No restaurants matched your filters. "
            "Try a different location, cuisine, or lower the minimum rating."
        )
    else:
        st.success(f"Found {len(result.recommendations)} recommendation(s)")
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
        "Choose your **location** and **cuisine** from the dropdowns, then click "
        "**Get recommendations** to run the pipeline."
    )
