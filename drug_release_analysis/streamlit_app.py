import streamlit as st
import pandas as pd
from drug_release_analysis.utils.string_helpers import lowercase

# DATE_COLUMN = "date/time"
TIME_BASED_ABSORBANCE_DATA_URL = (
    "datasets/simple_dataset_1/time_based_absorbance_data.csv"
)


@st.cache_data
def load_time_based_absorbance_data(nrows):
    data = pd.read_csv(TIME_BASED_ABSORBANCE_DATA_URL, nrows=nrows)

    data.rename(lowercase, axis="columns", inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# st.subheader("Number of pickups by hour")
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider("hour", 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader("Map of all pickups at %s:00" % hour_to_filter)
# st.map(filtered_data)


def render_app():
    st.title("Drug Release Analysis App")

    st.write("This is a Streamlit app for drug release analysis.")
    st.write("The app is currently under development.")

    data_load_state = st.text("Loading data...")
    data = load_time_based_absorbance_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    st.subheader("Time based absorbance data")
    st.write(data)


if __name__ == "__main__":
    render_app()
