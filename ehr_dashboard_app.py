
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("aha__3_.csv")
        return df
    except Exception as e:
        st.error("Failed to load 'aha__3_.csv'. Ensure the file is available in your working directory.")
        return pd.DataFrame()

df = load_data()

st.title("📊 EHR Adoption: Advanced Dashboard (AHA Dataset)")

if df.empty:
    st.warning("No data loaded.")
else:
    st.markdown("This dashboard provides insights into EHR adoption across U.S. regions using the AHA dataset.")

    # Filters (Optional)
    region_col = "region_code"
    year_col = "year" if "year" in df.columns else None

    st.sidebar.header("Filter Data")
    if year_col:
        selected_year = st.sidebar.selectbox("Select Year", sorted(df[year_col].dropna().unique()))
        df = df[df[year_col] == selected_year]

    # Overview
    st.subheader("Sample Data")
    st.dataframe(df.head(10))

    # 1. Correlation Heatmap
    st.markdown("### 🔥 Correlation Heatmap")
    cols_to_include = ["pct_hospital_cehrt", "pct_hospitals_cehrt_2015"]
    corr_data = df[cols_to_include].dropna()
    if not corr_data.empty:
        corr = corr_data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation between CEHRT Metrics")
        st.pyplot(fig)
    else:
        st.info("Insufficient data for correlation heatmap.")

    # 2. Choropleth Map by State
    st.markdown("### 🗺️ CEHRT Adoption by Region (State-Level Choropleth)")
    if "region_code" in df.columns and "pct_hospital_cehrt" in df.columns:
        map_df = df.groupby("region_code")["pct_hospital_cehrt"].mean().reset_index()
        map_df["region_code"] = map_df["region_code"].str.upper()

        fig = px.choropleth(
            map_df,
            locations="region_code",
            locationmode="USA-states",
            color="pct_hospital_cehrt",
            scope="usa",
            color_continuous_scale="Plasma",
            labels={"pct_hospital_cehrt": "% CEHRT Adoption"}
        )
        st.plotly_chart(fig)
    else:
        st.info("Required columns not available for choropleth map.")
