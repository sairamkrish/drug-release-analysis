import streamlit as st
import pandas as pd
from drug_release_analysis.models.drug_absorbance_observation import DrugAbsorbanceObservation
from drug_release_analysis.models.drug_concentration import DrugConcentration

pd.set_option("display.precision", 8)

SAMPLE_OBSERVATION_DATA_URL = "datasets/simple_dataset_1/observation_data.csv"
SAMPLE_CONCENTRATION_DATA_URL = "datasets/simple_dataset_1/concentration_data.csv"


def render_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    concentration = handle_concentration()
    st.subheader("Concentration data with computation")
    st.dataframe(concentration.get_metrix(), hide_index=True)

    observation = handle_absorbance_observation()
    st.subheader("Observation data with computation")

    # TODO: Precision is not being displayed correctly. But dataframe has the correct precision.
    # st.dataframe(data, hide_index=True, width=1000, height=500)
    st.dataframe(observation.get_metrix(), hide_index=True)


def handle_concentration():
    upload_msg = "Choose a drug concentration data (csv or csv compressed as zip)"
    sample_file_url = SAMPLE_CONCENTRATION_DATA_URL
    model = DrugConcentration

    return create_model_from_file_upload(upload_msg, model, sample_file_url)


def handle_absorbance_observation():
    upload_msg = "Choose a time based absorbance data (csv or csv compressed as zip)"
    sample_file_url = SAMPLE_OBSERVATION_DATA_URL
    model = DrugAbsorbanceObservation

    return create_model_from_file_upload(upload_msg, model, sample_file_url)


def create_model_from_file_upload(upload_msg, model, sample_file_url):
    file_compression = None
    file_url = sample_file_url
    uploaded_file = st.file_uploader(upload_msg, type=["csv", "zip"])
    if uploaded_file is not None:
        file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            file_compression = "zip"
    else:
        st.text("No file uploaded yet. Using sample data...")
    data_load_state = st.text("Loading data...")
    observation = model(
        file_url=file_url,
        nrows=10000,
        compression=file_compression,
    )
    data_load_state.text("Data loaded!")
    return observation


if __name__ == "__main__":
    render_app()
