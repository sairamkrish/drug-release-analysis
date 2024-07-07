import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objs as go
from statsmodels.iolib.summary import Summary
from pandas.util import hash_pandas_object
import hashlib


class DrugConcentration:
    original_data: DataFrame
    transformed_data: DataFrame
    coef_const: float
    coef_x1: float
    trendline_fig: go.Figure
    trendline_summary: Summary

    def __init__(self, file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None) -> None:
        self.original_data = pd.read_csv(file_url, nrows=nrows, compression=compression)
        self.transform()
        self.init_trendline()

    def transform(self):
        data = self.original_data.rename(lowercase, axis="columns")
        self.transformed_data = data

    def init_trendline(self):
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
        self.trendline_fig = fig
        self.trendline_summary = summary

    # def __key(self):
    #     hash_array_value = hash_pandas_object(self.original_data, index=True).values
    #     return int(hashlib.sha256(hash_array_value).hexdigest(), 16)
    #     # return hash_pandas_object(self.original_data)

    # def __hash__(self):
    #     return self.__key()

    # def __eq__(self, other):
    #     if isinstance(other, DrugConcentration):
    #         return self.__key() == other.__key()
    #     return NotImplemented
