import streamlit as st
from drug_release_analysis.models.drug_absorbance_observation import (
    DrugAbsorbanceObservation,
)
from drug_release_analysis.pages.generated_results.concentration import (
    popup_update_concentration_settings,
)


def observation_page_run():
    st.subheader("Observation data")
    add_observation_action_buttons()

    if st.session_state.get("observation"):
        observation: DrugAbsorbanceObservation = st.session_state.observation
        # Show x1 and const values used in below calculation
        # # TODO: Precision is not being displayed correctly. But dataframe has the correct precision.
        st.dataframe(
            observation.transformed_data,
            hide_index=True,
            use_container_width=True,
        )

        col1, _ = st.columns([0.2, 0.8], vertical_alignment="bottom")

        with col1:
            st.plotly_chart(
                observation.cumulative_percentage_trendline_fig,
                use_container_width=True,
            )

    else:
        st.markdown("`No observation data found`")


def add_observation_action_buttons():
    col1, _ = st.columns([0.1, 0.9], vertical_alignment="bottom")
    with col1:
        if st.button(label="Upload observation file", type="primary"):
            popup_upload_observation_file()


@st.dialog("Upload observation file", width="large")
def popup_upload_observation_file():
    upload_msg = (
        "Choose a time based absorbance data (csv or csv compressed as zip)"
    )
    uploaded_file = st.file_uploader(upload_msg, type=["csv", "zip"])

    if uploaded_file is not None:
        concentration_factory(
            uploaded_file,
        )


@st.cache_data
def concentration_factory(uploaded_file):
    file_compression = None
    if uploaded_file is not None:
        file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            file_compression = "zip"
        observation = DrugAbsorbanceObservation(
            file_url=file_url,
            nrows=10000,
            compression=file_compression,
        )
        observation.transform()
        st.session_state.observation = observation
        st.rerun()


def run_observation_transform():
    if st.session_state.get("observation"):
        observation: DrugAbsorbanceObservation = st.session_state.observation
        observation.transform()
        st.session_state.observation = observation


def display_observation_info():
    """
    Used by single page app
    """
    # at the moment, calls the same function as observation_page_run
    observation_page_run()
