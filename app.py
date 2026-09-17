import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Women Ethnic Search Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def clean_numeric_dataframe(df):
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.contains('%').any():
            df[f"{col}_num"] = df[col].astype(str).str.rstrip('%').replace(['-', 'nan', ''], '0').astype(float)
        elif df[col].dtype == 'object':
            cleaned_series = df[col].astype(str).str.replace(',', '').str.replace('$', '')
            numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
            if not numeric_series.isna().all():
                df[col] = numeric_series.fillna(0)
    return df

@st.cache_data(ttl=120)
def load_all_tabs():
    df = pd.read_csv("data.csv")
    df = clean_numeric_dataframe(df)

    df_sc = df[df['Category_Level'] == 'SC Level'] if 'Category_Level' in df.columns else df
    df_vert = df[df['Category_Level'] == 'Vertical Level'] if 'Category_Level' in df.columns else df
    df_kw = df[df['Category_Level'] == 'Store Level'] if 'Category_Level' in df.columns else df

    return df_sc, df_vert, df_kw

st.title("👗 Women Ethnic Search Intelligence Dashboard")

try:
    df_sc, df_vert, df_kw = load_all_tabs()

    tab1, tab2, tab3 = st.tabs([
        "📊 Supercategory (SC) Level & Observations", 
        "👗 Vertical Level Performance", 
        "🔥 Spiking Trends, Keywords & Store Paths"
    ])

    # TAB 1: SC LEVEL
    with tab1:
        st.header("August 2026 — Executive Summary Header")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.subheader("WE Total")
            st.metric("Total Searches", "118.71 M", delta="15.51% MoM | -1.82% YoY")
            st.metric("CTR", "54.84%", delta="-2.60% MoM | +1.77% YoY", delta_color="normal")
            st.metric("CVR", "0.60%", delta="-1.67% MoM | -1.78% YoY", delta_color="normal")

        with m2:
            st.subheader("Women Ethnic Contemporary")
            st.metric("Total Searches", "75.05 M", delta="12.85% MoM | +2.63% YoY")
            st.metric("CTR", "53.82%", delta="-3.19% MoM | +0.90% YoY", delta_color="normal")
            st.metric("CVR", "0.64%", delta="-4.50% MoM | -1.24% YoY", delta_color="normal")

        with m3:
            st.subheader("Women Ethnic Core")
            st.metric("Total Searches", "43.66 M", delta="20.39% MoM | -8.62% YoY")
            st.metric("CTR", "56.58%", delta="-1.75% MoM | +3.42% YoY", delta_color="normal")
            st.metric("CVR", "0.54%", delta="+5.40% MoM | -2.48% YoY", delta_color="normal")

        st.divider()

        st.header("📋 Consolidated Executive Observations")
        col_green, col_red = st.columns(2)
        
        with col_green:
            st.success("### 🟢 Green Flags (Growth Drivers)")
            st.markdown("""
            * **WE Core Strong MoM Rebound**: Core searches jumped **+20.39% MoM** accompanied by a healthy **+5.40% CVR improvement**.
            * **Massive Category Spikes**: **Sharara** (+262.13% MoM), **Kaftan dress** (+209.55% MoM), **Sambalpuri kurti sets** (+196.99% MoM).
            * **High-Performing Verticals**: **WomenSalwarKurtaDupatta** (+64.33% YoY Searches) and **WomenSalwar** (+184.30% YoY Searches).
            """)

        with col_red:
            st.error("### 🔴 Red Flags (Conversion Dips & Assortment Gaps)")
            st.markdown("""
            * **Contemporary CVR Drop**: Searches grew (+12.85% MoM), but CVR dropped by **-4.50% MoM**.
            * **Assortment & Search Redirection Gaps**: **Umbrella Kurti Sets** (+36.82% spike) flagged for **poor assortment**. **Dola Silk** (+119.70% spike) impacted by **poor CTR & CVR**.
            * **Dipping Verticals**: **WomenEthnicDress** (-33.92% YoY) and **WomenLehengaCholi** (-25.59% YoY).
            """)

        st.divider()
        st.subheader("Raw SC Level Data Matrix")
        st.dataframe(df_sc, use_container_width=True)

    # TAB 2: VERTICAL LEVEL
    with tab2:
        st.header("👗 Vertical Level Trends & Analysis")
        first_vert_col = df_vert.columns[0] if len(df_vert.columns) > 0 else df_vert.columns
        st.dataframe(df_vert, use_container_width=True)

    # TAB 3: KEYWORD LEVEL
    with tab3:
        st.header("🔥 Spiking Keywords & Store Paths")
        st.dataframe(df_kw, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
