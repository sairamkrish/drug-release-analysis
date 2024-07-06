from typing import Tuple
import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions
from pandas import DataFrame
import plotly.express as px


class DrugConcentration:
    original_data: DataFrame
    transformed_data: DataFrame
    coef_const: float
    coef_x1: float

    def __init__(self, file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None) -> None:
        self.original_data = pd.read_csv(file_url, nrows=nrows, compression=compression)
        self.transform()

    def transform(self):
        data = self.original_data.rename(lowercase, axis="columns")
        self.transformed_data = data

    def get_trendline(self):
        fig = px.scatter(
            self.transformed_data,
            x="drug_concentration",
            y="absorbance",
            trendline="ols",
        )
        results = px.get_trendline_results(fig)
        regression_results = results.px_fit_results.iloc[0]
        self.coef_const, self.coef_x1 = regression_results.params
        summary = regression_results.summary()
        return (fig, summary)

    def get_metrix(self):
        return self.transformed_data
