import streamlit as st
from drug_release_analysis.models.drug_absorbance_observation import DrugAbsorbanceObservation


def observation_page_run():
    st.subheader("Observation data")
    observation: DrugAbsorbanceObservation = st.session_state.observation
    # # TODO: Precision is not being displayed correctly. But dataframe has the correct precision.
    st.dataframe(observation.transformed_data, hide_index=True, use_container_width=True)
