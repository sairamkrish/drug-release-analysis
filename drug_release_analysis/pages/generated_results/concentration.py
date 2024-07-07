import streamlit as st
from drug_release_analysis.models.drug_concentration import DrugConcentration


def concentration_page_run():
    st.subheader("Concentration data")
    concentration: DrugConcentration = st.session_state.concentration
    col1, col2, col3 = st.columns([0.2, 0.3, 0.5])
    with col1:
        st.dataframe(concentration.transformed_data, hide_index=True)
    with col2:
        st.plotly_chart(concentration.trendline_fig, use_container_width=True)
    with col3:
        st.text(concentration.trendline_summary)
