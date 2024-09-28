import streamlit as st
import pandas as pd
from drug_release_analysis.models.drug_absorbance_observation import (
    DrugAbsorbanceObservation,
)
from drug_release_analysis.models.drug_concentration import DrugConcentration
from drug_release_analysis.pages.input.data import input_page_run
from drug_release_analysis.pages.generated_results.concentration import (
    concentration_page_run,
    display_concentration_info,
)
from drug_release_analysis.pages.generated_results.observation import (
    display_observation_info,
    observation_page_run,
)

pd.set_option("display.precision", 8)


def app_settings():
    st.session_state["concentration_actual_load"] = st.session_state.get(
        "concentration_actual_load", 50.0
    )
    st.session_state["concentration_theoretical_load"] = st.session_state.get(
        "concentration_theoretical_load", 50.0
    )


def render_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    input_page = st.Page(
        input_page_run, title="Input Data", icon=":material/edit:", default=True
    )
    concentration_page = st.Page(
        concentration_page_run, title="Concentration", icon=":material/edit:"
    )
    observation_page = st.Page(
        observation_page_run, title="Observation", icon=":material/edit:"
    )
    pg = st.navigation(
        {
            "Input": [input_page],
            "Generated Results": [concentration_page, observation_page],
        }
    )
    pg.run()


def render_single_page_app():
    st.set_page_config(layout="wide")
    st.title("Drug Release Analysis App")
    # show_dev_tools()
    display_concentration_info()
    display_observation_info()
    # version_number = "v0.1.0"
    # st.markdown(
    #     f'<div style="position: fixed; top: 0; left: 0;">{version_number}</div>',
    #     unsafe_allow_html=True,
    # )


def show_dev_tools():
    st.markdown("*Dev tools*")
    st.markdown("session_state object")
    st.table(st.session_state)


if __name__ == "__main__":
    # render_app()
    render_single_page_app()
