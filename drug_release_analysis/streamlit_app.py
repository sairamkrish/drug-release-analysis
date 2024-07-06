import streamlit as st
import pandas as pd
from drug_release_analysis.models.drug_absorbance_observation import DrugAbsorbanceObservation

pd.set_option("display.precision", 8)

SAMPLE_ABSORBANCE_OBSERVATION_DATA_URL = "datasets/simple_dataset_1/time_based_absorbance_data.csv"


def render_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    observation = handle_absorbance_observation()
    st.subheader("Time based absorbance data")

    # TODO: Precision is not being displayed correctly. But dataframe has the correct precision.
    # st.dataframe(data, hide_index=True, width=1000, height=500)
    st.dataframe(observation.get_metrix(), hide_index=True)


def handle_absorbance_observation():
    absorbance_observation_data_file_url = SAMPLE_ABSORBANCE_OBSERVATION_DATA_URL
    absorbance_observation_data_file_compression = None
    uploaded_file = st.file_uploader(
        "Choose a time based absorbance data file (csv or csv compressed as zip)", type=["csv", "zip"]
    )
    if uploaded_file is not None:
        absorbance_observation_data_file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            absorbance_observation_data_file_compression = "zip"
    else:
        st.text("No file uploaded yet. Showing sample data")
    data_load_state = st.text("Loading data...")
    observation = DrugAbsorbanceObservation(
        file_url=absorbance_observation_data_file_url,
        nrows=10000,
        compression=absorbance_observation_data_file_compression,
    )
    data_load_state.text("Data loaded!")
    return observation


if __name__ == "__main__":
    render_app()
