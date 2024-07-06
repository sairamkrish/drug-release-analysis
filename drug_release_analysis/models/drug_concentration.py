from decimal import Decimal
from numpy import double
import streamlit as st
import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

from pandas._typing import ReadCsvBuffer, CompressionOptions
from pandas import DataFrame


class DrugConcentration:
    original_data: DataFrame
    transformed_data: DataFrame

    def __init__(self, file_url: ReadCsvBuffer | str, nrows=1000, compression: CompressionOptions = None) -> None:
        self.original_data = pd.read_csv(file_url, nrows=nrows, compression=compression)
        self.transform()

    def transform(self):
        data = self.original_data.rename(lowercase, axis="columns")
        self.transformed_data = data

    def get_metrix(self):
        return self.transformed_data
