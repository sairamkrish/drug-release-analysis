from decimal import Decimal
from numpy import double
import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions
from pandas import DataFrame
from pandas.util import hash_pandas_object
import streamlit as st


class DrugAbsorbanceObservation:
    original_data: DataFrame
    transformed_data: DataFrame

    def __init__(self, file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None) -> None:
        self.original_data = pd.read_csv(file_url, nrows=nrows, compression=compression)

    def transform(self):
        data = self.original_data.rename(lowercase, axis="columns")
        data = data.groupby(["group_name", "time_in_hours", "dilution_factor"])[["absorbance"]].mean().reset_index()
        data.sort_values(by=["group_name", "time_in_hours"], inplace=True)
        self.calculate_x_ug_per_ml(data)
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
        self.transformed_data = data

    def calculate_x_ug_per_ml(self, data):
        concentration = st.session_state.concentration
        data["x_ug_per_ml"] = (
            (data["absorbance"].astype(double) - concentration.coef_const) / concentration.coef_x1
        ).astype(double)

    # def __key(self):
    #     return hash_pandas_object(self.original_data)

    # def __hash__(self):
    #     return self.__key()

    # def __eq__(self, other):
    #     if isinstance(other, DrugAbsorbanceObservation):
    #         return self.__key() == other.__key()
    #     return NotImplemented
