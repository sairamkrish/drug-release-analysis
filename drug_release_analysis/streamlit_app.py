from decimal import Decimal
from numpy import double
import streamlit as st
import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions

pd.set_option("display.precision", 8)

SAMPLE_TIME_BASED_ABSORBANCE_DATA_URL = "datasets/simple_dataset_1/time_based_absorbance_data.csv"


@st.cache_data
def load_time_based_absorbance_data(file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None):
    data = pd.read_csv(file_url, nrows=nrows, compression=compression)  # , compression="zip"

    data.rename(lowercase, axis="columns", inplace=True)
    calculate_x_ug_per_ml(data)
    data["drug_release_ug_per_ml"] = data["x_ug_per_ml"] * data["dilution_factor"]
    data["x100_ml_media"] = data["drug_release_ug_per_ml"] * 100
    data["per_pull_x5_ml"] = data["drug_release_ug_per_ml"] * 5
    data["total_drug_release"] = Decimal(0)
    data.at[0, "total_drug_release"] = data.at[0, "x100_ml_media"]
    for i in range(1, len(data)):
        data.at[i, "total_drug_release"] = (
            data.at[i, "x100_ml_media"] + data.at[i - 1, "per_pull_x5_ml"] - data.at[i - 1, "total_drug_release"]
        )

    data["cumulative_drug_release"] = data["total_drug_release"].cumsum()
    return data


def calculate_x_ug_per_ml(data):
    data["x_ug_per_ml"] = ((data["absorbance"].astype(double) - 0.0015) / 0.0367).astype(double)


def render_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    time_based_absorbance_data_file_url = SAMPLE_TIME_BASED_ABSORBANCE_DATA_URL
    time_based_absorbance_data_file_compression = None
    uploaded_file = st.file_uploader(
        "Choose a time based absorbance data file (csv or csv compressed as zip)", type=["csv", "zip"]
    )
    if uploaded_file is not None:
        time_based_absorbance_data_file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            time_based_absorbance_data_file_compression = "zip"
    else:
        st.text("No file uploaded yet. Showing sample data")
    data_load_state = st.text("Loading data...")
    data = load_time_based_absorbance_data(
        file_url=time_based_absorbance_data_file_url,
        nrows=10000,
        compression=time_based_absorbance_data_file_compression,
    )
    data_load_state.text("Data loaded!")

    st.subheader("Time based absorbance data")

    # TODO: Precision is not being displayed correctly. But dataframe has the correct precision.
    # st.dataframe(data, hide_index=True, width=1000, height=500)
    st.dataframe(data, hide_index=True)


if __name__ == "__main__":
    render_app()
