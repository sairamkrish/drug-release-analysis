import streamlit as st
from drug_release_analysis.models.drug_concentration import (
    DrugConcentration,
)
from drug_release_analysis.pages.input.data import create_model_from_file_upload


def concentration_page_run():
    st.subheader("Concentration data")
    add_concentration_action_buttons()
    if st.session_state.get("concentration"):
        concentration: DrugConcentration = st.session_state.concentration
        col1, col2, col3, _ = st.columns(
            [0.1, 0.1, 0.2, 0.6], vertical_alignment="bottom"
        )
        with col1:
            st.dataframe(concentration.transformed_data, hide_index=True)
        with col2:
            show_concentration_settings()
        with col3:
            st.plotly_chart(
                concentration.trendline_fig, use_container_width=True
            )
    else:
        st.markdown("`No concentration data found`")


def add_concentration_action_buttons():
    col1, col2, col3, _ = st.columns(
        [0.1, 0.11, 0.1, 0.7], vertical_alignment="bottom"
    )
    with col1:
        if st.button("Upload concentration file"):
            popup_upload_concentration_file()
    with col2:
        if st.button("Update concentration settings"):
            popup_update_concentration_settings()

    with col3:
        if st.button("Show trendline summary"):
            popup_concentration_trendline_summary()


@st.dialog("Concentration trendline summary", width="large")
def popup_concentration_trendline_summary():
    if st.session_state.get("concentration"):
        concentration: DrugConcentration = st.session_state.concentration
        st.text(concentration.trendline_summary)
    else:
        st.markdown(
            "`No concentration data found. Trendlyne summary is based on concentration data`"
        )


def show_concentration_settings():
    settings = {
        "X1": st.session_state.concentration.coef_x1,
        "Const": st.session_state.concentration.coef_const,
        "Actual Load": st.session_state.get("concentration_actual_load"),
        "Theoretical Load": st.session_state.get(
            "concentration_theoretical_load"
        ),
    }
    st.table(settings)


def display_concentration_info():
    """
    Used by single page app
    """
    # at the moment, calls the same function as concentration_page_run
    concentration_page_run()


@st.dialog("Update concentration settings", width="large")
def popup_update_concentration_settings():
    st.number_input(
        "Theoretical load",
        key="theoretical_load",
        value=st.session_state.get("concentration_theoretical_load", 50.0),
        step=0.1,
    )
    st.number_input(
        "Actual load",
        value=st.session_state.get("concentration_actual_load", 50.0),
        key="actual_load",
        step=0.1,
        # on_change=on_change_handler,
        # kwargs={
        #     "field_name": "concentration_actual_load",
        #     "field_key": "actual_load",
        # },
    )
    save_button = st.button("Save", on_click=on_save_concentration_settings)
    if save_button:
        from drug_release_analysis.pages.generated_results.observation import (
            run_observation_transform,
        )

        run_observation_transform()
        st.rerun()


def on_save_concentration_settings():
    st.session_state["concentration_actual_load"] = st.session_state[
        "actual_load"
    ]
    st.session_state["concentration_theoretical_load"] = st.session_state[
        "theoretical_load"
    ]


@st.dialog("Upload concentration file", width="large")
def popup_upload_concentration_file():
    upload_msg = (
        "Choose a drug concentration data (csv or csv compressed as zip)"
    )
    # sample_file_url = SAMPLE_CONCENTRATION_DATA_URL
    uploaded_file = st.file_uploader(upload_msg, type=["csv", "zip"])

    if uploaded_file is not None:
        concentration_factory(
            uploaded_file,
        )


@st.cache_data
def concentration_factory(uploaded_file):
    file_compression = None
    if uploaded_file is not None:
        file_url = uploaded_file
        if uploaded_file.type == "application/zip":
            file_compression = "zip"
        model_obj = DrugConcentration(
            file_url=file_url,
            nrows=10000,
            compression=file_compression,
        )
        st.session_state.concentration = model_obj
        st.rerun()
    # elif st.session_state.get("concentration"):
    #     # Use current session value
    #     # This can happen when user closes the file upload dialog
    #     # without selecting a file
    #     return None
