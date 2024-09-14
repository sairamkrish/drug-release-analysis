import streamlit as st
from drug_release_analysis.models.drug_absorbance_observation import (
    DrugAbsorbanceObservation,
)
from drug_release_analysis.models.drug_concentration import DrugConcentration

SAMPLE_OBSERVATION_DATA_URL = "datasets/simple_dataset_1/observation_data.csv"
SAMPLE_CONCENTRATION_DATA_URL = (
    "datasets/simple_dataset_1/concentration_data.csv"
)


def input_page_run():
    st.subheader("Concentration data")
    concentration = handle_concentration()
    if concentration:
        st.session_state.concentration = concentration

    st.subheader("Observation data")
    observation = handle_absorbance_observation()
    if observation:
        observation.transform()
        st.session_state.observation = observation


def handle_concentration():
    upload_msg = (
        "Choose a drug concentration data (csv or csv compressed as zip)"
    )
    sample_file_url = SAMPLE_CONCENTRATION_DATA_URL
    model = DrugConcentration
    uploaded_file = st.file_uploader(upload_msg, type=["csv", "zip"])

    return create_model_from_file_upload(
        uploaded_file,
        model,
        sample_file_url,
        st.session_state.get("concentration"),
    )


# def on_change_handler(field_name: str, field_key: str):
#     st.session_state[field_name] = st.session_state[field_key]


# def on_change_wrapper(field_name: str, ):
#     def on_change():
#         st.session_state[field_name] =


def handle_absorbance_observation():
    upload_msg = (
        "Choose a time based absorbance data (csv or csv compressed as zip)"
    )
    sample_file_url = SAMPLE_OBSERVATION_DATA_URL
    model = DrugAbsorbanceObservation
    uploaded_file = st.file_uploader(upload_msg, type=["csv", "zip"])

    return create_model_from_file_upload(
        uploaded_file,
        model,
        sample_file_url,
        st.session_state.get("observation"),
    )


# @st.cache_data
def create_model_from_file_upload(
    uploaded_file, model, sample_file_url, session_value
):
    file_compression = None
    file_url = sample_file_url
    if uploaded_file is not None:
        file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            file_compression = "zip"
    elif session_value:
        # Use current session value
        return None
    else:
        st.text("No file uploaded yet. Using sample data...")
    model_obj = model(
        file_url=file_url,
        nrows=10000,
        compression=file_compression,
    )
    return model_obj
