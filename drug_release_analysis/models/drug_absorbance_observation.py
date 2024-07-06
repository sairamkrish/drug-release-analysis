from decimal import Decimal
from numpy import double
import pandas as pd
from drug_release_analysis.models.drug_concentration import DrugConcentration
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions
from pandas import DataFrame


class DrugAbsorbanceObservation:
    original_data: DataFrame
    transformed_data: DataFrame
    concentration: DrugConcentration

    def __init__(self, file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None) -> None:
        self.original_data = pd.read_csv(file_url, nrows=nrows, compression=compression)

    def set_concentration(self, concentration: DrugConcentration):
        self.concentration = concentration

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

    def get_metrix(self):
        return self.transformed_data

    def calculate_x_ug_per_ml(self, data):
        data["x_ug_per_ml"] = (
            (data["absorbance"].astype(double) - self.concentration.coef_const) / self.concentration.coef_x1
        ).astype(double)
