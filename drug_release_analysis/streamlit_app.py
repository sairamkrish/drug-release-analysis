import streamlit as st
import pandas as pd
from drug_release_analysis.models.drug_absorbance_observation import DrugAbsorbanceObservation
from drug_release_analysis.models.drug_concentration import DrugConcentration
from drug_release_analysis.pages.input.data import input_page_run
from drug_release_analysis.pages.generated_results.concentration import concentration_page_run
from drug_release_analysis.pages.generated_results.observation import observation_page_run

pd.set_option("display.precision", 8)


def render_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    input_page = st.Page(input_page_run, title="Input Data", icon=":material/edit:", default=True)
    concentration_page = st.Page(concentration_page_run, title="Concentration", icon=":material/edit:")
    observation_page = st.Page(observation_page_run, title="Observation", icon=":material/edit:")
    pg = st.navigation(
        {
            "Input": [input_page],
            "Generated Results": [concentration_page, observation_page],
        }
    )
    pg.run()


if __name__ == "__main__":
    render_app()
