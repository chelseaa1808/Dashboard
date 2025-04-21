
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/chelseaa1808/EHR-Adoption-DataSet-Analysis/main/aha__3_.csv"
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error("Failed to load data. Make sure the file is available at the provided GitHub URL.")
        return pd.DataFrame()

df = load_data()

st.title("📊 EHR Adoption Analysis Dashboard")

if df.empty:
    st.warning("Data not available.")
else:
    # Sidebar filters
    st.sidebar.header("Filter Data")
    year_col = [col for col in df.columns if "year" in col.lower()]
    state_col = [col for col in df.columns if "state" in col.lower()]

    selected_year = st.sidebar.selectbox("Year", df[year_col[0]].dropna().unique()) if year_col else None
    selected_state = st.sidebar.selectbox("State", df[state_col[0]].dropna().unique()) if state_col else None

    # Filtered data
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df[year_col[0]] == selected_year]
    if selected_state:
        filtered_df = filtered_df[filtered_df[state_col[0]] == selected_state]

    st.subheader("EHR Metrics Overview")
    st.dataframe(filtered_df.head(10))

    # Sample visualization
    metric_cols = [col for col in filtered_df.columns if filtered_df[col].dtype in ['int64', 'float64']]
    if metric_cols:
        metric = st.selectbox("Select a metric to visualize", metric_cols)
        fig, ax = plt.subplots()
        filtered_df[metric].hist(bins=20, ax=ax)
        ax.set_title(f"Distribution of {metric}")
        st.pyplot(fig)
