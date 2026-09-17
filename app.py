import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Women Ethnic Search Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

st.title("👗 Women Ethnic Search Dashboard")

try:
    df = load_data()

    # Numeric conversions
    df['Total_Searches'] = pd.to_numeric(df['Total_Searches'], errors='coerce')
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
    df['PPVS'] = pd.to_numeric(df['PPVS'], errors='coerce')
    df['Successful_Search_Sessions'] = pd.to_numeric(df['Successful_Search_Sessions'], errors='coerce')
    df['CTR_num'] = df['CTR'].astype(str).str.rstrip('%').astype(float)
    df['CVR_num'] = df['CVR'].astype(str).str.rstrip('%').astype(float)

    # Sidebar Filter Controls
    st.sidebar.header("Filters")
    selected_dates = st.sidebar.multiselect("Select Date", options=df["Date"].unique(), default=df["Date"].unique())
    selected_verts = st.sidebar.multiselect("Select Vertical", options=df["Vertical"].unique(), default=df["Vertical"].unique())

    # Apply Selected Filters
    filtered_df = df[df["Date"].isin(selected_dates) & df["Vertical"].isin(selected_verts)]

    # Top Metric Scorecards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Searches", f"{filtered_df['Total_Searches'].sum():,.0f}")
    c2.metric("Total Units Sold", f"{filtered_df['Units'].sum():,.0f}")
    c3.metric("Product Views (PPVS)", f"{filtered_df['PPVS'].sum():,.0f}")
    c4.metric("Successful Sessions", f"{filtered_df['Successful_Search_Sessions'].sum():,.0f}")

    st.divider()

    # Visual Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Searches by Vertical")
        fig_bar = px.bar(
            filtered_df, 
            x="Vertical", 
            y="Total_Searches", 
            color="Vertical",
            title="Search Volume per Category"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Conversion Efficiency (Searches vs CVR %)")
        fig_scatter = px.scatter(
            filtered_df, 
            x="Total_Searches", 
            y="CVR_num",
            size="Units",
            color="Vertical",
            hover_name="Vertical_x_StoreID",
            title="Search Volume vs Conversion Rate (%)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Table View
    st.subheader("Data Overview")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
